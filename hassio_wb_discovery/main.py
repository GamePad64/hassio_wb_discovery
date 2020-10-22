from __future__ import annotations

import asyncio
import json
import re
from asyncio import Task
from collections import AsyncIterable, Iterator
from contextlib import AsyncExitStack
from typing import Any, BinaryIO, Dict, Set, Tuple

import click
import yaml
from asyncio_mqtt import Client as MQTTClient
from deepdiff import DeepDiff
from loguru import logger
from paho.mqtt.client import MQTTMessage
from pydantic.json import pydantic_encoder

from .device_drivers.generic import GenericDriver
from .models.config import Config, DeviceSettings
from .models.hass import HassDevice
from .util import Tree, cancel_tasks

drivers = {"generic": GenericDriver}


async def process_messages(messages: AsyncIterable[MQTTMessage], devices: Tree) -> None:
    async for message in messages:
        if m := re.match("/devices/(?P<subtopic>.+)$", message.topic):
            topics = m["subtopic"].split("/")

            d = devices
            for subtopic in topics[:-1]:
                d = d[subtopic]
            d[topics[-1]] = message.payload


def process_device_tree(config: Config, devices: Tree) -> Iterator[Tuple[str, dict]]:
    for device_id, device in devices.items():
        dm = HassDevice(identifiers=[f"{config.homeassistant.control_prefix}{device_id}"], name=device["meta"]["name"])

        device_settings: DeviceSettings = config.devices.get(device_id, DeviceSettings())
        driver = drivers[device_settings.driver]

        yield from driver.process(device, device_settings, config, device_id, dm)


async def publish_devices(
    client: MQTTClient, config: Config, devices: Tree, published_topics: Dict[str, Dict[str, Any]]
) -> None:
    devices_count = 0
    for topic, payload in process_device_tree(config, devices):
        diff = DeepDiff(published_topics.get(topic, None), payload)
        if diff:
            published_topics[topic] = payload

            payload_json = json.dumps(payload, default=pydantic_encoder)
            await client.publish(topic, payload_json)

            devices_count += 1
            logger.debug(f"Published: {topic}, {payload_json}. Change: {diff}")

    if devices_count:
        logger.info(f"Published {devices_count} devices")


async def periodic_publish_devices(client: MQTTClient, config: Config, devices: Tree, sleep: int = 5) -> None:
    published_topics: Dict[str, Dict[str, Any]] = {}

    while True:
        await asyncio.sleep(sleep)

        await publish_devices(client, config, devices, published_topics)


async def process_birthwill(
    messages: AsyncIterable[MQTTMessage], client: MQTTClient, config: Config, devices: Tree
) -> None:
    async for message in messages:
        if message.topic != config.homeassistant.birth_message.topic:
            continue

        await publish_devices(client, config, devices, dict())


async def main(config: Config) -> None:
    async with AsyncExitStack() as stack:
        tasks: Set[Task[Any]] = set()

        logger.info("Trying to connect to MQTT broker")
        client = MQTTClient(hostname=config.mqtt.host, port=config.mqtt.port, logger=logger)
        await stack.enter_async_context(client)
        stack.push_async_callback(cancel_tasks, tasks)

        logger.info("Connected to MQTT broker")

        devices = Tree()

        device_topic_filters = ["/devices/+/meta/#", "/devices/+/controls/+/meta/#"]

        for topic_filter in device_topic_filters:
            manager = client.filtered_messages(topic_filter)
            messages = await stack.enter_async_context(manager)

            task = asyncio.create_task(process_messages(messages, devices))
            tasks.add(task)

        status_topic_filters = [
            config.homeassistant.birth_message.topic,
        ]

        for topic_filter in status_topic_filters:
            manager = client.filtered_messages(topic_filter)
            messages = await stack.enter_async_context(manager)

            task = asyncio.create_task(process_birthwill(messages, client, config, devices))
            tasks.add(task)

        # Subscribe
        await client.subscribe([(topic, 0) for topic in device_topic_filters])
        await client.subscribe([(topic, 0) for topic in status_topic_filters])

        # Add periodic task
        task = asyncio.create_task(periodic_publish_devices(client, config, devices))
        tasks.add(task)

        await asyncio.gather(*tasks)


@click.command()
@click.option("--config", required=True, type=click.File(mode="rb"), help="Path to the config file")
def cli(config: BinaryIO) -> None:
    conf = Config(**yaml.safe_load(config))

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(conf))

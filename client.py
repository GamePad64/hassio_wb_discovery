from __future__ import annotations

import asyncio
import json
import logging
import re
import signal

import aiojobs
import yaml
from devtools import debug
from gmqtt import Client as MQTTClient
from gmqtt.mqtt.constants import MQTTv311
from pydantic.json import pydantic_encoder

from device_drivers.generic import GenericDriver
from models.config import Config, DeviceSettings
from models.hass import DeviceMeta
from util import Tree

logger = logging.getLogger(__name__)
devices = Tree()
drivers = {"generic": GenericDriver}
STOP = asyncio.Event()


def on_connect(client, flags, rc, properties):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/devices/+/meta/#")
    client.subscribe("/devices/+/controls/+/meta/#")


def on_message(client, topic, payload, qos, properties):
    if m := re.match("/devices/(?P<subtopic>.+)$", topic):
        topics = m['subtopic'].split('/')

        d = devices
        for subtopic in topics[:-1]:
            d = d[subtopic]
        d[topics[-1]] = payload


def on_disconnect(client, packet, exc=None):
    logger.info('Disconnected from MQTT broker')


def ask_exit(*args):
    STOP.set()


def process_device_tree(config: Config):
    for device_id, device in devices.items():
        dm = DeviceMeta(identifiers=[f"{config.homeassistant.control_prefix}{device_id}"], name=device['meta']['name'])

        device_settings: DeviceSettings = config.devices.get(device_id, DeviceSettings())
        driver = drivers[device_settings.driver]

        yield from driver.process(device, device_settings, config, device_id, dm)


async def process_device_tree_task(client: MQTTClient, config: Config):
    while 1:
        await asyncio.sleep(5)

        for topic, payload in process_device_tree(config):
            # debug((topic, payload.json(exclude_none=True)))
            payload_json = json.dumps(payload, default=pydantic_encoder)
            client.publish(topic, payload_json)
            print(f"Published: {topic}, {payload_json}")


async def main(config: Config):
    scheduler = await aiojobs.create_scheduler()

    client = MQTTClient("wb2hass")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    await client.connect(config.mqtt.host, config.mqtt.port, keepalive=60, version=MQTTv311)

    await scheduler.spawn(process_device_tree_task(client, config))

    await STOP.wait()
    await client.disconnect()
    await scheduler.close()


if __name__ == '__main__':
    with open("config.yaml") as f:
        conf = Config(**yaml.safe_load(f))

    debug(conf)
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(conf))

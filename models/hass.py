from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class DeviceMeta(BaseModel):
    connections: Optional[List[str]]
    identifiers: Optional[Union[List[str], str]]
    manufacturer: Optional[str]
    model: Optional[str]
    name: Optional[str]
    sw_version: Optional[str]
    via_device: Optional[str]


class Availability(BaseModel):
    payload_available: Optional[str]
    payload_not_available: Optional[str]
    topic: str


class SwitchMeta(BaseModel):
    availability: Optional[Availability]
    availability_topic: Optional[str]

    command_topic: Optional[str]
    device: Optional[DeviceMeta]
    icon: Optional[str]

    name: Optional[str]
    optimistic: Optional[bool]

    payload_available: Optional[str]
    payload_not_available: Optional[str]
    payload_off: Optional[str]
    payload_on: Optional[str]

    qos: Optional[int]
    retain: Optional[bool]

    state_off: Optional[str]
    state_on: Optional[str]
    state_topic: Optional[str]

    unique_id: Optional[str]
    value_template: Optional[str]


class BinarySensorMeta(BaseModel):
    class DeviceClass(Enum):
        BATTERY = "battery"
        BATTERY_CHARGING = "battery_charging"
        COLD = "cold"
        CONNECTIVITY = "connectivity"
        DOOR = "door"
        GARAGE_DOOR = "garage_door"
        GAS = "gas"
        HEAT = "heat"
        LIGHT = "light"
        LOCK = "lock"
        MOISTURE = "moisture"
        MOTION = "motion"
        MOVING = "moving"
        OCCUPANCY = "occupancy"
        OPENING = "opening"
        PLUG = "plug"
        POWER = "power"
        PRESENCE = "presence"
        PROBLEM = "problem"
        SAFETY = "safety"
        SMOKE = "smoke"
        SOUND = "sound"
        VIBRATION = "vibration"
        WINDOW = "window"

    availability: Optional[Availability]
    availability_topic: Optional[str]

    device: Optional[DeviceMeta]
    device_class: Optional[DeviceClass]
    name: Optional[str]

    payload_available: Optional[str]
    payload_not_available: Optional[str]
    payload_off: Optional[str]
    payload_on: Optional[str]

    qos: Optional[int]

    state_topic: str
    unique_id: Optional[str]
    value_template: Optional[str]


class SensorMeta(BaseModel):
    class DeviceClass(Enum):
        BATTERY = "battery"
        HUMIDITY = "humidity"
        ILLUMINANCE = "illuminance"
        SIGNAL_STRENGTH = "signal_strength"
        TEMPERATURE = "temperature"
        POWER = "power"
        PRESSURE = "pressure"
        TIMESTAMP = "timestamp"
        CURRENT = "current"
        ENERGY = "energy"
        POWER_FACTOR = "power_factor"
        VOLTAGE = "voltage"

    availability_topic: Optional[str]

    device: Optional[DeviceMeta]
    device_class: Optional[DeviceClass]

    expire_after: Optional[int]
    force_update: Optional[bool]

    icon: Optional[str]

    name: Optional[str]

    payload_available: Optional[str]
    payload_not_available: Optional[str]
    qos: Optional[int]

    state_topic: str
    unique_id: Optional[str]
    unit_of_measurement: Optional[str]
    value_template: Optional[str]

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class HassIntegrationType(Enum):
    SWITCH = "switch"
    BINARY_SENSOR = "binary_sensor"
    SENSOR = "sensor"
    LIGHT = "light"
    FAN = "fan"
    ALARM = "alarm_control_panel"
    CAMERA = "camera"
    COVER = "cover"
    DEVICE_TRIGGER = "device_trigger"
    CLIMATE = "climate"
    LOCK = "lock"
    TAG = "tag"
    VACUUM = "vacuum"


class HassDevice(BaseModel):
    connections: Optional[List[str]]
    identifiers: Optional[Union[List[str], str]]
    manufacturer: Optional[str]
    model: Optional[str]
    name: Optional[str]
    sw_version: Optional[str]
    via_device: Optional[str]


class HassAvailability(BaseModel):
    payload_available: Optional[str]
    payload_not_available: Optional[str]
    topic: str


class HassSwitchMeta(BaseModel):
    availability: Optional[HassAvailability]
    availability_topic: Optional[str]

    command_topic: Optional[str]
    device: Optional[HassDevice]
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


class HassBinarySensorMeta(BaseModel):
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

    availability: Optional[HassAvailability]
    availability_topic: Optional[str]

    device: Optional[HassDevice]
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


class HassSensorMeta(BaseModel):
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

    device: Optional[HassDevice]
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

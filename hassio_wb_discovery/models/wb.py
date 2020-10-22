from enum import Enum
from typing import Optional

from pydantic import BaseModel


class WBControlMetaType(Enum):
    SWITCH = b"switch"
    WO_SWITCH = b"wo-switch"
    PUSHBUTTON = b"pushbutton"
    RANGE = b"range"
    RGB = b"rgb"
    ALARM = b"alarm"
    TEXT = b"text"
    VALUE = b"value"
    # Value-like
    TEMPERATURE = b"temperature"
    REL_HUMIDITY = b"rel_humidity"
    ATMOSPHERIC_PRESSURE = b"atmospheric_pressure"
    RAINFALL = b"rainfall"
    WIND_SPEED = b"wind_speed"
    POWER = b"power"
    POWER_CONSUMPTION = b"power_consumption"
    VOLTAGE = b"voltage"
    WATER_FLOW = b"water_flow"
    WATER_CONSUMPTION = b"water_consumption"
    RESISTANCE = b"resistance"
    CONCENTRATION = b"concentration"
    HEAT_POWER = b"heat_power"
    HEAT_ENERGY = b"heat_energy"

    @property
    def is_value_like(self) -> bool:
        return self in [
            self.VALUE,
            self.TEMPERATURE,
            self.REL_HUMIDITY,
            self.ATMOSPHERIC_PRESSURE,
            self.RAINFALL,
            self.WIND_SPEED,
            self.POWER,
            self.POWER_CONSUMPTION,
            self.VOLTAGE,
            self.WATER_FLOW,
            self.WATER_CONSUMPTION,
            self.RESISTANCE,
            self.CONCENTRATION,
            self.HEAT_POWER,
            self.HEAT_ENERGY,
        ]


class WBControlMeta(BaseModel):
    type: WBControlMetaType
    readonly: Optional[int]

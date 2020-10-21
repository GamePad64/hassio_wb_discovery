from models.hass import HassSensorMeta
from models.wb import WBControlMetaType

VALUE_MAPPING = {
    WBControlMetaType.TEMPERATURE: HassSensorMeta.DeviceClass.TEMPERATURE,
    WBControlMetaType.REL_HUMIDITY: HassSensorMeta.DeviceClass.HUMIDITY,
    WBControlMetaType.ATMOSPHERIC_PRESSURE: HassSensorMeta.DeviceClass.PRESSURE,
    WBControlMetaType.POWER: HassSensorMeta.DeviceClass.POWER,
    WBControlMetaType.POWER_CONSUMPTION: HassSensorMeta.DeviceClass.ENERGY,
    WBControlMetaType.VOLTAGE: HassSensorMeta.DeviceClass.VOLTAGE,
}

VALUE_UNITS = {
    WBControlMetaType.TEMPERATURE: "°C",
    WBControlMetaType.REL_HUMIDITY: "%",
    WBControlMetaType.ATMOSPHERIC_PRESSURE: "mbar",
    WBControlMetaType.RAINFALL: "mm/hour",
    WBControlMetaType.WIND_SPEED: "m/s",
    WBControlMetaType.POWER: "W",
    WBControlMetaType.POWER_CONSUMPTION: "kWh",
    WBControlMetaType.VOLTAGE: "V",
    WBControlMetaType.WATER_FLOW: "m³/hour",
    WBControlMetaType.WATER_CONSUMPTION: "m³",
    WBControlMetaType.RESISTANCE: "Ohm",
    WBControlMetaType.CONCENTRATION: "ppm",
    WBControlMetaType.HEAT_POWER: "Gcal/hour",
    WBControlMetaType.HEAT_ENERGY: "Gcal",
}

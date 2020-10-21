from models.hass import SensorMeta
from models.wb import WBControlMetaType

VALUE_MAPPING = {
    WBControlMetaType.TEMPERATURE: SensorMeta.DeviceClass.TEMPERATURE,
    WBControlMetaType.REL_HUMIDITY: SensorMeta.DeviceClass.HUMIDITY,
    WBControlMetaType.ATMOSPHERIC_PRESSURE: SensorMeta.DeviceClass.PRESSURE,
    WBControlMetaType.POWER: SensorMeta.DeviceClass.POWER,
    WBControlMetaType.POWER_CONSUMPTION: SensorMeta.DeviceClass.ENERGY,
    WBControlMetaType.VOLTAGE: SensorMeta.DeviceClass.VOLTAGE,
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

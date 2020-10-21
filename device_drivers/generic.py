from typing import Any, Dict, Tuple, Iterator

from slugify import slugify

from models.config import Config, DeviceSettings, ControlSettings
from models.hass import BinarySensorMeta, DeviceMeta, SensorMeta, SwitchMeta
from models.mappings import VALUE_MAPPING, VALUE_UNITS
from models.wb import WBControlMeta, WBControlMetaType


class GenericDriver:
    @staticmethod
    def process(device: Dict[str, Dict[str, Any]], device_settings: DeviceSettings, config: Config, device_id: str, dm: DeviceMeta) -> Iterator[Tuple[str, dict]]:
        for control_id, control in device["controls"].items():
            # Check if control is excluded in config
            for exclude_pattern in device_settings.exclude_controls:
                if exclude_pattern.match(control_id):
                    return

            wb_control_meta = WBControlMeta(**control['meta'])

            unique_id = slugify(f"{config.homeassistant.control_prefix}{device_id}_{control_id}", separator="_")
            control_name = f"{dm.name} | {control_id}"
            wb_value_topic = f"/devices/{device_id}/controls/{control_id}"

            control_settings = device_settings.controls.get(control_id, ControlSettings())

            if wb_control_meta.type == WBControlMetaType.SWITCH:
                if not wb_control_meta.readonly:
                    integration_type = control_settings.force_type or "switch"

                    topic = f"{config.homeassistant.discovery_prefix}/{integration_type}/{unique_id}/config"
                    meta = SwitchMeta(
                        device=dm,
                        command_topic=wb_value_topic,
                        payload_off="0",
                        payload_on="1",
                        state_topic=wb_value_topic,
                        name=control_name,
                        unique_id=unique_id,
                    )

                    yield topic, {**meta.dict(exclude_unset=True, exclude_none=True), **control_settings.overrides}
                else:
                    topic = f"{config.homeassistant.discovery_prefix}/binary_sensor/{unique_id}/config"
                    meta = BinarySensorMeta(
                        device=dm,
                        payload_off="0",
                        payload_on="1",
                        state_topic=wb_value_topic,
                        name=control_name,
                        unique_id=unique_id,
                    )

                    yield topic, {**meta.dict(exclude_unset=True, exclude_none=True), **control_settings.overrides}
            if wb_control_meta.type.is_value_like():
                topic = f"{config.homeassistant.discovery_prefix}/sensor/{unique_id}/config"
                meta = SensorMeta(
                    device=dm,
                    device_class=VALUE_MAPPING.get(wb_control_meta.type),
                    state_topic=wb_value_topic,
                    name=control_name,
                    unique_id=unique_id,
                    unit_of_measurement=VALUE_UNITS.get(wb_control_meta.type)
                )

                yield topic, {**meta.dict(exclude_unset=True, exclude_none=True), **control_settings.overrides}

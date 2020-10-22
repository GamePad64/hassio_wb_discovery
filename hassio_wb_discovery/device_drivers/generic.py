from __future__ import annotations

from typing import Any, Dict, Iterator, Optional, Tuple

from pydantic import BaseModel
from slugify import slugify

from ..models.config import Config, ControlSettings, DeviceSettings
from ..models.hass import HassBinarySensorMeta, HassDevice, HassIntegrationType, HassSensorMeta, HassSwitchMeta
from ..models.mappings import VALUE_MAPPING, VALUE_UNITS
from ..models.wb import WBControlMeta, WBControlMetaType


class UnknownIntegrationError(Exception):
    pass


class GenericControl:
    def __init__(
        self,
        control_settings: ControlSettings,
        wb_control_meta: WBControlMeta,
        device_id: str,
        control_id: str,
        config: Config,
    ):
        self.control_settings = control_settings
        self.wb_control_meta = wb_control_meta
        self.device_id = device_id
        self.control_id = control_id
        self.config = config

    @property
    def integration_logic(self) -> HassIntegrationType:
        if self.wb_control_meta.type == WBControlMetaType.SWITCH:
            if not self.wb_control_meta.readonly:
                return HassIntegrationType.SWITCH
            else:
                return HassIntegrationType.BINARY_SENSOR
        elif self.wb_control_meta.type.is_value_like:
            return HassIntegrationType.SENSOR

        raise UnknownIntegrationError()

    @property
    def _integration_type(self) -> HassIntegrationType:
        if self.integration_logic == HassIntegrationType.SWITCH and self.control_settings.force_type:
            return HassIntegrationType(self.control_settings.force_type)
        return self.integration_logic

    def meta_to_dict(self, meta: BaseModel) -> dict:
        return {**meta.dict(exclude_unset=True, exclude_none=True), **self.control_settings.overrides}

    @property
    def device_class(self) -> Optional[HassSensorMeta.DeviceClass]:
        return VALUE_MAPPING.get(self.wb_control_meta.type)

    @property
    def unit_of_measurement(self) -> Optional[str]:
        return VALUE_UNITS.get(self.wb_control_meta.type)

    @property
    def unique_id(self) -> str:
        return slugify(f"{self.config.homeassistant.control_prefix}{self.device_id}_{self.control_id}", separator="_")

    @property
    def topic(self) -> str:
        return f"{self.config.homeassistant.discovery_prefix}/{self._integration_type.value}/{self.unique_id}/config"

    @property
    def wb_value_topic(self) -> str:
        return f"/devices/{self.device_id}/controls/{self.control_id}"

    @property
    def wb_command_topic(self) -> str:
        return f"/devices/{self.device_id}/controls/{self.control_id}/on"


class GenericDriver:
    @classmethod
    def process(
        cls,
        device: Dict[str, Dict[str, Any]],
        device_settings: DeviceSettings,
        config: Config,
        device_id: str,
        hass_device: HassDevice,
    ) -> Iterator[Tuple[str, dict]]:
        for control_id, wb_control in device["controls"].items():
            # Check if control is excluded in config
            for exclude_pattern in device_settings.exclude_controls:
                if exclude_pattern.match(control_id):
                    return

            wb_control_meta = WBControlMeta(**wb_control["meta"])

            control_name = f"{hass_device.name} | {control_id}"

            control = GenericControl(
                control_settings=device_settings.controls.get(control_id, ControlSettings()),
                wb_control_meta=wb_control_meta,
                device_id=device_id,
                control_id=control_id,
                config=config,
            )

            if control.integration_logic == HassIntegrationType.SWITCH:
                yield control.topic, control.meta_to_dict(
                    HassSwitchMeta(
                        device=hass_device,
                        command_topic=control.wb_command_topic,
                        payload_off="0",
                        payload_on="1",
                        state_topic=control.wb_value_topic,
                        name=control_name,
                        unique_id=control.unique_id,
                    )
                )
            elif control.integration_logic == HassIntegrationType.BINARY_SENSOR:
                yield control.topic, control.meta_to_dict(
                    HassBinarySensorMeta(
                        device=hass_device,
                        payload_off="0",
                        payload_on="1",
                        state_topic=control.wb_value_topic,
                        name=control_name,
                        unique_id=control.unique_id,
                    )
                )
            elif control.integration_logic == HassIntegrationType.SENSOR:
                yield control.topic, control.meta_to_dict(
                    HassSensorMeta(
                        device=hass_device,
                        device_class=control.device_class,
                        state_topic=control.wb_value_topic,
                        name=control_name,
                        unique_id=control.unique_id,
                        unit_of_measurement=control.unit_of_measurement,
                    )
                )

from collections import defaultdict
from functools import partial
from typing import Any, Dict, Optional, Pattern, List

from pydantic import BaseModel, BaseSettings, Field, conint


class MQTTSettings(BaseModel):
    host: str
    port: conint(lt=65536, ge=1) = 1883


class HomeAssistantSettings(BaseModel):
    discovery_prefix: str = "homeassistant"
    control_prefix: str = "wirenboard_"


class ControlSettings(BaseModel):
    force_type: Optional[str]
    overrides: Dict[str, Any] = Field(default_factory=dict)


class DeviceSettings(BaseModel):
    driver: str = Field(default="generic")
    controls: Dict[str, ControlSettings] = Field(default_factory=dict)
    exclude_controls: List[Pattern] = Field(default_factory=list)


class Config(BaseSettings):
    mqtt: MQTTSettings
    homeassistant: HomeAssistantSettings = Field(default=HomeAssistantSettings())
    devices: Dict[str, DeviceSettings] = Field(default_factory=partial(defaultdict, DeviceSettings))

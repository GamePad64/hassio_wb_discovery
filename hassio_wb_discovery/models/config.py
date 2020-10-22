from __future__ import annotations

from typing import Any, Dict, List, Optional, Pattern

from pydantic import BaseModel, BaseSettings, Field, conint


class MQTTSettings(BaseModel):
    host: str
    port: conint(lt=65536, ge=1) = 1883  # type: ignore


class BirthTopic(BaseModel):
    topic: str = "homeassistant/status"
    payload: str = "online"


class LastWillTopic(BaseModel):
    topic: str = "homeassistant/status"
    payload: str = "offline"


class HomeAssistantSettings(BaseModel):
    discovery_prefix: str = "homeassistant"
    control_prefix: str = "wirenboard_"
    birth_message: BirthTopic = Field(default_factory=BirthTopic)
    will_message: LastWillTopic = Field(default_factory=LastWillTopic)


class ControlSettings(BaseModel):
    force_type: Optional[str]
    overrides: Dict[str, Any] = Field(default_factory=dict)


class DeviceSettings(BaseModel):
    driver: str = Field(default="generic")
    controls: Dict[str, ControlSettings] = Field(default_factory=dict)
    exclude_controls: List[Pattern] = Field(default_factory=list)


class Config(BaseSettings):
    mqtt: MQTTSettings
    homeassistant: HomeAssistantSettings = Field(default_factory=HomeAssistantSettings)
    devices: Dict[str, DeviceSettings] = Field(default_factory=dict)

"""Contrato de telemetría v1. null significa que no hay una medición."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Source = Literal["device", "demo"]


class TelemetryInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)

    robot_id: Literal["robot-01"] = "robot-01"
    battery_v: float | None = Field(default=None, ge=0, le=20)
    distance_cm: float | None = Field(default=None, ge=0, le=1000)
    ir_left: bool | None = None
    ir_right: bool | None = None
    pwm_left: int | None = Field(default=None, ge=-255, le=255)
    pwm_right: int | None = Field(default=None, ge=-255, le=255)

    @model_validator(mode="after")
    def has_measurement(self):
        if all(value is None for key, value in self.model_dump().items() if key != "robot_id"):
            raise ValueError("Enviá al menos una medición u orden PWM registrada")
        return self


class TelemetryRecord(BaseModel):
    id: int
    robot_id: str
    source: Source
    received_at: str
    battery_v: float | None
    distance_cm: float | None
    ir_left: bool | None
    ir_right: bool | None
    pwm_left: int | None
    pwm_right: int | None


class TelemetryHistory(BaseModel):
    items: list[TelemetryRecord]
    total: int


class EmptyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DemoState(BaseModel):
    running: bool

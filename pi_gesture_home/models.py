"""Typed values shared by vision, gesture logic, and device control."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Command(str, Enum):
    LIGHT_ON = "light_on"
    LIGHT_OFF = "light_off"
    BRIGHTER = "brighter"
    DIMMER = "dimmer"
    MEDIA_NEXT = "media_next"
    CANCEL = "cancel"


@dataclass(frozen=True)
class Detection:
    timestamp: float
    pose: str
    confidence: float
    palm_x: float
    palm_y: float


@dataclass(frozen=True)
class EngineEvent:
    timestamp: float
    kind: str
    detail: str
    command: Command | None = None

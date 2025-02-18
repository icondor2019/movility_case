from pydantic import BaseModel
# from enum import Enum


class DamageResponse(BaseModel):
    damaged_system: str


class SpecificVolumeResponse(BaseModel):
    specific_volume_liquid: float
    specific_volume_vapor: float

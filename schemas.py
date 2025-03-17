from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class RollCreate(BaseModel):
    length: float = Field(..., gt=0, description="Length must be greater than 0")
    weight: float = Field(..., gt=0, description="Weight must be greater than 0")


class RollDelete(BaseModel):
    id: int


class RollFilter(BaseModel):
    id: Optional[Tuple[int, int]] = None
    length: Optional[Tuple[float, float]] = None
    weight: Optional[Tuple[float, float]] = None
    date_added: Optional[Tuple[datetime, datetime]] = None
    date_removed: Optional[Tuple[datetime, datetime]] = None


class RollTime(BaseModel):
    start_date: datetime
    end_date: datetime


class RollResponse(BaseModel):
    id: int
    length: float
    weight: float
    date_added: datetime


class RollDeleted(RollResponse):
    date_removed: datetime


class RollFull(RollResponse):
    date_removed: datetime | None = None


class RollStatistics(BaseModel):
    added_count: int
    removed_count: int
    average_length: float
    average_weight: float
    max_length: float
    min_length: float
    max_weight: float
    min_weight: float
    total_weight: float
    max_time_diff: Optional[float] = None
    min_time_diff: Optional[float] = None

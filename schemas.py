from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel


class RollCreate(BaseModel):
    length: float
    weight: float


class RollDelete(BaseModel):
    id: int


class RollFilter(BaseModel):
    id: Optional[Tuple[int, int]] = None
    length: Optional[Tuple[float, float]] = None
    weight: Optional[Tuple[float, float]] = None
    date_added: Optional[Tuple[datetime, datetime]] = None
    date_removed: Optional[Tuple[datetime, datetime]] = None

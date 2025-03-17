from datetime import datetime
from datetime import timezone
from typing import Type, Sequence, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Roll

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Roll


def add_roll(session: Session, length: float, weight: float) -> Roll:
    if length <= 0 or weight <= 0:
        raise ValueError("length and weight must be positive values")

    roll = Roll(length=length, weight=weight, date_added=datetime.now(timezone.utc))
    session.add(roll)
    session.commit()
    session.refresh(roll)
    return roll


def remove_roll(session: Session, roll_id: int) -> Type[Roll] | None:
    roll = session.get(Roll, roll_id)
    if roll:
        roll.date_removed = datetime.now(timezone.utc)
        session.commit()
        return roll
    return None


class RollFilter(BaseModel):
    id: Optional[Tuple[int, int]] = None
    length: Optional[Tuple[float, float]] = None
    weight: Optional[Tuple[float, float]] = None
    date_added: Optional[Tuple[datetime, datetime]] = None
    date_removed: Optional[Tuple[datetime, datetime]] = None


def filter_rolls(session: Session, roll_filter: RollFilter):
    query = select(Roll)

    for key, value in vars(roll_filter).items():
        if value:
            field = getattr(Roll, key, None)
            if field and value[0] is not None and value[1] is not None:
                query = query.filter(field.between(value[0], value[1]))

    result = session.execute(query).scalars().all()
    return result

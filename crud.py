from sqlalchemy.orm import Session

from models import Roll
from datetime import datetime, timezone


def add_roll(session: Session, length: float, weight: float) -> Roll:
    if length <= 0 or weight <= 0:
        raise ValueError("length and weight must be positive values")

    roll = Roll(length=length, weight=weight, date_added=datetime.now(timezone.utc))
    session.add(roll)
    session.commit()
    session.refresh(roll)
    return roll

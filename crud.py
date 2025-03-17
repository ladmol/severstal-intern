from datetime import datetime
from datetime import timezone
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Roll
from schemas import RollFilter, RollCreate, RollDelete


def add_roll(session: Session, roll_create: RollCreate) -> Roll:
    if roll_create.length <= 0 or roll_create.weight <= 0:
        raise ValueError("length and weight must be positive values")

    roll = Roll(
        length=roll_create.length,
        weight=roll_create.weight,
        date_added=datetime.now(timezone.utc),
    )
    session.add(roll)
    session.commit()
    session.refresh(roll)
    return roll


def remove_roll(session: Session, roll_delete: RollDelete) -> Type[Roll] | None:
    roll = session.get(Roll, roll_delete.id)
    if roll:
        roll.date_removed = datetime.now(timezone.utc)
        session.commit()
        return roll
    return None


def filter_rolls(session: Session, roll_filter: RollFilter):
    query = select(Roll)

    for key, value in vars(roll_filter).items():
        if value:
            field = getattr(Roll, key, None)
            if field and value[0] is not None and value[1] is not None:
                query = query.filter(field.between(value[0], value[1]))

    result = session.execute(query).scalars().all()
    return result

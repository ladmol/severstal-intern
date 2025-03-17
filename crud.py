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


def get_added_rolls_count(
    session: Session, start_date: datetime, end_date: datetime
) -> int:
    return (
        session.query(Roll)
        .filter(Roll.date_added.between(start_date, end_date))
        .count()
    )


def get_removed_rolls_count(
    session: Session, start_date: datetime, end_date: datetime
) -> int:
    return (
        session.query(Roll)
        .filter(Roll.date_removed.between(start_date, end_date))
        .count()
    )


def get_average_length_and_weight(
    session: Session, start_date: datetime, end_date: datetime
) -> tuple:
    rolls = (
        session.query(Roll).filter(Roll.date_added.between(start_date, end_date)).all()
    )
    total_length = sum(roll.length for roll in rolls)
    total_weight = sum(roll.weight for roll in rolls)
    rolls_len = len(rolls)
    return (total_length / rolls_len, total_weight / rolls_len) if rolls else (0, 0)


def get_max_min_length_and_weight(
    session: Session, start_date: datetime, end_date: datetime
) -> tuple:
    rolls = (
        session.query(Roll).filter(Roll.date_added.between(start_date, end_date)).all()
    )
    max_length = max(roll.length for roll in rolls)
    min_length = min(roll.length for roll in rolls)
    max_weight = max(roll.weight for roll in rolls)
    min_weight = min(roll.weight for roll in rolls)
    return (max_length, min_length, max_weight, min_weight) if rolls else (0, 0, 0, 0)


def get_total_weight(
    session: Session, start_date: datetime, end_date: datetime
) -> float:
    rolls = (
        session.query(Roll).filter(Roll.date_added.between(start_date, end_date)).all()
    )
    return sum(roll.weight for roll in rolls)


def get_max_min_time_diff(
    session: Session, start_date: datetime, end_date: datetime
) -> tuple:
    rolls = (
        session.query(Roll).filter(Roll.date_added.between(start_date, end_date)).all()
    )
    time_diffs = [
        (roll.date_removed - roll.date_added).total_seconds()
        for roll in rolls
        if roll.date_removed and roll.date_added
    ]
    return (max(time_diffs), min(time_diffs)) if time_diffs else (0, 0)

def calculate_statistics(session: Session, start_date: datetime, end_date: datetime):
    added_count = get_added_rolls_count(session, start_date, end_date)
    removed_count = get_removed_rolls_count(session, start_date, end_date)
    avg_length, avg_weight = get_average_length_and_weight(session, start_date, end_date)
    max_length, min_length, max_weight, min_weight = get_max_min_length_and_weight(session, start_date, end_date)
    total_weight = get_total_weight(session, start_date, end_date)
    max_time_diff, min_time_diff = get_max_min_time_diff(session, start_date, end_date)

    return {
        "added_count": added_count,
        "removed_count": removed_count,
        "average_length": avg_length,
        "average_weight": avg_weight,
        "max_length": max_length,
        "min_length": min_length,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "total_weight": total_weight,
        "max_time_diff": max_time_diff,
        "min_time_diff": min_time_diff
    }
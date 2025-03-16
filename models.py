from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Roll(Base):
    __tablename__ = "rolls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    length: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), nullable=False
    )
    date_removed: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<Roll(id={self.id}, length={self.length}, weight={self.weight})>"

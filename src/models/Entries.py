from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class Entries(Base):
	__tablename__ = "entries"

	sensor_id: Mapped[str] = mapped_column(
		String,
		ForeignKey("sensor.sid"),
		primary_key=True,
	)
	timestamp: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		primary_key=True,
	)
	reading: Mapped[float] = mapped_column(Float, nullable=False)

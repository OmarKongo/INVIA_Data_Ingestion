from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base

 
class Sensor(Base):
	__tablename__ = "sensor"

	sid: Mapped[str] = mapped_column(String, primary_key=True)
	s_name: Mapped[str] = mapped_column(String, nullable=False)
	s_vendor: Mapped[str] = mapped_column(String, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), default=datetime.utcnow, nullable=False
	)
	updated_at: Mapped[datetime | None] = mapped_column(
		DateTime(timezone=True), nullable=True
	)

	
	

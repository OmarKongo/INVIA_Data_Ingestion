from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Entries(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	sensor_id: str
	timestamp: datetime
	reading: float

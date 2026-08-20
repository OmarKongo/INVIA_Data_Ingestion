from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorCreate(BaseModel):
	sid: str
	s_name: str
	s_vendor: str


class Sensor(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	sid: str
	s_name: str
	s_vendor: str
	created_at: datetime 
	updated_at: datetime | None

import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import Entries as EntriesModel
from models import Sensor as SensorModel
from schemas import Entries as EntriesSchema
from schemas.Sensor import SensorCreate

logger = logging.getLogger("uvicorn.error")


class Engine:
	@staticmethod
	def create_sensor(sensor: SensorCreate, db: Session) -> SensorModel:
		if db.get(SensorModel, sensor.sid) is not None:
			logger.error("Sensor '%s' already exists", sensor.sid)
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"Sensor '{sensor.sid}' already exists",
			)

		db_item = SensorModel(
			sid=sensor.sid,
			s_name=sensor.s_name,
			s_vendor=sensor.s_vendor,
		)
		try:
			db.add(db_item)
			db.commit()
			return db_item
		except SQLAlchemyError:
			db.rollback()
			logger.exception("Failed to save sensor '%s'", sensor.sid)
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Sensor could not be saved",
			)

	@staticmethod
	def create_entry(entry: EntriesSchema, db: Session) -> EntriesModel:
		if db.get(SensorModel, entry.sensor_id) is None:
			logger.error("Sensor '%s' does not exist", entry.sensor_id)
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Sensor '{entry.sensor_id}' does not exist",
			)

		if db.get(EntriesModel, (entry.sensor_id, entry.timestamp)) is not None:
			logger.error(
				"Entry for sensor '%s' at '%s' already exists",
				entry.sensor_id,
				entry.timestamp,
			)
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail="The reading at this timestamp already exists",
			)

		db_item = EntriesModel(
			sensor_id=entry.sensor_id,
			timestamp=entry.timestamp,
			reading=entry.reading,
		)
		try:
			db.add(db_item)
			db.commit()
			return db_item
		except SQLAlchemyError:
			db.rollback()
			logger.exception(
				"Failed to save entry for sensor '%s'", entry.sensor_id
			)
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Entry could not be saved",
			)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers.Engine import Engine
from database import get_db
from schemas import Sensor as SensorSchema
from schemas import Entries as EntriesSchema
from schemas.Sensor import SensorCreate

sensor_route = APIRouter()


@sensor_route.post("/sensors/", response_model=SensorSchema, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    return Engine.create_sensor(sensor, db)


@sensor_route.post("/entries/", response_model=EntriesSchema, status_code=status.HTTP_201_CREATED)
def create_entry(entry: EntriesSchema, db: Session = Depends(get_db)):
    return Engine.create_entry(entry, db)
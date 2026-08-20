from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.Engine import Engine
from database import get_db
from schemas import Sensor as SensorSchema
from schemas import Entries as EntriesSchema
from schemas.Sensor import SensorCreate

sensor_route = APIRouter()


@sensor_route.post("/sensors/", response_model=SensorSchema, status_code=status.HTTP_201_CREATED)
async def create_sensor(sensor: SensorCreate, db: AsyncSession = Depends(get_db)):
    return await Engine.create_sensor(sensor, db)


@sensor_route.post("/entries/", response_model=EntriesSchema, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntriesSchema, db: AsyncSession = Depends(get_db)):
    return await Engine.create_entry(entry, db)
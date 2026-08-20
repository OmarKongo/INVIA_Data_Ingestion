import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import route
from database import engine
from models.Base import Base
# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)
app = FastAPI()
logger = logging.getLogger("uvicorn.error")


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.error(
        "Request schema validation failed for %s %s: %s",
        request.method,
        request.url.path,
        exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# Root endpoint for basic check
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI CRUD API!"}

app.include_router(route.sensor_route)


# INVIA Data Ingestion

A FastAPI service for registering sensors and storing sensor readings in a
SQLite database through SQLAlchemy.

## Project Structure

```text
.
├── README.md
└── src/
    ├── main.py                 # FastAPI application and startup table creation
    ├── route.py                # HTTP routes and dependency injection
    ├── database.py             # SQLAlchemy engine, session factory, and get_db
    ├── controllers/
    │   └── Engine.py           # Business logic and database write handling
    ├── models/
    │   ├── Base.py             # SQLAlchemy declarative base
    │   ├── Sensor.py           # sensor table model
	│   └── Entries.py          # entries table model
    └── schemas/
        ├── Sensor.py           # sensor request and response schemas
        └── Entries.py          # reading request and response schema
```

### Request Flow

1. FastAPI receives and validates the JSON request against a Pydantic schema.
2. A route in `route.py` injects a SQLAlchemy session using `get_db()`.
3. The route delegates business logic to `controllers/Engine.py`.
4. The controller checks references and duplicates, writes to the database,
   and rolls back and logs SQLAlchemy failures.

## Routes

### `GET /`

Returns a basic service health message:

```json
{
	"message": "Welcome to the FastAPI CRUD API!"
}
```

### `POST /sensors/`

Creates a sensor. The request does not include timestamps; `created_at` is
assigned by the database model and `updated_at` may be `null`.

Request:

```json
{
	"sid": "sensor-001",
	"s_name": "Temperature Sensor",
	"s_vendor": "Acme"
}
```

Response (`201 Created`):

```json
{
	"sid": "sensor-001",
	"s_name": "Temperature Sensor",
	"s_vendor": "Acme",
	"created_at": "2026-08-20T12:00:00",
	"updated_at": null
}
```

If the `sid` already exists, the service logs an error and returns `409
Conflict`.

### `POST /entries/`

Creates a reading for an existing sensor.

Request:

```json
{
	"sensor_id": "sensor-001",
	"timestamp": "2026-08-20T12:30:00Z",
	"reading": 23.7
}
```

Response (`201 Created`):

```json
{
	"sensor_id": "sensor-001",
	"timestamp": "2026-08-20T12:30:00Z",
	"reading": 23.7
}
```

The referenced sensor must exist. Otherwise, the service logs an error and
returns `404 Not Found`. An entry is uniquely identified by the composite
primary key `(sensor_id, timestamp)`; attempting to insert the same reading
again returns `409 Conflict` with `The reading at this timestamp already
exists`.

## Schemas

### `SensorCreate`

Used by `POST /sensors/`. All fields are required:

- `sid: string`
- `s_name: string`
- `s_vendor: string`

### `Sensor`

Used as the sensor response schema. It contains the create fields plus:

- `created_at: datetime`
- `updated_at: datetime | null`

It uses Pydantic's `from_attributes` configuration so SQLAlchemy model
instances can be returned directly from the route.

### `Entries`

Used by both the request and response for `POST /entries/`:

- `sensor_id: string`
- `timestamp: datetime`
- `reading: float`

Malformed JSON or values that do not match these schemas are logged by the
global FastAPI validation handler and return `422 Unprocessable Entity`.

## Database

The service uses SQLite with the URL `sqlite:///./test.db`. The SQLAlchemy
engine and connection pool are initialized when the application starts. A
short-lived session is created for each request and closed afterward; the
underlying connections are returned to the engine pool.

The tables are created from the model metadata during application startup:

- `sensor`: keyed by `sid`
- `entries`: keyed by `(sensor_id, timestamp)` and linked to `sensor.sid`

## Running Locally

From the repository root:

```bash
python -m pip install -r src/requirements.txt
cd src
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation
is available at `http://127.0.0.1:8000/docs`.

## Scaling Considerations

Assume the service is deployed in Docker on a server with 2 CPU cores and
2 GB of RAM. The load must increase from 10 sensors to 10,000 sensors, with
each sensor sending one reading per second. This represents up to 10,000
incoming readings per second, so the application, database, and network must
all be tested under the expected workload.

There are two primary scaling strategies: vertical scaling and horizontal
scaling.

### Vertical Scaling

Vertical scaling increases the resources of a single server. The service can
run more application workers instead of the initial two-worker configuration,
but the appropriate number of workers must be determined through load tests
and monitoring rather than selected arbitrarily. The tests should measure CPU,
RAM, request latency, throughput, database connections, and error rates.

The results can then guide the required increase in CPU and RAM. This approach
is simple to operate, but the service itself remains a single point of
failure if its only running instance becomes unavailable. A single instance
may also eventually reach hardware, connection, or network limits.

### Horizontal Scaling

Horizontal scaling adds multiple servers or service instances and distributes
traffic between them, typically through a load balancer. Instances should be
stateless so requests can be routed to any healthy server. This approach
provides better failover and redundancy and is generally the stronger
long-term option for 10,000 sensors, but it costs more and introduces extra
operational complexity.

The database must also support concurrent writes and high write throughput.
For production, the SQLite database used by this example should be replaced
with a production database such as PostgreSQL. A message broker or ingestion
queue can also absorb short traffic spikes and allow workers to process
readings asynchronously.

### Mixed Approach

A practical intermediate solution is to use one moderately sized server and
run multiple replicas of the service container on that server. A reverse
proxy or load balancer can distribute requests between the replicas.

This improves worker utilization and provides limited process-level
redundancy without immediately requiring multiple servers. The server remains
the infrastructure host, while the replicated containers reduce the risk of
the service itself being unavailable because one container or worker fails.

The final architecture should be selected using realistic load tests for
10,000 readings per second. Worker count, server size, database capacity, and
the number of replicas should all be based on measured throughput and latency
targets.

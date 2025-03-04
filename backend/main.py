from dishka.integrations.fastapi import setup_dishka
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.api.dependency.setup import setup_container
from backend.api.v1.routers import v1_router
from backend.core.clients.smtp_clients import SMTPClients
from backend.core.clients.redis_client import RedisClient
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


async def lifespan(app: FastAPI):
    app.state.db_connection = await DatabaseConnection()()
    app.state.redis_client = RedisClient()
    app.smtp_clients = SMTPClients()
    yield


app = FastAPI(lifespan=lifespan)


origins = ["http://localhost:5173", "https://www.fasttaski.ru", "https://fasttaski.ru"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, prefix="/api")
setup_dishka(setup_container(), app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        errors = []
        for error in exc.errors():
            field = error["loc"]
            input = error["input"]
            message = error["msg"]

            if isinstance(input, dict):
                input = input.get(field[-1])

            errors.append(
                {
                    "location": " -> ".join(field),
                    "detail": message,
                    "input": input,
                }
            )
        return JSONResponse(content=errors, status_code=422)
    except TypeError:
        return JSONResponse(
            status_code=422, content={"detail": exc.errors()}
        )

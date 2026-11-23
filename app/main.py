
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.api.websocket import websocket_router
from app.database.db import Base, engine
from app.database import models
from app.ingestion.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    start_scheduler()

    print("Finosauras application started!")

    yield

    stop_scheduler()

    print("Finosauras application stopped!")


app = FastAPI(
    title="Finosauras Concall Intelligence",
    description="AI-powered Concall Transcript Analysis",
    version="1.0",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "Finosauras AI Pipeline is running!",
        "status": "Success",
        "dashboard": "/dashboard"
    }


@app.get("/health")
def health():
    return {"status": "Healthy"}


app.include_router(router)
app.include_router(websocket_router)

app.mount(
    "/dashboard",
    StaticFiles(directory="app/static", html=True),
    name="dashboard"
)

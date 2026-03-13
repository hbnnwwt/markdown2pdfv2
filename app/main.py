"""FastAPI application entry point."""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import api
from app.deps import init_services, get_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    init_services()

    cleanup_task = asyncio.create_task(periodic_cleanup())

    yield

    cleanup_task.cancel()


async def periodic_cleanup():
    """Periodically clean up expired files."""
    while True:
        await asyncio.sleep(3600)
        storage = get_storage()
        if storage:
            count = storage.cleanup_expired()
            print(f"Cleaned up {count} expired files")


app = FastAPI(
    title="Markdown to PDF Converter",
    description="Convert Markdown documents to PDF with multiple themes",
    version="1.0.0",
    lifespan=lifespan,
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(api.router)

"""Application dependencies."""
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.services.storage import StorageService

# Global instances
storage_service: StorageService | None = None
templates: Jinja2Templates | None = None


def init_services():
    """Initialize global services."""
    global storage_service, templates

    storage_dir = Path(__file__).parent.parent / "temp"
    storage_service = StorageService(storage_dir, expire_hours=24)
    templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def get_storage() -> StorageService:
    """Get storage service instance."""
    if storage_service is None:
        raise RuntimeError("Storage service not initialized")
    return storage_service


def get_templates() -> Jinja2Templates:
    """Get templates instance."""
    if templates is None:
        raise RuntimeError("Templates not initialized")
    return templates

"""API routes for Markdown to PDF conversion."""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel

from app.deps import get_storage, get_templates
from app.services.converter import MarkdownConverter, ThemeType, THEMES

router = APIRouter()

# Converter instance
converter = MarkdownConverter()


class PreviewRequest(BaseModel):
    """Request model for preview."""
    markdown: str


class ConvertRequest(BaseModel):
    """Request model for conversion."""
    markdown: str
    theme: ThemeType = "default"
    filename: Optional[str] = None


class HistoryItem(BaseModel):
    """Response model for history item."""
    file_id: str
    original_name: str
    theme: str
    created_at: str
    expires_at: str
    file_size: int
    remaining_hours: float


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render main page."""
    return get_templates().TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/api/preview")
async def preview(request: PreviewRequest):
    """Preview markdown as HTML."""
    try:
        html_content = converter.to_html(request.markdown)
        return {"success": True, "html": html_content}
    except Exception as e:
        return {"success": False, "detail": str(e)}


@router.post("/api/convert")
async def convert(request: ConvertRequest):
    """Convert markdown to PDF."""
    try:
        pdf_bytes = converter.to_pdf(
            markdown_text=request.markdown,
            theme=request.theme,
            title=request.filename or "Document",
        )

        filename = request.filename or "document.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        record = get_storage().save(
            content=pdf_bytes,
            original_name=filename,
            theme=request.theme,
        )

        return {
            "success": True,
            "file_id": record.file_id,
            "download_url": f"/api/download/{record.file_id}",
            "filename": record.original_name,
            "file_size": record.file_size,
            "expires_at": record.expires_at.isoformat(),
        }
    except Exception as e:
        return {"success": False, "detail": str(e)}


@router.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    """Upload markdown file and return its content."""
    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed")

    try:
        content = await file.read()
        markdown_text = content.decode("utf-8")
        return {"success": True, "markdown": markdown_text, "filename": file.filename}
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/download/{file_id}")
async def download(file_id: str):
    """Download generated PDF file."""
    result = get_storage().get(file_id)
    if not result:
        raise HTTPException(status_code=404, detail="File not found or expired")

    pdf_bytes, record = result

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{record.original_name}"'
        },
    )


@router.get("/api/history")
async def history():
    """Get conversion history."""
    from datetime import datetime

    records = get_storage().list_recent(limit=20)

    items = []
    for r in records:
        remaining = (r.expires_at - datetime.now()).total_seconds() / 3600
        items.append(HistoryItem(
            file_id=r.file_id,
            original_name=r.original_name,
            theme=r.theme,
            created_at=r.created_at.isoformat(),
            expires_at=r.expires_at.isoformat(),
            file_size=r.file_size,
            remaining_hours=round(remaining, 1),
        ))

    return {"success": True, "items": items}

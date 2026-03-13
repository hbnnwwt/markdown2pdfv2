"""File storage service for temporary PDF files."""
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class FileRecord:
    """Record of a stored file."""
    file_id: str
    filename: str
    original_name: str
    created_at: datetime
    expires_at: datetime
    file_size: int
    theme: str = "default"


class StorageService:
    """Service for managing temporary file storage."""

    def __init__(self, storage_dir: Path, expire_hours: int = 24):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.expire_hours = expire_hours
        self._records: dict[str, FileRecord] = {}

    def save(self, content: bytes, original_name: str, theme: str = "default") -> FileRecord:
        """Save file content and return record."""
        file_id = self._generate_id()
        filename = f"{file_id}.pdf"
        file_path = self.storage_dir / filename

        # 写入文件
        file_path.write_bytes(content)

        # 创建记录
        now = datetime.now()
        record = FileRecord(
            file_id=file_id,
            filename=filename,
            original_name=original_name,
            created_at=now,
            expires_at=now + timedelta(hours=self.expire_hours),
            file_size=len(content),
            theme=theme,
        )
        self._records[file_id] = record

        return record

    def get(self, file_id: str) -> Optional[tuple[bytes, FileRecord]]:
        """Get file content and record by ID."""
        record = self._records.get(file_id)
        if not record:
            return None

        # 检查是否过期
        if datetime.now() > record.expires_at:
            self.delete(file_id)
            return None

        file_path = self.storage_dir / record.filename
        if not file_path.exists():
            return None

        return file_path.read_bytes(), record

    def delete(self, file_id: str) -> bool:
        """Delete file and record."""
        record = self._records.pop(file_id, None)
        if not record:
            return False

        file_path = self.storage_dir / record.filename
        if file_path.exists():
            file_path.unlink()

        return True

    def list_recent(self, limit: int = 20) -> list[FileRecord]:
        """List recent files."""
        now = datetime.now()
        # 过滤过期文件并按创建时间排序
        valid_records = [
            r for r in self._records.values()
            if r.expires_at > now
        ]
        sorted_records = sorted(valid_records, key=lambda r: r.created_at, reverse=True)
        return sorted_records[:limit]

    def cleanup_expired(self) -> int:
        """Remove expired files and return count."""
        now = datetime.now()
        expired_ids = [
            fid for fid, record in self._records.items()
            if record.expires_at <= now
        ]

        for file_id in expired_ids:
            self.delete(file_id)

        return len(expired_ids)

    def _generate_id(self) -> str:
        """Generate unique file ID."""
        return uuid.uuid4().hex[:12]

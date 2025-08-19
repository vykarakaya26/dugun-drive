from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileInfo(BaseModel):
    """File information model"""
    id: str
    name: str
    mime_type: str
    size: Optional[int] = None
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    web_view_link: Optional[str] = None
    download_link: Optional[str] = None

class UploadResponse(BaseModel):
    """Upload response model"""
    success: bool
    file_id: Optional[str] = None
    file_name: Optional[str] = None
    message: str

class FileListResponse(BaseModel):
    """File list response model"""
    files: List[FileInfo]
    next_page_token: Optional[str] = None
    total_count: int

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    status_code: int 
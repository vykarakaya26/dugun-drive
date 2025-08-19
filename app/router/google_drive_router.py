from fastapi import APIRouter, HTTPException, UploadFile, File, Query, Depends
from fastapi.responses import StreamingResponse
from typing import Optional
import io

from app.manager.google_drive_manager import GoogleDriveManager
from app.core.models import (
    FileInfo, 
    UploadResponse, 
    FileListResponse, 
    ErrorResponse
)
from app.core.exceptions import GoogleDriveException

router = APIRouter(prefix="/api/v1/drive", tags=["Google Drive"])

def get_drive_manager() -> GoogleDriveManager:
    """Dependency injection for Google Drive Manager"""
    return GoogleDriveManager()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """Upload file to Google Drive"""
    try:
        file_content = await file.read()
        response = drive_manager.upload_file(
            file_content=file_content,
            file_name=file.filename,
            mime_type=file.content_type
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files", response_model=FileListResponse)
async def list_files(
    page_size: int = Query(10, ge=1, le=100),
    page_token: Optional[str] = Query(None),
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """List files in Google Drive"""
    try:
        return drive_manager.list_files(page_size=page_size, page_token=page_token)
    except GoogleDriveException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/files/{file_id}", response_model=FileInfo)
async def get_file_info(
    file_id: str,
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """Get file information by ID"""
    try:
        file_info = drive_manager.get_file_info(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        return file_info
    except GoogleDriveException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """Delete file from Google Drive"""
    try:
        success = drive_manager.delete_file(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        return {"message": "File deleted successfully"}
    except GoogleDriveException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/files/{file_id}/download")
async def download_file(
    file_id: str,
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """Download file from Google Drive"""
    try:
        file_content = drive_manager.download_file(file_id)
        if not file_content:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file info for filename
        file_info = drive_manager.get_file_info(file_id)
        filename = file_info.name if file_info else "download"
        
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except GoogleDriveException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/search", response_model=FileListResponse)
async def search_files(
    query: str = Query(..., min_length=1),
    page_size: int = Query(10, ge=1, le=100),
    drive_manager: GoogleDriveManager = Depends(get_drive_manager)
):
    """Search files in Google Drive"""
    try:
        return drive_manager.search_files(query=query, page_size=page_size)
    except GoogleDriveException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Google Drive API"} 
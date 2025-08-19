import os
import io
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.models import FileInfo
from app.core.exceptions import (
    AuthenticationException, 
    FileNotFoundException, 
    PermissionException, 
    UploadException
)

class MockGoogleDriveService:
    """Mock service for testing without Google Drive API"""
    
    def __init__(self):
        self.files = {}
        self._create_sample_files()
    
    def _create_sample_files(self):
        """Create sample files for testing"""
        sample_files = [
            {
                'id': '1',
                'name': 'Örnek Resim.jpg',
                'mime_type': 'image/jpeg',
                'size': 1024000,
                'created_time': '2024-01-15T10:30:00Z',
                'modified_time': '2024-01-15T10:30:00Z',
                'web_view_link': 'https://drive.google.com/file/d/1/view'
            },
            {
                'id': '2',
                'name': 'Rapor.pdf',
                'mime_type': 'application/pdf',
                'size': 2048000,
                'created_time': '2024-01-14T14:20:00Z',
                'modified_time': '2024-01-14T14:20:00Z',
                'web_view_link': 'https://drive.google.com/file/d/2/view'
            },
            {
                'id': '3',
                'name': 'Video.mp4',
                'mime_type': 'video/mp4',
                'size': 15728640,
                'created_time': '2024-01-13T09:15:00Z',
                'modified_time': '2024-01-13T09:15:00Z',
                'web_view_link': 'https://drive.google.com/file/d/3/view'
            },
            {
                'id': '4',
                'name': 'Doküman.docx',
                'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'size': 512000,
                'created_time': '2024-01-12T16:45:00Z',
                'modified_time': '2024-01-12T16:45:00Z',
                'web_view_link': 'https://drive.google.com/file/d/4/view'
            }
        ]
        
        for file_data in sample_files:
            self.files[file_data['id']] = FileInfo(**file_data)
    
    def upload_file(self, file_content: bytes, file_name: str, mime_type: str = None) -> str:
        """Upload file to mock Google Drive"""
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        file_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + 'Z'
        
        self.files[file_id] = FileInfo(
            id=file_id,
            name=file_name,
            mime_type=mime_type,
            size=len(file_content),
            created_time=now,
            modified_time=now,
            web_view_link=f'https://drive.google.com/file/d/{file_id}/view'
        )
        
        return file_id
    
    def get_file_info(self, file_id: str) -> FileInfo:
        """Get file information by ID"""
        if file_id not in self.files:
            raise FileNotFoundException(f"File not found: {file_id}")
        
        return self.files[file_id]
    
    def list_files(self, page_size: int = 10, page_token: str = None) -> tuple[List[FileInfo], str]:
        """List files in mock Google Drive"""
        files_list = list(self.files.values())
        
        # Simple pagination
        start = 0
        if page_token:
            try:
                start = int(page_token)
            except ValueError:
                start = 0
        
        end = start + page_size
        page_files = files_list[start:end]
        
        next_page_token = str(end) if end < len(files_list) else None
        
        return page_files, next_page_token
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file from mock Google Drive"""
        if file_id not in self.files:
            raise FileNotFoundException(f"File not found: {file_id}")
        
        del self.files[file_id]
        return True
    
    def download_file(self, file_id: str) -> bytes:
        """Download file from mock Google Drive"""
        if file_id not in self.files:
            raise FileNotFoundException(f"File not found: {file_id}")
        
        # Return mock file content
        file_info = self.files[file_id]
        return f"Mock content for {file_info.name}".encode('utf-8') 
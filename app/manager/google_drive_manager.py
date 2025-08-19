from typing import List, Optional
import os
from app.service.google_drive_service import GoogleDriveService
from app.service.mock_drive_service import MockGoogleDriveService
from app.core.models import FileInfo, UploadResponse, FileListResponse
from app.core.exceptions import (
    GoogleDriveException,
    AuthenticationException,
    FileNotFoundException,
    PermissionException,
    UploadException
)

class GoogleDriveManager:
    """Manager for Google Drive operations"""
    
    def __init__(self):
        # Check if credentials file exists, use mock service if not
        if os.path.exists('credentials.json'):
            try:
                self.drive_service = GoogleDriveService()
            except Exception:
                print("Warning: Using mock service due to authentication issues")
                self.drive_service = MockGoogleDriveService()
        else:
            print("Info: Using mock service (no credentials.json found)")
            self.drive_service = MockGoogleDriveService()
    
    def upload_file(self, file_content: bytes, file_name: str, mime_type: str = None) -> UploadResponse:
        """Upload file to Google Drive"""
        try:
            file_id = self.drive_service.upload_file(file_content, file_name, mime_type)
            
            return UploadResponse(
                success=True,
                file_id=file_id,
                file_name=file_name,
                message="File uploaded successfully"
            )
            
        except UploadException as e:
            return UploadResponse(
                success=False,
                message=f"Upload failed: {str(e)}"
            )
        except AuthenticationException as e:
            return UploadResponse(
                success=False,
                message=f"Authentication failed: {str(e)}"
            )
        except Exception as e:
            return UploadResponse(
                success=False,
                message=f"Unexpected error: {str(e)}"
            )
    
    def get_file_info(self, file_id: str) -> Optional[FileInfo]:
        """Get file information by ID"""
        try:
            return self.drive_service.get_file_info(file_id)
        except FileNotFoundException:
            return None
        except Exception as e:
            raise GoogleDriveException(f"Error getting file info: {str(e)}")
    
    def list_files(self, page_size: int = 10, page_token: str = None) -> FileListResponse:
        """List files in Google Drive"""
        try:
            files, next_page_token = self.drive_service.list_files(page_size, page_token)
            
            return FileListResponse(
                files=files,
                next_page_token=next_page_token,
                total_count=len(files)
            )
            
        except Exception as e:
            raise GoogleDriveException(f"Error listing files: {str(e)}")
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file from Google Drive"""
        try:
            return self.drive_service.delete_file(file_id)
        except FileNotFoundException:
            return False
        except Exception as e:
            raise GoogleDriveException(f"Error deleting file: {str(e)}")
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download file from Google Drive"""
        try:
            return self.drive_service.download_file(file_id)
        except FileNotFoundException:
            return None
        except Exception as e:
            raise GoogleDriveException(f"Error downloading file: {str(e)}")
    
    def search_files(self, query: str, page_size: int = 10) -> FileListResponse:
        """Search files in Google Drive"""
        try:
            # This would need to be implemented in the service layer
            # For now, we'll use the list_files method
            files, next_page_token = self.drive_service.list_files(page_size)
            
            # Filter files based on query (simple name matching)
            filtered_files = [
                file for file in files 
                if query.lower() in file.name.lower()
            ]
            
            return FileListResponse(
                files=filtered_files,
                next_page_token=next_page_token,
                total_count=len(filtered_files)
            )
            
        except Exception as e:
            raise GoogleDriveException(f"Error searching files: {str(e)}") 
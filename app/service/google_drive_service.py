import os
import io
from typing import List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException, 
    FileNotFoundException, 
    PermissionException, 
    UploadException
)
from app.core.models import FileInfo

class GoogleDriveService:
    """Service for Google Drive operations"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    def __init__(self):
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API. Prefer service account if provided."""
        creds = None
        
        # Prefer service account if the credentials.json is a service account key
        if os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
            try:
                creds = ServiceAccountCredentials.from_service_account_file(
                    settings.GOOGLE_CREDENTIALS_FILE,
                    scopes=self.SCOPES
                )
                self.service = build('drive', 'v3', credentials=creds)
                return
            except Exception:
                # Not a service account file; continue with user OAuth flows
                pass

        # Fallback: user OAuth (requires token.json; not suitable for headless prod)
        if os.path.exists(settings.GOOGLE_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                settings.GOOGLE_TOKEN_FILE, self.SCOPES
            )
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise AuthenticationException(
                    "OAuth token not found or invalid in server environment. Provide a Google service account key in credentials.json."
                )
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def _ensure_public_permission(self, file_id: str) -> None:
        """Ensure the given file/folder is publicly readable via link."""
        try:
            self.service.permissions().create(
                fileId=file_id,
                body={
                    'type': 'anyone',
                    'role': 'reader',
                },
                fields='id'
            ).execute()
        except HttpError as error:
            # Ignore if permission already exists or forbidden by policy
            if getattr(error, 'resp', None) and getattr(error.resp, 'status', None) in (400, 403):
                return
            raise

    def _get_or_create_folder(self, folder_name: str = "Düğün Anıları") -> str:
        """Get or create a folder for wedding memories"""
        try:
            # Search for existing folder
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id,name)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            
            # Create new folder if not exists
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name'
            ).execute()
            
            folder_id = folder.get('id')
            # Make folder public to allow viewing with link
            if folder_id:
                self._ensure_public_permission(folder_id)
            return folder_id
            
        except HttpError as error:
            print(f"Error creating folder: {error}")
            return None

    def upload_file(self, file_content: bytes, file_name: str, mime_type: str = None) -> str:
        """Upload file to Google Drive"""
        try:
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Get or create wedding folder
            folder_id = self._get_or_create_folder()
            
            file_metadata = {
                'name': file_name,
                'parents': [folder_id] if folder_id else []
            }
            
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            file_id = file.get('id')
            # Ensure the uploaded file is viewable via link (inherits from folder, but set explicitly too)
            if file_id:
                try:
                    self._ensure_public_permission(file_id)
                except Exception:
                    # Non-fatal if we cannot set file permission
                    pass
            return file_id
            
        except HttpError as error:
            if error.resp.status == 403:
                raise PermissionException("Permission denied for upload")
            elif error.resp.status == 400:
                raise UploadException("Invalid upload request")
            else:
                raise UploadException(f"Upload failed: {error}")

    def get_folder_link(self) -> Optional[str]:
        """Return the public web link for the wedding folder."""
        try:
            folder_id = self._get_or_create_folder()
            if not folder_id:
                return None
            # Ensure public permission (idempotent)
            self._ensure_public_permission(folder_id)
            return f"https://drive.google.com/drive/folders/{folder_id}"
        except Exception:
            return None
    
    def get_file_info(self, file_id: str) -> FileInfo:
        """Get file information by ID"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id,name,mimeType,size,createdTime,modifiedTime,webViewLink'
            ).execute()
            
            return FileInfo(
                id=file.get('id'),
                name=file.get('name'),
                mime_type=file.get('mimeType'),
                size=int(file.get('size', 0)) if file.get('size') else None,
                created_time=file.get('createdTime'),
                modified_time=file.get('modifiedTime'),
                web_view_link=file.get('webViewLink')
            )
            
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundException(f"File not found: {file_id}")
            elif error.resp.status == 403:
                raise PermissionException("Permission denied")
            else:
                raise FileNotFoundException(f"Error getting file info: {error}")
    
    def list_files(self, page_size: int = 10, page_token: str = None) -> tuple[List[FileInfo], str]:
        """List files in Google Drive"""
        try:
            # Get wedding folder
            folder_id = self._get_or_create_folder()
            
            # Query for files in the wedding folder
            query = f"'{folder_id}' in parents and trashed=false" if folder_id else "trashed=false"
            
            results = self.service.files().list(
                pageSize=page_size,
                pageToken=page_token,
                q=query,
                fields="nextPageToken, files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink)"
            ).execute()
            
            files = []
            for file in results.get('files', []):
                files.append(FileInfo(
                    id=file.get('id'),
                    name=file.get('name'),
                    mime_type=file.get('mimeType'),
                    size=int(file.get('size', 0)) if file.get('size') else None,
                    created_time=file.get('createdTime'),
                    modified_time=file.get('modifiedTime'),
                    web_view_link=file.get('webViewLink')
                ))
            
            return files, results.get('nextPageToken')
            
        except HttpError as error:
            if error.resp.status == 403:
                raise PermissionException("Permission denied")
            else:
                raise Exception(f"Error listing files: {error}")
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
            
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundException(f"File not found: {file_id}")
            elif error.resp.status == 403:
                raise PermissionException("Permission denied")
            else:
                raise Exception(f"Error deleting file: {error}")
    
    def download_file(self, file_id: str) -> bytes:
        """Download file from Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            return file.getvalue()
            
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundException(f"File not found: {file_id}")
            elif error.resp.status == 403:
                raise PermissionException("Permission denied")
            else:
                raise Exception(f"Error downloading file: {error}") 
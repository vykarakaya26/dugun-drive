class GoogleDriveException(Exception):
    """Base exception for Google Drive operations"""
    pass

class AuthenticationException(GoogleDriveException):
    """Exception raised for authentication errors"""
    pass

class FileNotFoundException(GoogleDriveException):
    """Exception raised when file is not found"""
    pass

class PermissionException(GoogleDriveException):
    """Exception raised for permission errors"""
    pass

class UploadException(GoogleDriveException):
    """Exception raised for upload errors"""
    pass 
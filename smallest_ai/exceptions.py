class TTSError(Exception):
    """Base exception for TTS SDK"""
    pass

class APIError(TTSError):
    """Raised when the API returns an error"""
    pass

class ValidationError(TTSError):
    """Raised when input validation fails"""
    pass

class AuthenticationError(TTSError):
    """Raised when authentication fails"""
    pass
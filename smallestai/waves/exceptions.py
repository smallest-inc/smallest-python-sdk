class TTSError(Exception):
    """Base exception for TTS SDK"""
    default_message = "API key is required. Please set the `SMALLEST_API_KEY` environment variable or visit https://waves.smallest.ai/ to obtain your API key."
    
    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class APIError(TTSError):
    """Raised when the API returns an error"""
    pass

class ValidationError(TTSError):
    """Raised when input validation fails"""
    pass

class AuthenticationError(TTSError):
    """Raised when authentication fails"""
    pass
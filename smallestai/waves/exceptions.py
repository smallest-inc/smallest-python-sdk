class InvalidError(Exception):
    """Base exception for TTS SDK"""
    default_message = "API key is required. Please set the `SMALLEST_API_KEY` environment variable or visit https://waves.smallest.ai/ to obtain your API key."
    
    def __init__(self, message=None):
        super().__init__(message or self.default_message)

class APIError(InvalidError):
    """Raised when the API returns an error"""
    pass

class ValidationError(InvalidError):
    """Raised when input validation fails"""
    pass

class AuthenticationError(InvalidError):
    """Raised when authentication fails"""
    pass
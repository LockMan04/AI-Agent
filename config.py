"""
Configuration settings for Meeting Preparation System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    # Model settings
    MODEL_NAME = "gpt-4o-mini"
    MODEL_TEMPERATURE = 0.7
    
    # Meeting settings
    MIN_MEETING_DURATION = 15
    MAX_MEETING_DURATION = 180
    DEFAULT_MEETING_DURATION = 60
    MEETING_DURATION_STEP = 15
    
    # File settings
    MAX_HISTORY_FILES = 5
    FILE_ENCODING = 'utf-8'
    
    # UI settings
    PAGE_TITLE = "Lên lịch cuộc họp với AI"
    PAGE_LAYOUT = "wide"
    
    @classmethod
    def validate_api_keys(cls):
        """
        Kiểm tra tính hợp lệ của API keys
        
        Returns:
            bool: True nếu tất cả API keys đều có
        """
        return bool(cls.OPENAI_API_KEY and cls.SERPER_API_KEY)
    
    @classmethod
    def set_environment_variables(cls):
        """
        Thiết lập environment variables
        """
        if cls.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = cls.OPENAI_API_KEY
        if cls.SERPER_API_KEY:
            os.environ["SERPER_API_KEY"] = cls.SERPER_API_KEY

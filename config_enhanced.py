"""
Enhanced Configuration settings for Meeting Preparation System
"""
import os
import streamlit as st
from dotenv import load_dotenv
from typing import List, Optional
import sys

# Load environment variables
load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors"""
    pass

class Config:
    """Enhanced configuration class for the application"""
    
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
    MAX_ATTENDEES = 20
    MIN_ATTENDEES = 1
    
    # File settings
    MAX_HISTORY_FILES = 5
    FILE_ENCODING = 'utf-8'
    REPORTS_DIR = "reports"
    MAX_FILE_SIZE_MB = 10
    
    # UI settings
    PAGE_TITLE = "🤖 AI Agent - Meeting Scheduler"
    PAGE_LAYOUT = "wide"
    
    # Security settings
    ALLOWED_FILE_EXTENSIONS = ['.md', '.txt', '.json']
    MAX_COMPANY_NAME_LENGTH = 100
    MAX_OBJECTIVE_LENGTH = 500
    MAX_FOCUS_AREAS_LENGTH = 300
    
    @classmethod
    def validate_api_keys(cls) -> bool:
        """
        Validate that all required API keys are present
        
        Returns:
            bool: True if all keys are valid
            
        Raises:
            ConfigError: If any required API key is missing
        """
        missing_keys = []
        
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY.strip() == "":
            missing_keys.append("OPENAI_API_KEY")
        if not cls.SERPER_API_KEY or cls.SERPER_API_KEY.strip() == "":
            missing_keys.append("SERPER_API_KEY")
        
        if missing_keys:
            error_msg = f"Missing required API keys: {', '.join(missing_keys)}"
            st.error(f"❌ {error_msg}")
            st.markdown("""
            ### 🔧 Cách khắc phục:
            1. Tạo file `.env` trong thư mục gốc dự án
            2. Thêm các dòng sau vào file `.env`:
            ```
            OPENAI_API_KEY=your_openai_api_key_here
            SERPER_API_KEY=your_serper_api_key_here
            ```
            3. Restart ứng dụng Streamlit
            
            ### 📋 Cách lấy API Keys:
            - **OpenAI API Key**: https://platform.openai.com/api-keys
            - **Serper API Key**: https://serper.dev/api-key
            """)
            raise ConfigError(error_msg)
        
        return True
    
    @classmethod
    def set_environment_variables(cls):
        """Set API keys as environment variables for the session"""
        try:
            if cls.OPENAI_API_KEY:
                os.environ["OPENAI_API_KEY"] = cls.OPENAI_API_KEY
            if cls.SERPER_API_KEY:
                os.environ["SERPER_API_KEY"] = cls.SERPER_API_KEY
        except Exception as e:
            raise ConfigError(f"Failed to set environment variables: {e}")
    
    @classmethod
    def get_safe_model_config(cls) -> dict:
        """
        Get model configuration with safe defaults
        
        Returns:
            dict: Model configuration
        """
        return {
            "model": cls.MODEL_NAME,
            "temperature": max(0.0, min(1.0, cls.MODEL_TEMPERATURE)),  # Clamp between 0-1
            "api_key": cls.OPENAI_API_KEY
        }
    
    @classmethod
    def validate_meeting_config(cls, duration: int, attendees_count: int) -> List[str]:
        """
        Validate meeting configuration parameters
        
        Args:
            duration: Meeting duration in minutes
            attendees_count: Number of attendees
            
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        errors = []
        
        if duration < cls.MIN_MEETING_DURATION:
            errors.append(f"Thời lượng cuộc họp phải ít nhất {cls.MIN_MEETING_DURATION} phút")
        elif duration > cls.MAX_MEETING_DURATION:
            errors.append(f"Thời lượng cuộc họp không nên quá {cls.MAX_MEETING_DURATION} phút")
        
        if attendees_count < cls.MIN_ATTENDEES:
            errors.append(f"Phải có ít nhất {cls.MIN_ATTENDEES} người tham gia")
        elif attendees_count > cls.MAX_ATTENDEES:
            errors.append(f"Không nên có quá {cls.MAX_ATTENDEES} người tham gia")
        
        return errors
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        try:
            os.makedirs(cls.REPORTS_DIR, exist_ok=True)
        except OSError as e:
            raise ConfigError(f"Cannot create reports directory: {e}")
    
    @classmethod
    def validate_input_lengths(cls, company_name: str, objective: str, focus_areas: str) -> List[str]:
        """
        Validate input field lengths for security
        
        Args:
            company_name: Company name
            objective: Meeting objective
            focus_areas: Focus areas
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        if len(company_name) > cls.MAX_COMPANY_NAME_LENGTH:
            errors.append(f"Tên công ty không được vượt quá {cls.MAX_COMPANY_NAME_LENGTH} ký tự")
        
        if len(objective) > cls.MAX_OBJECTIVE_LENGTH:
            errors.append(f"Mục đích cuộc họp không được vượt quá {cls.MAX_OBJECTIVE_LENGTH} ký tự")
        
        if len(focus_areas) > cls.MAX_FOCUS_AREAS_LENGTH:
            errors.append(f"Mục tiêu không được vượt quá {cls.MAX_FOCUS_AREAS_LENGTH} ký tự")
        
        return errors
    
    @classmethod
    def get_system_info(cls) -> dict:
        """Get system information for debugging"""
        return {
            "python_version": sys.version,
            "os_name": os.name,
            "current_dir": os.getcwd(),
            "reports_dir_exists": os.path.exists(cls.REPORTS_DIR),
            "env_file_exists": os.path.exists(".env"),
            "has_openai_key": bool(cls.OPENAI_API_KEY),
            "has_serper_key": bool(cls.SERPER_API_KEY),
            "streamlit_version": st.__version__ if hasattr(st, '__version__') else 'unknown'
        }
    
    @classmethod
    def display_system_status(cls):
        """Display system status in Streamlit sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🔧 System Status")
            
            try:
                system_info = cls.get_system_info()
                
                # API Keys status
                api_status = "✅" if cls.validate_api_keys() else "❌"
                st.markdown(f"**API Keys:** {api_status}")
                
                # Directories status
                dirs_status = "✅" if system_info['reports_dir_exists'] else "❌"
                st.markdown(f"**Directories:** {dirs_status}")
                
                # Environment file
                env_status = "✅" if system_info['env_file_exists'] else "⚠️"
                st.markdown(f"**Environment File:** {env_status}")
                
            except Exception as e:
                st.error(f"Error checking system status: {e}")

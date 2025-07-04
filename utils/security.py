"""
Security utilities for the Meeting Preparation System
"""
import re
import hashlib
import secrets
import os
from typing import Optional, List
import streamlit as st


class SecurityValidator:
    """Security validation utilities"""
    
    # Patterns for potentially dangerous content
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript protocol
        r'on\w+\s*=',  # Event handlers
        r'<iframe[^>]*>.*?</iframe>',  # Iframes
        r'eval\s*\(',  # eval() function
        r'exec\s*\(',  # exec() function
    ]
    
    # Safe characters for filenames
    SAFE_FILENAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
    
    @classmethod
    def sanitize_input(cls, text: str, max_length: int = 1000) -> str:
        """
        Sanitize user input to prevent XSS and other attacks
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Limit length
        text = text[:max_length]
        
        # Remove dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Basic HTML entity encoding for display
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text.strip()
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Create a safe filename from user input
        
        Args:
            filename: Original filename
            
        Returns:
            str: Safe filename
        """
        if not filename:
            return "unnamed_file"
        
        # Keep only safe characters
        safe_name = ''.join(c for c in filename if c in cls.SAFE_FILENAME_CHARS)
        
        # Remove multiple spaces and trim
        safe_name = re.sub(r'\s+', ' ', safe_name).strip()
        
        # Limit length
        if len(safe_name) > 50:
            safe_name = safe_name[:50].rstrip()
        
        # Ensure not empty
        if not safe_name:
            safe_name = "unnamed_file"
        
        # Avoid reserved names
        reserved_names = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'lpt1', 'lpt2']
        if safe_name.lower() in reserved_names:
            safe_name = f"file_{safe_name}"
        
        return safe_name
    
    @classmethod
    def validate_file_path(cls, filepath: str) -> bool:
        """
        Validate that a file path is safe
        
        Args:
            filepath: File path to validate
            
        Returns:
            bool: True if path is safe
        """
        if not filepath:
            return False
        
        # Normalize path
        normalized = os.path.normpath(filepath)
        
        # Check for path traversal attempts
        if '..' in normalized or normalized.startswith('/'):
            return False
        
        # Check for absolute paths on Windows
        if os.path.isabs(normalized):
            return False
        
        # Ensure path stays within project directory
        try:
            full_path = os.path.abspath(normalized)
            project_root = os.path.abspath('.')
            return full_path.startswith(project_root)
        except (OSError, ValueError):
            return False
    
    @classmethod
    def generate_secure_token(cls, length: int = 32) -> str:
        """
        Generate a cryptographically secure token
        
        Args:
            length: Token length
            
        Returns:
            str: Secure token
        """
        return secrets.token_urlsafe(length)
    
    @classmethod
    def hash_sensitive_data(cls, data: str) -> str:
        """
        Hash sensitive data for logging/storage
        
        Args:
            data: Sensitive data to hash
            
        Returns:
            str: SHA256 hash
        """
        return hashlib.sha256(data.encode()).hexdigest()[:16]  # First 16 chars
    
    @classmethod
    def validate_email_format(cls, email: str) -> bool:
        """
        Validate email format with security considerations
        
        Args:
            email: Email to validate
            
        Returns:
            bool: True if email format is valid and safe
        """
        if not email or len(email) > 254:  # RFC limit
            return False
        
        # Basic email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False
        
        # Additional security checks
        if '..' in email or email.startswith('.') or email.endswith('.'):
            return False
        
        return True
    
    @classmethod
    def check_rate_limit(cls, session_key: str, max_requests: int = 10, time_window: int = 60) -> bool:
        """
        Simple rate limiting check using Streamlit session state
        
        Args:
            session_key: Unique key for this rate limit check
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
            
        Returns:
            bool: True if under rate limit
        """
        import time
        
        current_time = time.time()
        
        if session_key not in st.session_state:
            st.session_state[session_key] = []
        
        # Clean old requests
        requests = st.session_state[session_key]
        st.session_state[session_key] = [req_time for req_time in requests 
                                       if current_time - req_time < time_window]
        
        # Check if under limit
        if len(st.session_state[session_key]) >= max_requests:
            return False
        
        # Add current request
        st.session_state[session_key].append(current_time)
        return True


class InputValidator:
    """Enhanced input validation with security focus"""
    
    @classmethod
    def validate_company_name(cls, name: str) -> List[str]:
        """
        Validate company name with security checks
        
        Args:
            name: Company name to validate
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        if not name:
            errors.append("Tên công ty không được để trống")
            return errors
        
        # Length check
        if len(name) < 2:
            errors.append("Tên công ty phải có ít nhất 2 ký tự")
        elif len(name) > 100:
            errors.append("Tên công ty không được quá 100 ký tự")
        
        # Character validation
        if not re.match(r'^[a-zA-Z0-9\s\-&.,()]+$', name):
            errors.append("Tên công ty chứa ký tự không hợp lệ")
        
        # Check for suspicious patterns
        suspicious_patterns = ['<', '>', 'script', 'javascript', 'eval', 'exec']
        if any(pattern in name.lower() for pattern in suspicious_patterns):
            errors.append("Tên công ty chứa nội dung không được phép")
        
        return errors
    
    @classmethod
    def validate_meeting_objective(cls, objective: str) -> List[str]:
        """
        Validate meeting objective with security checks
        
        Args:
            objective: Meeting objective to validate
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        if not objective:
            errors.append("Mục đích cuộc họp không được để trống")
            return errors
        
        # Length check
        if len(objective) < 10:
            errors.append("Mục đích cuộc họp phải có ít nhất 10 ký tự")
        elif len(objective) > 500:
            errors.append("Mục đích cuộc họp không được quá 500 ký tự")
        
        # Security check
        sanitized = SecurityValidator.sanitize_input(objective)
        if len(sanitized) != len(objective):
            errors.append("Mục đích cuộc họp chứa nội dung không an toàn")
        
        return errors
    
    @classmethod
    def validate_attendees_list(cls, attendees: str) -> List[str]:
        """
        Validate attendees list with security checks
        
        Args:
            attendees: Attendees list to validate
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        if not attendees:
            errors.append("Danh sách người tham gia không được để trống")
            return errors
        
        attendee_lines = [line.strip() for line in attendees.split('\n') if line.strip()]
        
        if len(attendee_lines) == 0:
            errors.append("Cần có ít nhất 1 người tham gia")
        elif len(attendee_lines) > 20:
            errors.append("Không được có quá 20 người tham gia")
        
        # Validate each attendee
        for i, attendee in enumerate(attendee_lines, 1):
            if len(attendee) > 100:
                errors.append(f"Thông tin người tham gia {i} quá dài (max 100 ký tự)")
            
            # Security check
            sanitized = SecurityValidator.sanitize_input(attendee)
            if len(sanitized) != len(attendee):
                errors.append(f"Thông tin người tham gia {i} chứa nội dung không an toàn")
        
        return errors


def log_security_event(event_type: str, details: str, user_hash: Optional[str] = None):
    """
    Log security events for monitoring
    
    Args:
        event_type: Type of security event
        details: Event details
        user_hash: Hashed user identifier
    """
    try:
        import datetime
        
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] SECURITY {event_type}: {details}"
        
        if user_hash:
            log_entry += f" (User: {user_hash})"
        
        # In production, this should go to a proper logging system
        print(log_entry)  # For now, just print
        
    except Exception:
        pass  # Don't let logging errors break the app

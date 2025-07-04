"""
Input validation utilities
"""
import re
import streamlit as st
from typing import Tuple, List


def validate_inputs(company_name, meeting_objective, attendees, focus_areas) -> bool:
    """
    Kiểm tra tính hợp lệ của inputs
    
    Args:
        company_name (str): Tên công ty
        meeting_objective (str): Mục đích cuộc họp
        attendees (str): Danh sách người tham gia
        focus_areas (str): Các lĩnh vực tập trung
        
    Returns:
        bool: True nếu tất cả inputs hợp lệ
    """
    errors = []
    
    # Validate company name
    if not company_name or not company_name.strip():
        errors.append("Tên công ty không được để trống")
    elif len(company_name.strip()) < 2:
        errors.append("Tên công ty phải có ít nhất 2 ký tự")
    elif len(company_name.strip()) > 100:
        errors.append("Tên công ty không được quá 100 ký tự")
    
    # Validate meeting objective
    if not meeting_objective or not meeting_objective.strip():
        errors.append("Mục đích cuộc họp không được để trống")
    elif len(meeting_objective.strip()) < 10:
        errors.append("Mục đích cuộc họp phải có ít nhất 10 ký tự")
    elif len(meeting_objective.strip()) > 500:
        errors.append("Mục đích cuộc họp không được quá 500 ký tự")
    
    # Validate attendees
    if not attendees or not attendees.strip():
        errors.append("Danh sách người tham gia không được để trống")
    else:
        attendee_list = [line.strip() for line in attendees.split('\n') if line.strip()]
        if len(attendee_list) == 0:
            errors.append("Cần có ít nhất 1 người tham gia")
        elif len(attendee_list) > 20:
            errors.append("Không được có quá 20 người tham gia")
    
    # Validate focus areas
    if not focus_areas or not focus_areas.strip():
        errors.append("Các mục tiêu cần đạt được không được để trống")
    elif len(focus_areas.strip()) < 5:
        errors.append("Mục tiêu phải có ít nhất 5 ký tự")
    elif len(focus_areas.strip()) > 300:
        errors.append("Mục tiêu không được quá 300 ký tự")
    
    # Display errors
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return False
    
    return True


def validate_email(email: str) -> bool:
    """
    Kiểm tra tính hợp lệ của email
    
    Args:
        email (str): Email cần kiểm tra
        
    Returns:
        bool: True nếu email hợp lệ
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_filename(filename: str) -> str:
    """
    Làm sạch tên file để đảm bảo an toàn
    
    Args:
        filename (str): Tên file gốc
        
    Returns:
        str: Tên file đã được làm sạch
    """
    # Chỉ giữ lại các ký tự an toàn
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
    cleaned = "".join(c for c in filename if c in safe_chars)
    
    # Loại bỏ khoảng trắng thừa
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Giới hạn độ dài
    if len(cleaned) > 50:
        cleaned = cleaned[:50].rstrip()
    
    return cleaned or "unnamed"


def validate_meeting_duration(duration: int) -> Tuple[bool, str]:
    """
    Kiểm tra tính hợp lệ của thời lượng cuộc họp
    
    Args:
        duration (int): Thời lượng (phút)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if duration < 15:
        return False, "Thời lượng cuộc họp phải ít nhất 15 phút"
    elif duration > 180:
        return False, "Thời lượng cuộc họp không nên quá 3 giờ (180 phút)"
    elif duration % 15 != 0:
        return False, "Thời lượng cuộc họp nên là bội số của 15 phút"
    
    return True, ""


def parse_attendees(attendees_text: str) -> List[dict]:
    """
    Parse danh sách người tham gia thành structured data
    
    Args:
        attendees_text (str): Text chứa thông tin người tham gia
        
    Returns:
        list: Danh sách dict chứa thông tin người tham gia
    """
    attendees = []
    
    for line in attendees_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Try to parse format: "Name - Role" or "Name (Role)" or just "Name"
        if ' - ' in line:
            parts = line.split(' - ', 1)
            name = parts[0].strip()
            role = parts[1].strip()
        elif '(' in line and ')' in line:
            name = line.split('(')[0].strip()
            role = line.split('(')[1].split(')')[0].strip()
        else:
            name = line
            role = ""
            
        attendees.append({
            'name': name,
            'role': role,
            'email': ''  # Có thể mở rộng để extract email
        })
    
    return attendees

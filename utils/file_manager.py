"""
File management utilities
"""
import datetime
import os
import streamlit as st
from pathlib import Path


def save_meeting_result(result, company_name):
    """
    Lưu kết quả cuộc họp vào file
    
    Args:
        result: Kết quả từ AI agents
        company_name (str): Tên công ty
    
    Returns:
        str: Tên file đã lưu
    
    Raises:
        OSError: Nếu không thể tạo thư mục hoặc ghi file
    """
    try:
        # Tạo thư mục reports nếu chưa có
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        
        # Tạo tên file an toàn
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        filename = report_dir / f"meeting_prep_{safe_company_name}_{timestamp}.md"
        
        # Ghi file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Chuẩn bị cuộc họp - {company_name}\n")
            f.write(f"**Ngày tạo:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(str(result))
        
        return str(filename)
        
    except OSError as e:
        st.error(f"❌ Lỗi khi lưu file: {e}")
        return None


def create_download_button(filename, company_name):
    """
    Tạo button download file
    
    Args:
        filename (str): Đường dẫn file
        company_name (str): Tên công ty
    """
    try:
        if filename and os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            st.download_button(
                label="📥 Tải xuống báo cáo",
                data=content,
                file_name=f"meeting_prep_{company_name}_{datetime.datetime.now().strftime('%d%m%Y')}.md",
                mime="text/markdown"
            )
    except Exception as e:
        st.error(f"❌ Lỗi khi tạo download button: {e}")


def get_report_files(limit=5):
    """
    Lấy danh sách file báo cáo gần nhất
    
    Args:
        limit (int): Số lượng file tối đa
        
    Returns:
        list: Danh sách file paths
    """
    try:
        import glob
        pattern = os.path.join("reports", "meeting_prep_*.md")
        files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
        return files[:limit]
    except Exception as e:
        st.error(f"❌ Lỗi khi lấy danh sách file: {e}")
        return []


def clean_old_reports(max_files=10):
    """
    Dọn dẹp các file báo cáo cũ
    
    Args:
        max_files (int): Số file tối đa giữ lại
    """
    try:
        files = get_report_files(limit=100)  # Lấy tất cả
        if len(files) > max_files:
            for file_to_delete in files[max_files:]:
                os.remove(file_to_delete)
            st.info(f"🧹 Đã dọn dẹp {len(files) - max_files} file báo cáo cũ")
    except Exception as e:
        st.warning(f"⚠️ Lỗi khi dọn dẹp file: {e}")

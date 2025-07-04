"""
Dashboard and metrics utilities
"""
import streamlit as st
import glob
import os
from datetime import datetime, timedelta
from typing import Dict, List


def display_dashboard_metrics():
    """
    Hiển thị dashboard với metrics tổng quan
    """
    st.markdown("---")
    st.markdown("### 📊 Dashboard Tổng quan")
    
    try:
        # Lấy dữ liệu từ files
        report_files = glob.glob(os.path.join("reports", "meeting_prep_*.md"))
        
        if not report_files:
            st.info("📝 Chưa có dữ liệu để hiển thị dashboard")
            return
        
        # Phân tích dữ liệu
        total_meetings = len(report_files)
        recent_meetings = get_recent_meetings_count(report_files, days=7)
        companies = get_unique_companies(report_files)
        avg_prep_time = estimate_avg_prep_time(report_files)
        
        # Hiển thị metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Tổng cuộc họp",
                value=total_meetings,
                delta=f"+{recent_meetings} tuần này"
            )
        
        with col2:
            st.metric(
                label="🏢 Số công ty",
                value=len(companies),
                help="Số lượng công ty đã làm việc"
            )
        
        with col3:
            st.metric(
                label="⏱️ Thời gian chuẩn bị TB",
                value=f"{avg_prep_time} phút",
                help="Thời gian trung bình để chuẩn bị một cuộc họp"
            )
        
        with col4:
            success_rate = calculate_success_rate(report_files)
            st.metric(
                label="✅ Tỷ lệ thành công",
                value=f"{success_rate}%",
                help="Tỷ lệ cuộc họp được chuẩn bị thành công"
            )
        
        # Charts
        display_meeting_trends(report_files)
        display_company_distribution(companies)
        
    except Exception as e:
        st.error(f"❌ Lỗi khi hiển thị dashboard: {e}")


def get_recent_meetings_count(files: List[str], days: int = 7) -> int:
    """
    Đếm số cuộc họp trong N ngày gần đây
    
    Args:
        files: Danh sách file paths
        days: Số ngày để tính
        
    Returns:
        int: Số cuộc họp gần đây
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        count = 0
        
        for file in files:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file))
                if file_time >= cutoff_date:
                    count += 1
            except (OSError, ValueError):
                continue
                
        return count
        
    except Exception:
        return 0


def get_unique_companies(files: List[str]) -> List[str]:
    """
    Lấy danh sách công ty unique từ tên files
    
    Args:
        files: Danh sách file paths
        
    Returns:
        List[str]: Danh sách tên công ty
    """
    companies = set()
    
    for file in files:
        try:
            filename = os.path.basename(file)
            parts = filename.split('_')
            
            if len(parts) >= 3:
                company = parts[2]  # meeting_prep_{company}_{date}.md
                companies.add(company)
                
        except (IndexError, AttributeError):
            continue
    
    return list(companies)


def estimate_avg_prep_time(files: List[str]) -> int:
    """
    Ước tính thời gian chuẩn bị trung bình
    
    Args:
        files: Danh sách file paths
        
    Returns:
        int: Thời gian trung bình (phút)
    """
    # Đây là ước tính dựa trên độ phức tạp file
    # Trong thực tế có thể track thời gian thực
    
    try:
        total_complexity = 0
        valid_files = 0
        
        for file in files:
            try:
                file_size = os.path.getsize(file)
                # Ước tính: file lớn hơn = chuẩn bị lâu hơn
                complexity = min(file_size // 1000, 10)  # Max 10 points
                total_complexity += complexity
                valid_files += 1
                
            except OSError:
                continue
        
        if valid_files == 0:
            return 45  # Default estimate
        
        avg_complexity = total_complexity / valid_files
        estimated_time = int(30 + (avg_complexity * 5))  # 30-80 minutes range
        
        return estimated_time
        
    except Exception:
        return 45  # Default fallback


def calculate_success_rate(files: List[str]) -> int:
    """
    Tính tỷ lệ thành công dựa trên việc có file hay không
    
    Args:
        files: Danh sách file paths
        
    Returns:
        int: Tỷ lệ phần trăm
    """
    try:
        valid_files = 0
        
        for file in files:
            try:
                if os.path.exists(file) and os.path.getsize(file) > 100:  # Min file size
                    valid_files += 1
            except OSError:
                continue
        
        if len(files) == 0:
            return 100
            
        success_rate = int((valid_files / len(files)) * 100)
        return success_rate
        
    except Exception:
        return 100


def display_meeting_trends(files: List[str]):
    """
    Hiển thị xu hướng cuộc họp theo thời gian
    
    Args:
        files: Danh sách file paths
    """
    try:
        st.markdown("#### 📈 Xu hướng cuộc họp")
        
        # Group by date
        date_counts = {}
        
        for file in files:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file))
                date_key = file_time.strftime('%Y-%m-%d')
                date_counts[date_key] = date_counts.get(date_key, 0) + 1
                
            except (OSError, ValueError):
                continue
        
        if date_counts:
            # Simple text display (có thể dùng chart library sau)
            recent_dates = sorted(date_counts.keys())[-7:]  # Last 7 days
            
            cols = st.columns(len(recent_dates) if recent_dates else 1)
            
            for i, date in enumerate(recent_dates):
                if i < len(cols):
                    with cols[i]:
                        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m')
                        st.metric(formatted_date, date_counts[date])
        else:
            st.info("Chưa có dữ liệu xu hướng")
            
    except Exception as e:
        st.warning(f"⚠️ Không thể hiển thị xu hướng: {e}")


def display_company_distribution(companies: List[str]):
    """
    Hiển thị phân bố công ty
    
    Args:
        companies: Danh sách tên công ty
    """
    try:
        st.markdown("#### 🏢 Phân bố công ty")
        
        if companies:
            # Count company frequency
            company_counts = {}
            for company in companies:
                company_counts[company] = company_counts.get(company, 0) + 1
            
            # Sort by frequency
            sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Display top companies
            for company, count in sorted_companies[:5]:
                progress_value = count / max(company_counts.values()) if company_counts.values() else 0
                st.markdown(f"**{company}**: {count} cuộc họp")
                st.progress(progress_value)
        else:
            st.info("Chưa có dữ liệu công ty")
            
    except Exception as e:
        st.warning(f"⚠️ Không thể hiển thị phân bố công ty: {e}")


def display_system_health():
    """
    Hiển thị trạng thái hệ thống
    """
    st.markdown("---")
    st.markdown("### 🔧 Trạng thái hệ thống")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Check reports directory
        reports_exist = os.path.exists("reports")
        st.metric(
            "📁 Thư mục Reports", 
            "✅ OK" if reports_exist else "❌ Lỗi"
        )
    
    with col2:
        # Check config
        try:
            from ..config import Config
            api_keys_valid = Config.validate_api_keys()
            st.metric(
                "🔑 API Keys",
                "✅ OK" if api_keys_valid else "❌ Thiếu"
            )
        except:
            st.metric("🔑 API Keys", "❌ Lỗi")
    
    with col3:
        # Check disk space (simplified)
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free // (1024**3)
            st.metric(
                "💾 Dung lượng còn lại",
                f"{free_gb} GB"
            )
        except:
            st.metric("💾 Dung lượng", "❓ Không xác định")

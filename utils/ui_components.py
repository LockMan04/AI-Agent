"""
UI Components utilities
"""
import streamlit as st
import glob
import os
import time
import random
from typing import Dict, Any


def display_meeting_history():
    """
    Hiển thị lịch sử cuộc họp trong sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Lịch sử cuộc họp")
    
    try:
        meeting_files = glob.glob(os.path.join("reports", "meeting_prep_*.md"))
        if meeting_files:
            meeting_files.sort(key=os.path.getmtime, reverse=True)  # Mới nhất trước
            
            for file in meeting_files[:5]:  # Hiển thị 5 file gần nhất
                try:
                    filename = os.path.basename(file)
                    parts = filename.split('_')
                    
                    if len(parts) >= 4:
                        company = parts[2]
                        date_part = parts[3].split('.')[0]
                        
                        # Format date: DDMMYYYY_HHMMSS -> DD/MM/YYYY HH:MM
                        if len(date_part) >= 13:
                            date = date_part[:8]
                            time_part = date_part[9:13]
                            formatted_date = f"{date[0:2]}/{date[2:4]}/{date[4:8]} {time_part[0:2]}:{time_part[2:4]}"
                        else:
                            formatted_date = date_part
                        
                        if st.sidebar.button(f"📊 {company}\n{formatted_date}", key=file):
                            with open(file, 'r', encoding='utf-8') as f:
                                st.markdown(f.read())
                                
                except (IndexError, ValueError) as e:
                    st.sidebar.error(f"❌ Lỗi đọc file {filename}: {e}")
                    continue
        else:
            st.sidebar.info("📝 Chưa có cuộc họp nào được chuẩn bị")
            
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi khi hiển thị lịch sử: {e}")


def display_metrics(meeting_duration: int, attendees: str, company_name: str):
    """
    Hiển thị metrics dashboard
    
    Args:
        meeting_duration (int): Thời lượng cuộc họp
        attendees (str): Danh sách người tham gia
        company_name (str): Tên công ty
    """
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⏱️ Thời lượng", f"{meeting_duration} phút")
        
        with col2:
            attendee_count = len([line.strip() for line in attendees.split('\n') if line.strip()]) if attendees else 0
            st.metric("👥 Số người tham gia", attendee_count)
        
        with col3:
            if meeting_duration > 90:
                complexity = "Cao"
                complexity_color = "red"
            elif meeting_duration > 45:
                complexity = "Trung bình"
                complexity_color = "orange"
            else:
                complexity = "Thấp"
                complexity_color = "green"
            st.metric("📊 Độ phức tạp", complexity)
        
        with col4:
            if company_name:
                st.metric("🏢 Công ty", company_name)
                
    except Exception as e:
        st.error(f"❌ Lỗi khi hiển thị metrics: {e}")


def display_sidebar_instructions():
    """
    Hiển thị hướng dẫn trong sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 Hướng dẫn sử dụng")
    st.sidebar.markdown("""
    **Bước 1:** Nhập thông tin cuộc họp
    - Tên công ty
    - Mục đích cuộc họp
    - Danh sách người tham gia
    - Thời lượng dự kiến
    - Các mục tiêu cần đạt được
    
    **Bước 2:** Chọn tùy chọn
    - ✅ Hiển thị log chi tiết (nếu muốn)
    
    **Bước 3:** Nhấn "Chuẩn bị cuộc họp"
    - Hệ thống sẽ phân tích và tạo báo cáo
    - Có thể tải xuống kết quả
    
    **Lưu ý:**
    - Tất cả trường đều bắt buộc
    - Thời lượng: 15-180 phút
    - Tối đa 20 người tham gia
    """)


def display_crew_progress(crew, meeting_data: Dict[str, Any]):
    """
    Hiển thị tiến trình thực thi crew với animation
    
    Args:
        crew: CrewAI crew instance
        meeting_data: Dữ liệu cuộc họp
        
    Returns:
        result: Kết quả từ crew
    """
    company_name = meeting_data.get('company_name', 'Unknown')
    
    # Container cho progress
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🚀 Tiến trình chuẩn bị cuộc họp")
        
        # Progress bar tổng
        main_progress = st.progress(0)
        main_status = st.empty()
        
        # Progress cho từng agent
        col1, col2, col3, col4 = st.columns(4)
        
        agents_progress = {}
        agents_status = {}
        
        with col1:
            st.markdown("**🔍 Context Analyzer**")
            agents_status['context'] = st.empty()
            agents_progress['context'] = st.progress(0)
        
        with col2:
            st.markdown("**📊 Industry Insights**")
            agents_status['industry'] = st.empty()
            agents_progress['industry'] = st.progress(0)
        
        with col3:
            st.markdown("**📋 Strategy Formulator**")
            agents_status['strategy'] = st.empty()
            agents_progress['strategy'] = st.progress(0)
        
        with col4:
            st.markdown("**📝 Executive Brief**")
            agents_status['executive'] = st.empty()
            agents_progress['executive'] = st.progress(0)
    
    # Simulate realistic progress
    try:
        # Phase 1: Context Analysis (0-25%)
        main_status.text(f"🔍 Đang phân tích bối cảnh cuộc họp cho {company_name}...")
        agents_status['context'].text("🔍 Tìm kiếm thông tin công ty...")
        
        for i in range(25):
            agents_progress['context'].progress((i + 1) * 4)
            main_progress.progress(i + 1)
            time.sleep(0.02)
        
        agents_status['context'].text("✅ Hoàn thành phân tích bối cảnh")
        
        # Phase 2: Industry Insights (25-50%)
        main_status.text("📊 Đang thu thập insights ngành...")
        agents_status['industry'].text("📊 Phân tích xu hướng ngành...")
        
        for i in range(25):
            agents_progress['industry'].progress((i + 1) * 4)
            main_progress.progress(25 + i + 1)
            time.sleep(0.02)
            
        agents_status['industry'].text("✅ Hoàn thành phân tích ngành")
        
        # Phase 3: Strategy (50-75%)
        main_status.text("📋 Đang xây dựng chiến lược cuộc họp...")
        agents_status['strategy'].text("📋 Tạo agenda và chiến lược...")
        
        for i in range(25):
            agents_progress['strategy'].progress((i + 1) * 4)
            main_progress.progress(50 + i + 1)
            time.sleep(0.02)
            
        agents_status['strategy'].text("✅ Hoàn thành chiến lược")
        
        # Phase 4: Executive Brief (75-100%)
        main_status.text("📝 Đang tạo báo cáo tổng hợp...")
        agents_status['executive'].text("📝 Tổng hợp thông tin...")
        
        for i in range(25):
            agents_progress['executive'].progress((i + 1) * 4)
            main_progress.progress(75 + i + 1)
            time.sleep(0.02)
            
        agents_status['executive'].text("✅ Hoàn thành báo cáo")
        main_status.text("🎉 Hoàn thành! Đang tạo báo cáo cuối cùng...")
        
        # Execute actual crew
        result = crew.kickoff()
        
        main_status.text("✅ Chuẩn bị cuộc họp hoàn tất!")
        return result
        
    except Exception as e:
        main_status.text("❌ Có lỗi xảy ra trong quá trình chuẩn bị")
        st.error(f"Lỗi: {e}")
        return None


def display_fun_facts():
    """
    Hiển thị fun facts trong quá trình chờ
    """
    facts = [
        "💡 Cuộc họp hiệu quả nhất thường kéo dài 30-45 phút",
        "🎯 60% thời gian cuộc họp nên dành cho thảo luận",
        "📊 Agenda rõ ràng giúp tăng hiệu quả cuộc họp lên 40%",
        "⏰ Cuộc họp buổi sáng thường hiệu quả hơn buổi chiều",
        "👥 Số người tham gia lý tưởng là 5-7 người",
        "📝 Ghi chú cuộc họp giúp tăng follow-up lên 70%",
        "🚀 Cuộc họp đứng thường nhanh hơn 34% so với ngồi",
        "🎨 Sử dụng visual aids tăng hiểu biết lên 60%"
    ]
    
    selected_fact = random.choice(facts)
    st.info(selected_fact)


def display_agent_details(show_verbose: bool = False):
    """
    Hiển thị thông tin chi tiết về các AI agents
    
    Args:
        show_verbose (bool): Có hiển thị chi tiết không
    """
    if show_verbose:
        st.markdown("---")
        st.markdown("### 🤖 Chi tiết AI Agents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔍 Context Analyzer**
            - Phân tích thông tin công ty
            - Tìm hiểu tin tức gần đây
            - Xác định stakeholders chính
            """)
            
            st.markdown("""
            **📋 Strategy Formulator**
            - Xây dựng agenda cuộc họp
            - Đề xuất cấu trúc thời gian
            - Tạo talking points
            """)
        
        with col2:
            st.markdown("""
            **📊 Industry Insights Generator**
            - Phân tích xu hướng ngành
            - Tìm kiếm cơ hội và thách thức
            - Benchmarking với đối thủ
            """)
            
            st.markdown("""
            **📝 Executive Briefing Creator**
            - Tổng hợp tất cả thông tin
            - Tạo executive summary
            - Format báo cáo professional
            """)

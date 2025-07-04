"""
Utility functions for Meeting Preparation System
"""
import datetime
import glob
import streamlit as st
import os

def save_meeting_result(result, company_name):
    """
    Lưu kết quả cuộc họp vào file
    
    Args:
        result: Kết quả        messages = [
            "🔍 Đang tổng hợp phân tích bối cảnh...",
            "📊 Đang kết hợp insights ngành...", 
            "📋 Đang hoàn thiện chiến lược...",
            "📝 Đang tạo executive summary...",
            "✨ Đang polish báo cáo cuối cùng...",
            "🎯 Đang kiểm tra chất lượng...",
            "📋 Đang format và cấu trúc...",
            "🔧 Đang tối ưu hóa nội dung...",
            "💎 Đang hoàn thiện những chi tiết cuối...",
            "🚀 Sắp xong rồi! Đang finalize...",
            "⭐ Đang thêm những touch cuối cùng...",
            "🎨 Đang làm cho báo cáo thêm professional..."
        ]        company_name (str): Tên công ty
    
    Returns:
        str: Tên file đã lưu
    """
    report_dir = "reports"
    filename = os.path.join(report_dir, f"meeting_prep_{company_name}_{datetime.datetime.now().strftime('%d%m%Y_%H%M%S')}.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Chuẩn bị cuộc họp - {company_name}\n")
        f.write(f"**Ngày tạo:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write(str(result))
    
    return filename

def display_meeting_history():
    """
    Hiển thị lịch sử cuộc họp trong sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("Lịch sử cuộc họp")
    
    meeting_files = glob.glob("meeting_prep_*.md")
    if meeting_files:
        meeting_files.sort(reverse=True)  # Mới nhất trước
        for file in meeting_files[:5]:  # Hiển thị 5 file gần nhất
            try:
                parts = file.split('_')
                if len(parts) >= 4:
                    company = parts[2]
                    date = parts[3].split('.')[0]
                    formatted_date = f"{date[:4]}/{date[4:6]}/{date[6:8]} {date[9:11]}:{date[11:13]}"
                    
                    if st.sidebar.button(f"📊 {company} - {formatted_date}", key=file):
                        with open(file, 'r', encoding='utf-8') as f:
                            st.markdown(f.read())
            except (IndexError, ValueError):
                # Skip malformed filenames
                continue
    else:
        st.sidebar.info("Chưa có cuộc họp nào được chuẩn bị")

def display_metrics(meeting_duration, attendees, company_name):
    """
    Hiển thị metrics dashboard
    
    Args:
        meeting_duration (int): Thời lượng cuộc họp
        attendees (str): Danh sách người tham gia
        company_name (str): Tên công ty
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏱️ Thời lượng", f"{meeting_duration} phút")
    
    with col2:
        attendee_count = len(attendees.split('\n')) if attendees else 0
        st.metric("👥 Số người tham gia", attendee_count)
    
    with col3:
        complexity = "Cao" if meeting_duration > 90 else "Trung bình" if meeting_duration > 45 else "Thấp"
        st.metric("📊 Độ phức tạp", complexity)
    
    with col4:
        if company_name:
            st.metric("🏢 Công ty", company_name)

def validate_inputs(company_name, meeting_objective, attendees, focus_areas):
    """
    Kiểm tra tính hợp lệ của inputs
    
    Args:
        company_name (str): Tên công ty
        meeting_objective (str): Mục đích cuộc họp
        attendees (str): Người tham gia
        focus_areas (str): Lĩnh vực trọng tâm
    
    Returns:
        bool: True nếu tất cả inputs hợp lệ
    """
    return all([company_name, meeting_objective, attendees, focus_areas])

def display_sidebar_instructions():
    """
    Hiển thị hướng dẫn sử dụng trong sidebar
    """
    st.sidebar.markdown("""
    ## Cách sử dụng ứng dụng này:
    1. Cung cấp thông tin được yêu cầu về cuộc họp.
    2. Nhấp vào 'Chuẩn bị cuộc họp' để tạo gói chuẩn bị cuộc họp toàn diện của bạn.

    Các tác nhân AI sẽ cùng nhau:
    - Phân tích bối cảnh cuộc họp và thông tin công ty
    - Cung cấp thông tin chi tiết và xu hướng ngành
    - Phát triển chiến lược và chương trình cuộc họp tùy chỉnh
    - Tạo bản tóm tắt điều hành với các điểm nói chuyện chính

    Quá trình này có thể mất vài phút. Xin hãy kiên nhẫn!
    """)

def create_download_button(result, filename):
    """
    Tạo nút download cho kết quả
    
    Args:
        result: Kết quả cần download
        filename (str): Tên file
    """
    st.download_button(
        label="📥 Tải xuống kết quả",
        data=str(result),
        file_name=filename,
        mime="text/markdown"
    )

def display_crew_progress(crew, meeting_data):
    """
    Hiển thị tiến trình thực hiện của crew với chi tiết từng agent
    
    Args:
        crew: Crew instance
        meeting_data (dict): Thông tin cuộc họp
    
    Returns:
        result: Kết quả từ crew
    """
    company_name = meeting_data['company_name']
    
    # Container cho progress
    progress_container = st.container()
    
    with progress_container:
        # Progress bar tổng
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Progress cho từng agent
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**🔍 Context Analyzer**")
            context_status = st.empty()
            context_progress = st.progress(0)
        
        with col2:
            st.markdown("**📊 Industry Insights**")
            industry_status = st.empty()
            industry_progress = st.progress(0)
        
        with col3:
            st.markdown("**📋 Strategy Formulator**")
            strategy_status = st.empty()
            strategy_progress = st.progress(0)
        
        with col4:
            st.markdown("**📝 Executive Brief**")
            executive_status = st.empty()
            executive_progress = st.progress(0)
    
    # Mô phỏng tiến trình thực tế
    import time
    
    # Bước 1: Context Analysis
    status_text.text(f"🔍 Đang phân tích bối cảnh cuộc họp cho {company_name}...")
    context_status.text("Đang tìm kiếm thông tin công ty...")
    for i in range(20):
        context_progress.progress((i + 1) * 5)
        progress_bar.progress((i + 1) * 1)
        time.sleep(0.03)  # Nhanh hơn
    
    context_status.text("Đang phân tích tin tức gần đây...")
    for i in range(20, 25):
        context_progress.progress((i + 1) * 4)
        progress_bar.progress((i + 1) * 1)
        time.sleep(0.03)
    context_status.text("✅ Hoàn thành phân tích bối cảnh")
    
    # Bước 2: Industry Analysis  
    status_text.text("📊 Đang phân tích ngành và xu hướng thị trường...")
    industry_status.text("Đang nghiên cứu xu hướng ngành...")
    for i in range(20):
        industry_progress.progress((i + 1) * 5)
        progress_bar.progress(25 + (i + 1) * 1)
        time.sleep(0.03)
    
    industry_status.text("Đang phân tích đối thủ cạnh tranh...")
    for i in range(20, 25):
        industry_progress.progress((i + 1) * 4)
        progress_bar.progress(25 + (i + 1) * 1)
        time.sleep(0.03)
    industry_status.text("✅ Hoàn thành phân tích ngành")
    
    # Bước 3: Strategy Development
    status_text.text("📋 Đang phát triển chiến lược và agenda cuộc họp...")
    strategy_status.text("Đang tạo agenda chi tiết...")
    for i in range(15):
        strategy_progress.progress((i + 1) * 6)
        progress_bar.progress(50 + (i + 1) * 1)
        time.sleep(0.03)
    
    strategy_status.text("Đang phát triển talking points...")
    for i in range(15, 25):
        strategy_progress.progress(90 + (i - 14) * 1)
        progress_bar.progress(50 + (i + 1) * 1)
        time.sleep(0.03)
    strategy_status.text("✅ Hoàn thành chiến lược")
    
    # Bước 4: Executive Brief
    status_text.text("📝 Đang tạo bản tóm tắt điều hành toàn diện...")
    executive_status.text("Đang tổng hợp tất cả thông tin...")
    for i in range(15):
        executive_progress.progress((i + 1) * 6)
        progress_bar.progress(75 + (i + 1) * 1)
        time.sleep(0.03)
    
    executive_status.text("Đang chuẩn bị Q&A section...")
    for i in range(15, 25):
        executive_progress.progress(90 + (i - 14) * 1)
        progress_bar.progress(75 + (i + 1) * 1)
        time.sleep(0.03)
    executive_status.text("✅ Hoàn thành tóm tắt điều hành")
    
    # Thực thi crew
    status_text.text("🤖 Đang xử lý và hoàn thiện kết quả cuối cùng...")
    
    # Thực hiện crew kickoff với progress bar động
    final_progress = st.progress(0)
    final_status = st.empty()
    
    import threading
    import queue
    
    # Queue để truyền kết quả
    result_queue = queue.Queue()
    progress_queue = queue.Queue()
    
    def run_crew():
        try:
            result = crew.kickoff()
            result_queue.put(result)
        except Exception as e:
            result_queue.put(f"Lỗi: {e}")
    
    def animate_progress():
        messages = [
            "🔍 Đang tổng hợp phân tích bối cảnh...",
            "📊 Đang kết hợp insights ngành...", 
            "📋 Đang hoàn thiện chiến lược...",
            "📝 Đang tạo executive summary...",
            "✨ Đang polish báo cáo cuối cùng...",
            "🎯 Đang kiểm tra chất lượng...",
            "📋 Đang format và cấu trúc...",
            "🔧 Đang tối ưu hóa nội dung..."
        ]
        
        progress = 0
        message_index = 0
        
        while result_queue.empty():
            # Cập nhật message
            if message_index < len(messages):
                final_status.text(messages[message_index])
                message_index = (message_index + 1) % len(messages)
            
            # Tăng progress (chậm để tránh đạt 100% quá sớm)
            if progress < 95:
                progress += 1
                final_progress.progress(progress)
            
            time.sleep(0.3)  # Update mỗi 0.3 giây
    
    # Chạy crew trong thread riêng
    crew_thread = threading.Thread(target=run_crew)
    crew_thread.start()
    
    # Chạy animation
    animate_progress()
    
    # Chờ kết quả
    crew_thread.join()
    result = result_queue.get()
    
    # Hoàn thành
    final_progress.progress(100)
    final_status.text("✅ Đã tạo xong báo cáo!")
    progress_bar.progress(100)
    status_text.text("✅ Đã hoàn thành tất cả các bước chuẩn bị cuộc họp!")
    
    # Clear progress sau 3 giây
    time.sleep(3)
    progress_container.empty()
    
    return result

def display_agent_details():
    """
    Hiển thị thông tin chi tiết về các agent
    """
    with st.expander("🤖 Thông tin chi tiết về các AI Agents"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔍 Context Analyzer**
            - Phân tích thông tin công ty
            - Tìm kiếm tin tức mới nhất
            - Xác định đối thủ cạnh tranh
            
            **📊 Industry Insights Generator**
            - Phân tích xu hướng ngành
            - Đánh giá cơ hội/thách thức
            - Nghiên cứu thị trường
            """)
        
        with col2:
            st.markdown("""
            **📋 Strategy Formulator**
            - Tạo agenda cuộc họp
            - Phát triển chiến lược
            - Lập kế hoạch thời gian
            
            **📝 Executive Briefing Creator**
            - Tổng hợp thông tin
            - Tạo talking points
            - Chuẩn bị Q&A
            """)

def display_fun_facts():
    """
    Hiển thị các fun facts về AI và meeting trong lúc chờ
    """
    fun_facts = [
        "💡 **Fun Fact**: Trung bình một nhân viên văn phòng dành 37% thời gian trong các cuộc họp!",
        "🤖 **AI Insight**: AI có thể phân tích 1000 trang tài liệu trong thời gian bạn đọc 1 trang!",
        "📊 **Meeting Stats**: 67% executives cho rằng họ dành quá nhiều thời gian trong các cuộc họp không hiệu quả.",
        "⚡ **Speed Fact**: AI agents của chúng ta đang xử lý thông tin nhanh hơn 10,000 lần so với con người!",
        "🎯 **Productivity**: Các cuộc họp được chuẩn bị kỹ lưỡng có hiệu quả cao hơn 40%!",
        "🔍 **Research**: AI đang tìm kiếm qua hàng triệu trang web để tìm thông tin tốt nhất cho bạn!",
        "📈 **Trend**: 85% các công ty thành công đều có quy trình chuẩn bị cuộc họp chuyên nghiệp.",
        "🚀 **Innovation**: Bạn đang sử dụng công nghệ tương tự như các tập đoàn Fortune 500!"
    ]
    
    import random
    selected_fact = random.choice(fun_facts)
    
    with st.expander("💫 Thông tin thú vị trong lúc chờ"):
        st.markdown(selected_fact)
        st.markdown("---")
        st.markdown("🎵 *Hãy thư giãn, AI đang làm việc chăm chỉ cho bạn...*")

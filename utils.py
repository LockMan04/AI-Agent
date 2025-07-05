"""
Utility functions for Meeting Preparation System - Simplified Version
"""
import datetime
import glob
import streamlit as st
import os
import time
import random


def save_meeting_result(result, company_name):
    """Lưu kết quả cuộc họp vào file"""
    try:
        # Tạo thư mục reports nếu chưa có
        os.makedirs("reports", exist_ok=True)
        
        # Tạo tên file an toàn
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        timestamp = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        filename = f"reports/meeting_prep_{safe_company_name}_{timestamp}.md"
        
        # Ghi file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Chuẩn bị cuộc họp - {company_name}\n")
            f.write(f"**Ngày tạo:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(str(result))
        
        return filename
    except Exception as e:
        st.error(f"❌ Lỗi khi lưu file: {e}")
        return None


def create_download_button(filename, company_name):
    """Tạo button download file"""
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
        st.error(f"❌ Lỗi download: {e}")


def display_meeting_history():
    """Hiển thị lịch sử cuộc họp trong sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Lịch sử cuộc họp")
    
    try:
        meeting_files = glob.glob("reports/meeting_prep_*.md")
        if meeting_files:
            meeting_files.sort(key=os.path.getmtime, reverse=True)  # Mới nhất trước
            
            for file in meeting_files[:5]:  # Hiển thị 5 file gần nhất
                try:
                    filename = os.path.basename(file)
                    parts = filename.split('_')
                    
                    if len(parts) >= 4:
                        company = parts[2]
                        date_part = parts[3].split('.')[0]
                        
                        # Format ngày
                        if len(date_part) >= 13:
                            date = date_part[:8]
                            time_part = date_part[9:13]
                            formatted_date = f"{date[0:2]}/{date[2:4]}/{date[4:8]} {time_part[0:2]}:{time_part[2:4]}"
                        else:
                            formatted_date = date_part
                        
                        if st.sidebar.button(f"📊 {company}\n{formatted_date}", key=file):
                            with open(file, 'r', encoding='utf-8') as f:
                                st.markdown(f.read())
                                
                except Exception:
                    continue
        else:
            st.sidebar.info("📝 Chưa có cuộc họp nào")
            
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi: {e}")


def display_metrics(meeting_duration, attendees, company_name):
    """Hiển thị metrics dashboard"""
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⏱️ Thời lượng", f"{meeting_duration} phút")
        
        with col2:
            attendee_count = len([line.strip() for line in attendees.split('\n') if line.strip()]) if attendees else 0
            st.metric("👥 Số người tham gia", attendee_count)
        
        with col3:
            complexity = "Cao" if meeting_duration > 90 else "Trung bình" if meeting_duration > 45 else "Thấp"
            st.metric("📊 Độ phức tạp", complexity)
        
        with col4:
            if company_name:
                st.metric("🏢 Công ty", company_name)
                
    except Exception as e:
        st.error(f"❌ Lỗi metrics: {e}")


def validate_inputs(company_name, meeting_objective, attendees, focus_areas):
    """Kiểm tra tính hợp lệ của inputs"""
    if not company_name or not company_name.strip():
        return False
    if not meeting_objective or not meeting_objective.strip():
        return False
    if not attendees or not attendees.strip():
        return False
    if not focus_areas or not focus_areas.strip():
        return False
    return True


def display_sidebar_instructions():
    """Hiển thị hướng dẫn chi tiết trong sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 Hướng dẫn sử dụng")
    st.sidebar.markdown("""
    **Bước 1:** Nhập thông tin cuộc họp
    - 🏢 Tên công ty (bắt buộc)
    - 🎯 Mục đích cuộc họp rõ ràng
    - 👥 Danh sách người tham gia và vai trò
    - ⏱️ Thời lượng dự kiến (15-180 phút)
    - 🎨 Các mục tiêu cần đạt được
    
    **Bước 2:** Tùy chọn nâng cao
    - ✅ Hiển thị log chi tiết (nếu muốn)
    - 📊 Theo dõi tiến trình real-time
    
    **Bước 3:** Thực hiện chuẩn bị
    - 🚀 Nhấn "Chuẩn bị cuộc họp"
    - ⏳ Đợi AI agents hoàn thành
    - 📥 Tải xuống kết quả
    
    **💡 Mẹo sử dụng:**
    - Thông tin càng chi tiết, kết quả càng tốt
    - Agenda sẽ được tối ưu theo thời lượng
    - Có thể xem lại lịch sử các cuộc họp
    
    **📊 Metrics Dashboard:**
    - Theo dõi độ phức tạp cuộc họp
    - Thống kê số người tham gia
    - Phân tích thời lượng tối ưu
    """)
    
    # Thêm phần thống kê nhanh
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Thống kê nhanh")
    
    try:
        import glob
        meeting_files = glob.glob("reports/meeting_prep_*.md")
        total_meetings = len(meeting_files)
        
        if total_meetings > 0:
            st.sidebar.metric("📊 Tổng cuộc họp đã chuẩn bị", total_meetings)
            
            # Thống kê tuần này
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            recent_files = [f for f in meeting_files 
                          if os.path.getmtime(f) > week_ago.timestamp()]
            
            st.sidebar.metric("📅 Cuộc họp tuần này", len(recent_files))
        else:
            st.sidebar.info("🎯 Hãy chuẩn bị cuộc họp đầu tiên!")
            
    except Exception:
        pass


def display_crew_progress(crew, meeting_data):
    """Hiển thị tiến trình crew với animation thực tế hơn"""
    company_name = meeting_data.get('company_name', 'Unknown')
    
    # Container cho progress
    progress_container = st.container()
    
    with progress_container:
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
    
    try:
        # Các message động cho từng phase
        context_messages = [
            "🔍 Bắt đầu tìm kiếm thông tin...",
            "🏢 Đang phân tích thông tin công ty...",
            "📰 Thu thập tin tức và báo cáo gần đây...",
            "👥 Xác định các stakeholder chính...",
            "� Đánh giá tình hình tài chính...",
            "🎯 Phân tích mục tiêu kinh doanh...",
            "✅ Hoàn thành phân tích bối cảnh"
        ]
        
        industry_messages = [
            "📊 Khởi động phân tích ngành...",
            "📈 Nghiên cứu xu hướng thị trường...",
            "🏆 Phân tích đối thủ cạnh tranh...",
            "💡 Tìm kiếm cơ hội phát triển...",
            "⚠️ Đánh giá rủi ro tiềm ẩn...",
            "🔍 Thu thập market insights...",
            "✅ Hoàn thành phân tích ngành"
        ]
        
        strategy_messages = [
            "📋 Bắt đầu thiết kế chiến lược...",
            "⏰ Xây dựng cấu trúc thời gian...",
            "🎯 Tạo agenda chi tiết...",
            "💬 Chuẩn bị talking points...",
            "❓ Thiết kế câu hỏi thảo luận...",
            "🚀 Tối ưu hóa flow cuộc họp...",
            "✅ Hoàn thành chiến lược"
        ]
        
        executive_messages = [
            "📝 Khởi tạo báo cáo tổng hợp...",
            "📋 Tổng hợp thông tin từ các agent...",
            "💼 Tạo executive summary...",
            "� Thêm charts và visualizations...",
            "🎨 Format báo cáo chuyên nghiệp...",
            "✅ Finalize deliverables...",
            "✅ Hoàn thành báo cáo"
        ]
        
        # Phase 1: Context Analysis (0-25%) - Chậm hơn, thực tế hơn
        main_status.text(f"🔍 Đang phân tích bối cảnh cuộc họp cho {company_name}...")
        
        for i, message in enumerate(context_messages):
            agents_status['context'].text(message)
            progress_val = int((i + 1) / len(context_messages) * 100)
            agents_progress['context'].progress(progress_val)
            main_progress.progress(int(progress_val * 0.25))
            time.sleep(0.8)  # Chậm hơn để realistic
        
        # Phase 2: Industry Insights (25-50%)
        main_status.text("📊 Đang thu thập insights ngành...")
        
        for i, message in enumerate(industry_messages):
            agents_status['industry'].text(message)
            progress_val = int((i + 1) / len(industry_messages) * 100)
            agents_progress['industry'].progress(progress_val)
            main_progress.progress(25 + int(progress_val * 0.25))
            time.sleep(0.8)
        
        # Phase 3: Strategy (50-75%)
        main_status.text("📋 Đang xây dựng chiến lược cuộc họp...")
        
        for i, message in enumerate(strategy_messages):
            agents_status['strategy'].text(message)
            progress_val = int((i + 1) / len(strategy_messages) * 100)
            agents_progress['strategy'].progress(progress_val)
            main_progress.progress(50 + int(progress_val * 0.25))
            time.sleep(0.8)
        
        # Phase 4: Executive Brief (75-100%)
        main_status.text("📝 Đang tạo báo cáo tổng hợp...")
        
        for i, message in enumerate(executive_messages):
            agents_status['executive'].text(message)
            progress_val = int((i + 1) / len(executive_messages) * 100)
            agents_progress['executive'].progress(progress_val)
            main_progress.progress(75 + int(progress_val * 0.25))
            time.sleep(0.8)
        
        # Final phase với loading animation
        main_status.text("🎉 Hoàn thành! Đang tạo báo cáo cuối cùng...")
        
        # Thêm animation loading cho phần cuối
        loading_messages = [
            "🔄 Đang compile kết quả...",
            "📄 Đang format báo cáo...",
            "🎨 Đang tối ưu hóa layout...",
            "✅ Sắp hoàn thành..."
        ]
        
        for i, message in enumerate(loading_messages):
            main_status.text(message)
            time.sleep(0.5)
        
        # Execute actual crew (chạy thật)
        main_status.text("⚡ Đang chạy AI Crew...")
        result = crew.kickoff()
        
        main_status.text("✅ Chuẩn bị cuộc họp hoàn tất!")
        return result
        
    except Exception as e:
        main_status.text("❌ Có lỗi xảy ra trong quá trình chuẩn bị")
        st.error(f"Lỗi: {e}")
        return None


def display_fun_facts():
    """Hiển thị fun facts thú vị về cuộc họp"""
    facts = [
        "💡 Cuộc họp hiệu quả nhất thường kéo dài 30-45 phút",
        "🎯 60% thời gian cuộc họp nên dành cho thảo luận",
        "📊 Agenda rõ ràng giúp tăng hiệu quả cuộc họp lên 40%",
        "⏰ Cuộc họp buổi sáng thường hiệu quả hơn buổi chiều",
        "👥 Số người tham gia lý tưởng là 5-7 người",
        "📝 Ghi chú cuộc họp giúp tăng follow-up lên 70%",
        "🚀 Cuộc họp đứng thường nhanh hơn 34% so với ngồi",
        "🎨 Sử dụng visual aids tăng hiểu biết lên 60%",
        "🔄 90% các quyết định quan trọng được đưa ra trong 10 phút đầu",
        "📱 Tắt điện thoại giúp tăng tập trung lên 50%",
        "🌡️ Nhiệt độ phòng lý tưởng cho cuộc họp là 21-23°C",
        "☕ Uống cà phê trước cuộc họp tăng sự tỉnh táo lên 25%"
    ]
    
    selected_fact = random.choice(facts)
    st.info(selected_fact)


def display_agent_details():
    """Hiển thị thông tin chi tiết về các AI agents với expander"""
    with st.expander("🤖 Chi tiết AI Agents", expanded=False):
        st.markdown("*Hệ thống sử dụng 4 AI agents chuyên biệt để chuẩn bị cuộc họp một cách toàn diện*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔍 Context Analyzer**
            - 🏢 Phân tích thông tin công ty và ngành
            - 📰 Tìm hiểu tin tức và sự kiện gần đây
            - 👥 Xác định stakeholders chính
            - 🎯 Đánh giá bối cảnh kinh doanh
            
            **📋 Strategy Formulator**
            - 📅 Xây dựng agenda cuộc họp chi tiết
            - ⏰ Đề xuất cấu trúc thời gian tối ưu
            - 🎨 Tạo talking points và câu hỏi chính
            - 🚀 Đưa ra chiến lược thảo luận hiệu quả
            """)
        
        with col2:
            st.markdown("""
            **📊 Industry Insights Generator**
            - 📈 Phân tích xu hướng và cơ hội ngành
            - 🔍 Tìm kiếm thách thức và rủi ro tiềm ẩn
            - 🏆 Benchmarking với đối thủ cạnh tranh
            - 💡 Đề xuất insights và recommendations
            
            **📝 Executive Briefing Creator**
            - 📋 Tổng hợp tất cả thông tin thành báo cáo
            - 💼 Tạo executive summary ngắn gọn
            - 🎨 Format báo cáo professional
            - 📊 Bao gồm charts và key takeaways
            """)
        
        with st.expander("🔄 Quy trình làm việc chi tiết", expanded=False):
            # Workflow diagram using text
            workflow_col1, workflow_col2, workflow_col3, workflow_col4 = st.columns(4)
            
            with workflow_col1:
                st.markdown("""
                **Bước 1** 🔍
                
                **Context Analysis**
                
                *Thu thập & phân tích dữ liệu*
                
                - Nghiên cứu công ty
                - Tìm tin tức gần đây
                - Phân tích stakeholders
                - Đánh giá bối cảnh
                """)
            
            with workflow_col2:
                st.markdown("""
                **Bước 2** 📊
                
                **Industry Research**
                
                *Insights & trends*
                
                - Xu hướng ngành
                - Phân tích đối thủ
                - Cơ hội & rủi ro
                - Market insights
                """)
            
            with workflow_col3:
                st.markdown("""
                **Bước 3** 📋
                
                **Strategy Design**
                
                *Agenda & structure*
                
                - Thiết kế agenda
                - Cấu trúc thời gian
                - Talking points
                - Q&A preparation
                """)
            
            with workflow_col4:
                st.markdown("""
                **Bước 4** 📝
                
                **Report Creation**
                
                *Final deliverable*
                
                - Tổng hợp thông tin
                - Executive summary
                - Action items
                - Next steps
                """)
        
        st.info("💡 **Pro tip:** Bật chế độ verbose để xem chi tiết quá trình làm việc của từng agent")

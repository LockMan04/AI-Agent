import streamlit as st
from crewai import Crew, LLM
from crewai.process import Process

# Import các modules tự tạo
from config import Config
from agents import create_agents
from tasks import create_tasks
from utils import (
    save_meeting_result, 
    display_meeting_history, 
    display_metrics, 
    validate_inputs,
    display_sidebar_instructions,
    create_download_button,
    display_crew_progress,
    display_agent_details,
    display_fun_facts
)

# Streamlit app setup
st.set_page_config(page_title=Config.PAGE_TITLE, layout=Config.PAGE_LAYOUT)
st.title(Config.PAGE_TITLE)

# Check if all API keys are set
if Config.validate_api_keys():
    # Set API keys as environment variables
    Config.set_environment_variables()

    chatgpt = LLM(model=Config.MODEL_NAME, temperature=Config.MODEL_TEMPERATURE, api_key=Config.OPENAI_API_KEY)

    # Input fields
    company_name = st.text_input("Nhập tên công ty:")
    meeting_objective = st.text_input("Mục đích cuộc họp:")
    attendees = st.text_area("Nhập người tham gia và vai trò của họ (một người mỗi dòng):")
    meeting_duration = st.number_input(
        "Nhập thời gian (phút):", 
        min_value=Config.MIN_MEETING_DURATION, 
        max_value=Config.MAX_MEETING_DURATION, 
        value=Config.DEFAULT_MEETING_DURATION, 
        step=Config.MEETING_DURATION_STEP
    )
    focus_areas = st.text_input("Nhập mục tiêu mà cần đạt được:")
    
    # Tùy chọn hiển thị log chi tiết
    show_verbose = st.checkbox("🔍 Hiển thị log chi tiết quá trình", value=False)
    
    # Validation
    all_fields_filled = validate_inputs(company_name, meeting_objective, attendees, focus_areas)
    
    if not all_fields_filled:
        st.warning("⚠️ Vui lòng điền đầy đủ tất cả thông tin trước khi chuẩn bị cuộc họp")
    else:
        st.success("✅ Thông tin đã đầy đủ, sẵn sàng chuẩn bị cuộc họp!")

        # Tạo agents và tasks
        agents = create_agents(chatgpt)
        
        meeting_data = {
            'company_name': company_name,
            'meeting_objective': meeting_objective,
            'attendees': attendees,
            'meeting_duration': meeting_duration,
            'focus_areas': focus_areas
        }
        
        tasks = create_tasks(agents, meeting_data)

        # Tạo crew
        meeting_prep_crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=show_verbose,
            process=Process.sequential
        )

        # Chạy crew khi người dùng nhấp vào nút
        if st.button("🚀 Chuẩn bị cuộc họp", disabled=not all_fields_filled, type="primary"):
            if show_verbose:
                st.info("🔍 Chế độ verbose được bật - sẽ hiển thị log chi tiết")
            
            # Hiển thị thông tin agents (có thể đóng/mở)
            display_agent_details()
            
            # Hiển thị fun facts
            display_fun_facts()
            
            # Chạy crew với progress display
            st.markdown("### 🚀 Tiến trình chuẩn bị cuộc họp")
            result = display_crew_progress(meeting_prep_crew, meeting_data)
            
            if result:
                st.success("✅ Đã chuẩn bị xong cuộc họp!")
                st.markdown("---")
                st.markdown("### 📋 Kết quả chuẩn bị cuộc họp")
                st.markdown(result)
                
                # Lưu kết quả và tạo download button
                filename = save_meeting_result(result, company_name)
                if filename:
                    st.info(f"📁 Kết quả đã được lưu vào file: {filename}")
                    create_download_button(filename, company_name)

    # Hiển thị metrics dashboard
    display_metrics(meeting_duration, attendees, company_name)
    st.markdown("---")

    # Sidebar instructions and meeting history
    display_sidebar_instructions()
    display_meeting_history()

else:
    st.error("❌ Thiếu API keys!")
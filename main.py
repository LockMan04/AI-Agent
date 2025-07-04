import streamlit as st
from crewai import Crew, LLM
from crewai.process import Process

# Import các modules tự tạo
try:
    from config_enhanced import Config, ConfigError
except ImportError:
    from config import Config
    ConfigError = Exception

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
from utils.security import SecurityValidator, InputValidator, log_security_event

# Streamlit app setup
st.set_page_config(page_title=Config.PAGE_TITLE, layout=Config.PAGE_LAYOUT)
st.title(Config.PAGE_TITLE)

# Security: Rate limiting
if not SecurityValidator.check_rate_limit("main_page_access", max_requests=50, time_window=3600):
    st.error("❌ Quá nhiều requests. Vui lòng thử lại sau.")
    st.stop()

# Check if all API keys are set
try:
    if Config.validate_api_keys():
        # Set API keys as environment variables
        Config.set_environment_variables()
        # Ensure required directories exist
        Config.ensure_directories()
    else:
        st.stop()  # Stop execution if API keys are missing
except ConfigError as e:
    st.stop()  # Error already displayed in validate_api_keys

    chatgpt = LLM(model=Config.MODEL_NAME, temperature=Config.MODEL_TEMPERATURE, api_key=Config.OPENAI_API_KEY)

    # Input fields với security validation
    company_name = st.text_input("Nhập tên công ty:")
    if company_name:
        company_errors = InputValidator.validate_company_name(company_name)
        if company_errors:
            for error in company_errors:
                st.error(f"❌ {error}")
    
    meeting_objective = st.text_input("Mục đích cuộc họp:")
    if meeting_objective:
        objective_errors = InputValidator.validate_meeting_objective(meeting_objective)
        if objective_errors:
            for error in objective_errors:
                st.error(f"❌ {error}")
    
    attendees = st.text_area("Nhập người tham gia và vai trò của họ (một người mỗi dòng):")
    if attendees:
        attendees_errors = InputValidator.validate_attendees_list(attendees)
        if attendees_errors:
            for error in attendees_errors:
                st.error(f"❌ {error}")
    
    meeting_duration = st.number_input(
        "Nhập thời gian (phút):", 
        min_value=Config.MIN_MEETING_DURATION, 
        max_value=Config.MAX_MEETING_DURATION, 
        value=Config.DEFAULT_MEETING_DURATION, 
        step=Config.MEETING_DURATION_STEP
    )
    
    focus_areas = st.text_input("Nhập mục tiêu mà cần đạt được:")
    if focus_areas:
        # Validate focus areas length
        length_errors = Config.validate_input_lengths("", "", focus_areas)
        if length_errors:
            for error in length_errors:
                st.error(f"❌ {error}")
    
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

        # Tạo nhóm
        meeting_prep_crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=show_verbose,
            process=Process.sequential
        )

    # Chạy nhóm khi người dùng nhấp vào nút
    if st.button("🚀 Chuẩn bị cuộc họp", disabled=not all_fields_filled, type="primary"):
        # Hiển thị chi tiết agents trước khi bắt đầu
        display_agent_details()
        
        # Hiển thị fun facts
        display_fun_facts()
        
        # Chạy crew với progress display
        st.markdown("### 🚀 Tiến trình chuẩn bị cuộc họp")
        result = display_crew_progress(meeting_prep_crew, meeting_data)
        
        st.success("✅ Đã chuẩn bị xong cuộc họp!")
        st.markdown("---")
        st.markdown("### 📋 Kết quả chuẩn bị cuộc họp")
        st.markdown(result)
        
        # Lưu kết quả và tạo download button
        filename = save_meeting_result(result, company_name)
        st.info(f"📁 Kết quả đã được lưu vào file: {filename}")
        create_download_button(result, filename)

    # Hiển thị metrics dashboard
    display_metrics(meeting_duration, attendees, company_name)
    st.markdown("---")

    # Sidebar instructions and meeting history
    display_sidebar_instructions()
    display_meeting_history()

else:
    st.warning("Đang gặp vấn đề với API keys.")
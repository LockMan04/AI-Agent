"""
Tasks configuration for Meeting Preparation System
"""
from crewai import Task

def create_tasks(agents, meeting_data):
    """
    Tạo và cấu hình tất cả tasks cho hệ thống chuẩn bị cuộc họp
    
    Args:
        agents (dict): Dictionary chứa tất cả agents
        meeting_data (dict): Thông tin cuộc họp từ user input
    
    Returns:
        list: Danh sách các tasks
    """
    
    company_name = meeting_data['company_name']
    meeting_objective = meeting_data['meeting_objective']
    attendees = meeting_data['attendees']
    meeting_duration = meeting_data['meeting_duration']
    focus_areas = meeting_data['focus_areas']
    
    # Task 1: Phân tích bối cảnh
    context_analysis_task = Task(
        description=f"""
        QUAN TRỌNG: TẤT CẢ TRẢ LỜI HOÀN TOÀN BẰNG TIẾNG VIỆT
        
        Phân tích bối cảnh cuộc họp với {company_name}, xem xét:
        1. Mục tiêu cuộc họp: {meeting_objective}
        2. Người tham dự: {attendees}
        3. Thời lượng cuộc họp: {meeting_duration} phút
        4. Các lĩnh vực trọng tâm hoặc mối quan tâm cụ thể: {focus_areas}

        Nghiên cứu {company_name} kỹ lưỡng, bao gồm:
        1. Tin tức và thông cáo báo chí gần đây
        2. Các sản phẩm hoặc dịch vụ chính
        3. Các đối thủ cạnh tranh lớn

        Cung cấp bản tóm tắt toàn diện về các phát hiện của bạn, nêu bật thông tin phù hợp nhất cho bối cảnh cuộc họp.
        Định dạng đầu ra của bạn bằng markdown với các tiêu đề và tiêu đề phụ phù hợp.
        """,
        agent=agents['context_analyzer'],
        expected_output="Một phân tích chi tiết về bối cảnh cuộc họp và thông tin công ty, bao gồm các phát triển gần đây, hiệu suất tài chính và sự liên quan đến mục tiêu cuộc họp, được định dạng bằng markdown với các tiêu đề và tiêu đề phụ."
    )

    # Task 2: Phân tích ngành
    industry_analysis_task = Task(
        description=f"""
        QUAN TRỌNG: TẤT CẢ TRẢ LỜI HOÀN TOÀN BẰNG TIẾNG VIỆT
        
        Dựa trên phân tích bối cảnh cho {company_name} và mục tiêu cuộc họp: {meeting_objective}, cung cấp phân tích ngành chuyên sâu:
        1. Xác định các xu hướng và phát triển chính trong ngành
        2. Phân tích bối cảnh cạnh tranh
        3. Nêu bật các cơ hội và mối đe dọa tiềm năng
        4. Cung cấp thông tin chi tiết về vị trí thị trường

        Đảm bảo phân tích phù hợp với mục tiêu cuộc họp và vai trò của người tham dự.
        Định dạng đầu ra của bạn bằng markdown với các tiêu đề và tiêu đề phụ phù hợp.
        """,
        agent=agents['industry_insights_generator'],
        expected_output="Một báo cáo phân tích ngành toàn diện, bao gồm các xu hướng, bối cảnh cạnh tranh, cơ hội, mối đe dọa và thông tin chi tiết liên quan đến mục tiêu cuộc họp, được định dạng bằng markdown với các tiêu đề và tiêu đề phụ."
    )

    # Task 3: Phát triển chiến lược
    strategy_development_task = Task(
        description=f"""
        QUAN TRỌNG: TẤT CẢ TRẢ LỜI HOÀN TOÀN BẰNG TIẾNG VIỆT
        
        Sử dụng phân tích bối cảnh và thông tin chi tiết về ngành, phát triển chiến lược cuộc họp tùy chỉnh và chương trình chi tiết cho cuộc họp {meeting_duration} phút với {company_name}. Bao gồm:
        1. Một chương trình giới hạn thời gian với các mục tiêu rõ ràng cho từng phần
        2. Các điểm nói chuyện chính cho từng mục trong chương trình
        3. Người nói hoặc lãnh đạo được đề xuất cho từng phần
        4. Các chủ đề thảo luận và câu hỏi tiềm năng để thúc đẩy cuộc trò chuyện
        5. Các chiến lược để giải quyết các lĩnh vực trọng tâm và mối quan tâm cụ thể: {focus_areas}

        Đảm bảo chiến lược và chương trình phù hợp với mục tiêu cuộc họp: {meeting_objective}
        Định dạng đầu ra của bạn bằng markdown với các tiêu đề và tiêu đề phụ phù hợp.
        """,
        agent=agents['strategy_formulator'],
        expected_output="Một chiến lược cuộc họp chi tiết và chương trình giới hạn thời gian, bao gồm các mục tiêu, các điểm nói chuyện chính và các chiến lược để giải quyết các lĩnh vực trọng tâm cụ thể, được định dạng bằng markdown với các tiêu đề và tiêu đề phụ."
    )

    # Task 4: Tóm tắt điều hành
    executive_brief_task = Task(
        description=f"""
        QUAN TRỌNG: TẤT CẢ TRẢ LỜI HOÀN TOÀN BẰNG TIẾNG VIỆT
        
        Tổng hợp tất cả thông tin đã thu thập thành một bản tóm tắt điều hành toàn diện nhưng ngắn gọn cho cuộc họp với {company_name}. Tạo các thành phần sau:

        1. Một bản tóm tắt điều hành chi tiết một trang, bao gồm:
            - Tuyên bố rõ ràng về mục tiêu cuộc họp
            - Danh sách những người tham dự chính và vai trò của họ
            - Các điểm nền quan trọng về {company_name} và bối cảnh ngành liên quan
            - 3-5 mục tiêu chiến lược hàng đầu cho cuộc họp, phù hợp với mục tiêu
            - Tổng quan ngắn gọn về cấu trúc cuộc họp và các chủ đề chính sẽ được đề cập

        2. Danh sách chi tiết các điểm nói chuyện chính, mỗi điểm được hỗ trợ bởi:
            - Dữ liệu hoặc số liệu thống kê liên quan
            - Các ví dụ cụ thể hoặc nghiên cứu điển hình
            - Mối liên hệ với tình hình hiện tại hoặc thách thức của công ty

        3. Dự đoán và chuẩn bị cho các câu hỏi tiềm năng:
            - Liệt kê các câu hỏi có thể xảy ra từ những người tham dự dựa trên vai trò của họ và mục tiêu cuộc họp
            - Xây dựng các câu trả lời chu đáo, dựa trên dữ liệu cho từng câu hỏi
            - Bao gồm bất kỳ thông tin hỗ trợ hoặc bối cảnh bổ sung nào có thể cần thiết

        4. Các khuyến nghị chiến lược và các bước tiếp theo:
            - Cung cấp 3-5 khuyến nghị có thể hành động dựa trên phân tích
            - Phác thảo các bước tiếp theo rõ ràng để thực hiện hoặc theo dõi
            - Đề xuất các mốc thời gian hoặc thời hạn cho các hành động chính
            - Xác định các thách thức hoặc trở ngại tiềm năng và đề xuất các chiến lược giảm thiểu

        Đảm bảo bản tóm tắt toàn diện nhưng ngắn gọn, có khả năng hành động cao và phù hợp chính xác với mục tiêu cuộc họp: {meeting_objective}. Tài liệu nên được cấu trúc để dễ điều hướng và tham khảo nhanh trong cuộc họp.
        Định dạng đầu ra của bạn bằng markdown với các tiêu đề phụ phù hợp và tiêu đề chính (Dòng đầu tiên) không định dạng kiểu.
        """,
        agent=agents['executive_briefing_creator'],
        expected_output="Một bản tóm tắt điều hành toàn diện bao gồm tóm tắt, các điểm nói chuyện chính, chuẩn bị Q&A và các khuyến nghị chiến lược, được định dạng bằng markdown với các tiêu đề chính (H1), tiêu đề phần (H2) và tiêu đề phụ phần (H3) khi thích hợp. Sử dụng dấu đầu dòng, danh sách được đánh số và nhấn mạnh (in đậm/in nghiêng) cho thông tin chính."
    )

    return [
        context_analysis_task,
        industry_analysis_task,
        strategy_development_task,
        executive_brief_task
    ]

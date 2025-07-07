"""
AI Agents configuration for Meeting Preparation System
"""
from crewai import Agent
from crewai_tools import SerperDevTool

def create_agents(llm):
    """
    Tạo và cấu hình tất cả AI agents cho hệ thống chuẩn bị cuộc họp
    
    Args:
        llm: Language model instance
    
    Returns:
        dict: Dictionary chứa tất cả agents
    """
    
    search_tool = SerperDevTool()
    
    # Agent 1: Chuyên gia phân tích bối cảnh
    context_analyzer = Agent(
        role='Chuyên gia phân tích bối cảnh cuộc họp',
        goal='Phân tích và tóm tắt thông tin nền quan trọng cho cuộc họp',
        backstory='Bạn là một chuyên gia hiểu nhanh các bối cảnh kinh doanh phức tạp và xác định thông tin quan trọng.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool]
    )
    
    # Agent 2: Chuyên gia ngành
    industry_insights_generator = Agent(
        role='Chuyên gia ngành',
        goal='Cung cấp phân tích chuyên sâu về ngành và xác định các xu hướng chính',
        backstory='Bạn là một nhà phân tích ngành kỳ cựu với khả năng phát hiện các xu hướng và cơ hội mới nổi.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool]
    )
    
    # Agent 3: Chuyên gia chiến lược cuộc họp
    strategy_formulator = Agent(
        role='Chuyên gia chiến lược cuộc họp',
        goal='Phát triển chiến lược cuộc họp tùy chỉnh và chương trình chi tiết',
        backstory='Bạn là một bậc thầy lập kế hoạch cuộc họp, nổi tiếng với việc tạo ra các chiến lược và chương trình hiệu quả cao.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Agent 4: Chuyên gia truyền thông
    executive_briefing_creator = Agent(
        role='Chuyên gia truyền thông',
        goal='Tổng hợp thông tin thành các bản tóm tắt ngắn gọn và có tác động',
        backstory='Bạn là một chuyên gia truyền thông, có kỹ năng chắt lọc thông tin phức tạp thành các hiểu biết rõ ràng, dễ hành động.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    return {
        'context_analyzer': context_analyzer,
        'industry_insights_generator': industry_insights_generator,
        'strategy_formulator': strategy_formulator,
        'executive_briefing_creator': executive_briefing_creator
    }


import json
from dotenv import load_dotenv
from tools import call_gemini

load_dotenv()

# Định nghĩa logic cho Agent
def qa_agent(user_query):
  tools_prompt = f"""
    Bạn là một trợ lý AI có khả năng trả lời các câu hỏi, tìm kiếm thông tin trên web và ghi/đọc thông tin từ bộ nhớ

    Người dùng đưa ra yêu cầu: "{user_query}"

    Dựa vào yêu cầu này, hãy quyết định hành động tiếp theo:
    1. Nếu câu hỏi yêu cầu tìm kiếm thông tin (Ví dụ: Thủ đô Việt Nam?, Sương mù là gì?, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: search_google("Câu hỏi tìm kiếm")`
    2. Nếu người dùng muốn lưu thông tin (Ví dụ: Tên của tôi là Toàn, Tôi là một sinh viên Nguyễn Tất Thành, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: save_info("Key", "Thông tin cần lưu")`
    3. Nếu người dùng muốn đọc thông tin từ bộ nhớ (Ví dụ: Tên tôi là gì?, Tôi là sinh viên nào?, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: load_info("Key")`
    4. Nếu câu hỏi có thể trả lời trực tiếp bằng kiến thức chung của bạn, hoặc không thuộc các loại trên, hãy trả lời duy nhất một dòng với format: `ANSWER: Câu trả lời của bạn`
  """
  decision = call_gemini(tools_prompt)
  print(f'Gemini quyết định: {decision}')
  
  
# Chat với gemini
print('--- Chào một ngày tốt lành, Mimi có thể giúp gì cho bạn? ---')
print('Bạn có thể hỏi bất cứ điều gì, yêu cầu tìm kiếm, hoặc lưu/đọc thông tin.')
print('Gõ "exit" để thoát.')
while True:
    user_query = input('Bạn: ')
    if user_query.lower() == 'exit': # Dùng .lower() cho chuẩn
        print('Mimi tạm biệt bạn! Hẹn gặp lại :)))')
        break
    qa_agent(user_query)

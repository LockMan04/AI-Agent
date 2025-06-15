import json
import os
from google import genai
from dotenv import load_dotenv
from tools import call_gemini

load_dotenv()

# Định nghĩa logic cho Agent
def qa_agent(user_query):
  tools_prompt = f"""
    Bạn là một trợ lý AI có khả năng trả lời các câu hỏi, tìm kiếm thông tin trên web và ghi/đọc thông tin từ bộ nhớ

    Người dùng đưa ra yêu cầu: "{user_query}"

    Dựa vào yêu cầu này, hãy quyết định hành động tiếp theo:
    1. Nếu câu hỏi yêu cầu tìm kiếm thông tin mới hoặc thông tin cập nhật (Ví dụ: Thời tiết hôm nay thế nào?, Tin tức mới nhất, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: search("Câu hỏi tìm kiếm")`
    2. Nếu người dùng muốn lưu thông tin (Ví dụ: Tên của tôi là Toàn, Tôi là một sinh viên Nguyễn Tất Thành, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: save("Key", "Thông tin cần lưu")`
    3. Nếu người dùng muốn đọc thông tin từ bộ nhớ (Ví dụ: Tên tôi là gì?, Tôi là sinh viên nào?, ...), hãy chỉ trả lời duy nhất một dòng với format: `TOOL_CALL: load("Key")`
    4. Nếu câu hỏi có thể trả lời trực tiếp bằng kiến thức chung của bạn, hoặc không thuộc các loại trên, hãy trả lời duy nhất một dòng với format: `ANSWER: Câu trả lời của bạn`
  """
  decision = call_gemini(tools_prompt)
  print(f'Gemini quyết định: {decision}')
  
print('Chào một ngày tốt lành, tôi có thể giúp gì cho bạn?')
while True:
  user_query = input('Bạn: ')
  if user_query == 'exit':
    break
  qa_agent(user_query)
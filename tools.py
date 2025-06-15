import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import wikipedia as wiki

load_dotenv()
wiki.set_lang('vi') 
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
  raise ValueError('Không tìm thấy API, hãy thử lại')
print('Thành công lấy API Key từ .env')

# Cấu hình Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Hàm công cụ search_google
def wiki_search(query):
  s = wiki.search(query)
  if not s:
    return "Xin lỗi, mình không tìm thấy thông tin nào trên wiki liên quan đến yêu cầu của bạn."
  result = wiki.summary(s, sentences=3, auto_suggest=False)
  return result

DATA_FILE = 'user_data.json'
def save_info(key, value):
  try:
    if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
    else:
        data = {}
        
    data[key] = value
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return f'Tôi đã ghi nhớ rồi ạ'
  except Exception as e:
    print(f"[ERROR] Lỗi khi lưu thông tin: {e}")
    return "Có lỗi xảy ra khi lưu thông tin, vui lòng thử lại sau."
  
def load_info(key):
  try:
    if not os.path.exists(DATA_FILE):
        return "Chưa có thông tin nào được lưu trữ."
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if key in data:
        return data[key]
    else:
        return f"Xin lỗi nhưng có vẻ tôi đã quên rồi."
  except Exception as e:
    print(f"[ERROR] Lỗi khi đọc thông tin: {e}")
    return "Có lỗi xảy ra khi đọc thông tin, vui lòng thử lại sau."

AVAILABLE_TOOLS = {
    "wiki_search": wiki_search,
    "save_info": save_info,
    "load_info": load_info,
}

model_instance = genai.GenerativeModel(
  model_name='gemini-2.0-flash',
  tools=list(AVAILABLE_TOOLS.values()),
)

# Hàm gọi Gemini để xử lý prompt
def call_gemini(prompt_text: str):
  try:
    chat_session = model_instance.start_chat() 
    
    response = chat_session.send_message(prompt_text) 

    while True:
      if response.text: 
        return response.text
      
      elif response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = {k: v for k, v in function_call.args.items()}
                    
            if function_name in AVAILABLE_TOOLS:
                # Gọi hàm Python tương ứng
                try:
                    tool_output = AVAILABLE_TOOLS[function_name](**function_args)
                    # Gửi kết quả của công cụ trở lại Gemini
                    response = chat_session.send_message(
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={"result": tool_output} # Gemini mong đợi một dict với key 'result'
                            )
                        )
                    )
                except Exception as e:
                    tool_output = f"Lỗi khi thực thi công cụ '{function_name}': {e}"
                    print(f"[ERROR] {tool_output}")
                    # Nếu có lỗi, cũng báo cho Gemini biết
                    response = chat_session.send_message(
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={"result": tool_output}
                            )
                        )
                    )
            else:
                print(f"[ERROR] Công cụ '{function_name}' không được định nghĩa.")
                return f"Công cụ '{function_name}' không được định nghĩa."    
                  
      elif response.text:
        return response.text
      
      else:
        return "Xin lỗi, tôi không hiểu yêu cầu của bạn hoặc có lỗi xảy ra."

  
  except Exception as e:
    print('Error', e)
    return "Có vẻ mình không ổn rồi, thử lại sau nhé"


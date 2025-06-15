import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
  raise ValueError('Không tìm thấy API, hãy thử lại')
print('Thành công lấy API Key từ .env')
client = genai.Client(api_key=GEMINI_API_KEY)

# Hàm gọi Gemini để xử lý prompt
def call_gemini(prompt_text):
  try:
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt_text]
    )
    return response.text
  except Exception as e:
    print('Error', e)
    return "Có vẻ mình không ổn rồi, thử lại sau nhé"
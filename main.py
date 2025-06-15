import os
from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Lấy khóa API từ biến môi trường
genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Tạo model chat
model = genai.models(model="gemini-2.0-flash")

response = model.send_message("Việt Nam có bao nhiêu tỉnh thành?")
print(response.text)

# AI Meeting Preparation Agent 📝

## Mô tả đồ án
Ứng dụng AI Meeting Agent sử dụng công nghệ CrewAI để tự động chuẩn bị cuộc họp một cách chuyên nghiệp và toàn diện. Hệ thống multi-agent làm việc cùng nhau để phân tích, nghiên cứu và tạo ra các tài liệu chuẩn bị cuộc họp chi tiết.

## Tính năng chính
- 🤖 **Multi-Agent System**: 4 AI agents chuyên biệt làm việc cùng nhau
- 🔍 **Phân tích bối cảnh**: Tự động nghiên cứu thông tin công ty và ngành
- 📊 **Phân tích ngành**: Cung cấp insights về xu hướng và cạnh tranh
- 📋 **Chiến lược cuộc họp**: Tạo agenda và chiến lược tùy chỉnh
- 📄 **Executive Brief**: Tóm tắt điều hành với talking points chi tiết
- 💾 **Lưu trữ kết quả**: Lưu và quản lý lịch sử cuộc họp
- 📥 **Export**: Tải xuống kết quả dạng Markdown

## Kiến trúc hệ thống

### 4 AI Agents chuyên biệt:
1. **Context Analyzer** - Phân tích bối cảnh cuộc họp
2. **Industry Insights Generator** - Chuyên gia ngành
3. **Strategy Formulator** - Chuyên gia chiến lược
4. **Executive Briefing Creator** - Chuyên gia truyền thông

### Quy trình xử lý:
```
Input → Context Analysis → Industry Analysis → Strategy Development → Executive Brief → Output
```

## Cài đặt và chạy

### 1. Clone repository
```bash
git clone [repository-url]
cd AI-Meeting-Agent
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cấu hình API Keys
Tạo file `.env` và thêm:
```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

### 4. Chạy ứng dụng
```bash
streamlit run main.py
```

## Cách sử dụng
1. Mở ứng dụng trên browser
2. Nhập thông tin cuộc họp:
   - Tên công ty
   - Mục đích cuộc họp
   - Danh sách người tham gia
   - Thời lượng cuộc họp
   - Các lĩnh vực trọng tâm
3. Nhấn "Chuẩn bị cuộc họp"
4. Chờ AI agents xử lý (2-3 phút)
5. Xem kết quả và tải xuống file

## Công nghệ sử dụng
- **Frontend**: Streamlit
- **AI Framework**: CrewAI
- **LLM**: OpenAI GPT-4o-mini
- **Search**: SerperDev API
- **Language**: Python 3.8+

## Cấu trúc thư mục
```
AI-Meeting-Agent/
├── main.py              # File chính
├── config.py            # Cấu hình và settings
├── agents.py            # Định nghĩa AI agents
├── tasks.py             # Định nghĩa các tasks
├── utils.py             # Utility functions
├── requirements.txt     # Dependencies với version cụ thể
├── README.md            # Tài liệu
└── .env                 # API keys (cần tạo)
```

## Đóng góp
Đây là đồ án chuyên ngành, mọi góp ý và cải thiện đều được hoan nghênh.

## Tác giả
**Toàn Thành** - Sinh viên chuyên ngành AI

## License
MIT License

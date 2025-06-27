from langchain.tools import Tool
from datetime import datetime
import wikipedia

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Lưu dữ liệu nghiên cứu có cấu trúc vào tệp văn bản.",
)

def search_wikipedia(query: str) -> str:
    try:
        results = wikipedia.search(query, results=5)
        if not results:
            return "No relevant Wikipedia articles found."
        
        summaries = []
        for title in results:
            page = wikipedia.page(title)
            summaries.append(f"**{title}**: {page.summary[:500]}...")  # Limit summary length
        
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error fetching Wikipedia data: {str(e)}"
    
wiki_tool = Tool(
    name="search_wikipedia",
    func=search_wikipedia,
    description="Tìm kiếm các bài viết có liên quan trên Wikipedia và trả về bản tóm tắt.",
)

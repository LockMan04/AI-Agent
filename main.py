from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import save_tool, wiki_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    
  
llm = ChatOpenAI(model_name="gpt-4o-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Bạn là một trợ lý nghiên cứu sẽ giúp tạo ra một bài nghiên cứu.
            
            QUAN TRỌNG - Cách sử dụng tools:
            - save_info: Cần 1 tham số key và value. Ví dụ: save_info(name="Toàn)
            - load_info: Cần 1 tham số key. Ví dụ: load_info(key="name")  
            - list_user_info: Không cần tham số. Ví dụ: list_info()
            
            Trả lời truy vấn của người dùng và sử dụng các công cụ cần thiết.
            Gói đầu ra ở định dạng này và không cung cấp văn bản nào khác\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})
print(raw_response)


try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)
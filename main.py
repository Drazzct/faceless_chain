from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("HF_TOKEN")

model = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    model="Qwen/Qwen3.5-9B",
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Bạn là một trợ lý xuất sắc"),
    ("human", "{input}")
])


class ChatState(TypedDict):
    messages: list

def chatbot(state: ChatState):
    formatted = prompt.format_messages(input=state["messages"][-1]["content"])

    response = model.invoke(formatted)

    return {
        "messages": state["messages"] + [
            {"role": "assistant", "content": response.content}
        ]
    }


builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot)
builder.set_entry_point("chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

messages = []

while True:
    user_input = input("User: ")

    if user_input == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    result = graph.invoke({"messages": messages})

    messages = result["messages"]

    print("AI:", messages[-1]["content"])

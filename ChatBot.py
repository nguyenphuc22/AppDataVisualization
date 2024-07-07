from typing import Protocol

class ChatbotInterface(Protocol):
    def generate_response(self, app_context) -> str:
        ...

class OpenAIChatbot:
    # Add API KEY HERE
    api_key = "YOUR_API_KEY"
    def generate_response(self, app_context) -> str:
        # Example response using app_context's titlePage and content
        # TODO: Chị xử lý api ở đây nhé, toàn class này luôn
        response = f"Welcome to {app_context.titlePage}. {app_context.content} \n Câu hỏi của bạn là ${app_context.prompt}"
        return response
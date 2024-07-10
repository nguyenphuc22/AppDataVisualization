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
        response = (f"Chào mừng tới với trang web {app_context.titlePage}. \n \n"
                    f" {app_context.content} \n \n"
                    f" {app_context.hyphothesisTitle} \n \n"
                    f" {app_context.hyphothesisContent} \n \n"
                    f" Câu hỏi của bạn là {app_context.prompt}"
                    )
        return response
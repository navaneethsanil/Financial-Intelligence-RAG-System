from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Data model representing a request to the chat system.

    Attributes:
        query (str): The user input or query sent to the AI chatbot.
    """

    query: str


class ChatResponse(BaseModel):
    """
    Data model representing a response from the chat system.

    Attributes:
        ai_response (str): The generated response from the AI based on the input query.
    """

    ai_response: str

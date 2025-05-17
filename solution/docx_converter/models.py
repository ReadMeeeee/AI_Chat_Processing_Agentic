from pydantic import BaseModel


class Message(BaseModel):
    sender: str
    text: str


class Chat(BaseModel):
    messages: list[Message]
    name: str = None
    numbers: list[str] | set[str] = None


class CompanyChat(BaseModel):
    company: str
    whole_chat: str

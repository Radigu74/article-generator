from pydantic import BaseModel

class TopicRequest(BaseModel):
    keywords: str
    num_topics: int = 7

class ArticleRequest(BaseModel):
    topic: str
    tone: str
    length: int  # word count target

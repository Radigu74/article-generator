from sqlalchemy.orm import Session
from schemas import TopicRequest, ArticleRequest  # ✅

def get_client_by_key(db: Session, key: str):
    return db.query(Client).filter(Client.api_key == key).first()

def log_usage(db: Session, client_id: int, tokens: float):
    usage = Usage(client_id=client_id, tokens=tokens)
    db.add(usage)
    db.commit()

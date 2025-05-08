import os
from dotenv import load_dotenv, find_dotenv
import openai
from fastapi import FastAPI, Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.auth import api_key_auth
from crud import log_usage
from models import Base
from schemas import TopicRequest, ArticleRequest

# ─── Load and Override .env ─────────────────────────────────────────────────
env_path = find_dotenv()
load_dotenv(env_path, override=True)

# ─── Debug Prints (remove in production) ───────────────────────────────────
print("→ cwd:", os.getcwd())
print("→ DATABASE_URL  :", repr(os.getenv("DATABASE_URL")))
print("→ LOCAL_DATABASE_URL:", repr(os.getenv("LOCAL_DATABASE_URL")))

# ─── Promote LOCAL_DATABASE_URL to DATABASE_URL if defined ────────────────
local = os.getenv("LOCAL_DATABASE_URL")
if local:
    os.environ["DATABASE_URL"] = local
    print("→ Overrode DATABASE_URL with LOCAL_DATABASE_URL")

# ─── Validate that we now actually have a DATABASE_URL ──────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please check .env or LOCAL_DATABASE_URL.")

# ─── OpenAI Key ─────────────────────────────────────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env.")

# ─── Database Setup ────────────────────────────────────────────────────────
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# ─── FastAPI App & Dependency ──────────────────────────────────────────────
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── Your endpoints (example) ──────────────────────────────────────────────
@app.post("/api/topics")
async def gen_topics(
    body: TopicRequest,
    request: Request,
    db=Depends(get_db),
    auth=Depends(api_key_auth),
):
    prompt = f"Keywords: {body.keywords}. Generate {body.num_topics} distinct topics."
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    log_usage(db, request.state.client.id, resp.usage.total_tokens)
    return {"topics": resp.choices[0].message.content}

@app.post("/api/articles")
async def gen_article(body: ArticleRequest, request: Request, db=Depends(get_db), auth=Depends(api_key_auth)):
    prompt = f"Topic: {body.topic}. Tone: {body.tone}. Write ~{body.length} words..."
    resp = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"user","content":prompt}])
    tokens = resp.usage.total_tokens
    log_usage(db, request.state.client.id, tokens)
    return {"article": resp.choices[0].message.content}

@app.get("/api/usage")
async def usage(request: Request, db=Depends(get_db), auth=Depends(api_key_auth)):
    usages = db.query(Usage).filter(Usage.client_id==request.state.client.id).all()
    return {"usage": sum(u.tokens for u in usages)}

import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".env"
)

print("🔍 Attempting to load .env from:", ENV_PATH)

loaded = load_dotenv(ENV_PATH)
print("🔍 load_dotenv returned:", loaded)
print("🔍 ENCRYPTION_KEY value:", os.getenv("ENCRYPTION_KEY"))
print("🔍 FASTROUTER_MODEL:", os.getenv("FASTROUTER_MODEL"))



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.generate_tasks import router as generate_tasks_router
from app.api.push_to_jira import router as push_to_jira_router
from app.api.auth import router as auth_router
from app.api import jira
from app.api.pipeline import router as pipeline_router

# DB
from app.db.base import Base
from app.db.session import engine

# 🔑 IMPORTANT: load all models
from app.db import models  # noqa: F401

app = FastAPI(title="PRD → Jira Backend")

# ----------------------------
# Create DB tables (MVP mode)
# ----------------------------

Base.metadata.create_all(bind=engine)

# ----------------------------
# CORS CONFIG
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Routes
# ----------------------------

app.include_router(auth_router)
app.include_router(generate_tasks_router)
app.include_router(push_to_jira_router)
app.include_router(jira.router)
app.include_router(pipeline_router)

# ----------------------------
# Health check
# ----------------------------

@app.get("/")
def root():
    return {"status": "ok", "service": "PRD → Jira Backend"}

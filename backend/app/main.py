import os

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

# Load models so SQLAlchemy registers them
from app.db import models  # noqa: F401


app = FastAPI(
    title="PRD → Jira Backend",
    version="1.0.0"
)

# ----------------------------
# CORS CONFIG
# ----------------------------
# For now allow all (safe for MVP)
# Lock this to Netlify domain later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# DATABASE (MVP MODE)
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# ROUTES
# ----------------------------
app.include_router(auth_router)
app.include_router(generate_tasks_router)
app.include_router(push_to_jira_router)
app.include_router(jira.router)
app.include_router(pipeline_router)

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "PRD → Jira Backend"
    }

FlowForge

FlowForge is a product execution tool that converts raw Product Requirement Documents (PRDs) into structured Jira work items using AI, and allows teams to preview, review, and push those tasks directly into Jira.

The goal of FlowForge is simple: reduce the gap between product thinking and execution.


---

What FlowForge Does

FlowForge helps product teams go from idea to execution faster by:

Taking a raw PRD or product idea as input

Converting it into structured Epics and Stories

Letting users preview and validate generated tasks

Pushing approved tasks directly into Jira

Displaying Jira issues in a Kanban-style board

Allowing basic workflow transitions (Backlog → In Progress → Done)


The system is designed to stay strictly aligned with the PRD — no hallucinated features, no generic task templates.


---

Core Features

PRD → Task Generation

Accepts free-form product descriptions or PRDs

Uses AI to extract:

Core features

User flows

Technical requirements

Constraints and edge cases


Outputs structured Epics and Stories with clear intent


Jira Integration

Secure Jira connection using API tokens

Create issues, subtasks, and comments

Fetch issues by project

Transition issues across workflow states

View Jira data in a Kanban layout


Task Preview

Generated tasks are reviewed before pushing

No automatic Jira writes without user confirmation

Clear separation between generation and execution



---

Tech Stack

Frontend

React (Vite)

Tailwind CSS

Modular component architecture

API-driven state management


Backend

FastAPI (Python)

SQLAlchemy + SQLite (local)

JWT-based authentication

Encrypted storage for sensitive tokens

REST-based Jira API integration


AI / LLM

OpenRouter API

Model configurable via environment variables

Strict prompting to prevent feature hallucination



---

Project Structure

flowforge_test/
├── frontend/        # React + Vite frontend
├── backend/         # FastAPI backend
├── README.md


---

Environment Variables

Create a .env file inside the backend/ directory.

# Jira (single system user)
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token

# AI / LLM
FASTROUTER_API_KEY=your_openrouter_api_key
FASTROUTER_MODEL=openai/gpt-4o-mini

# Security
ENCRYPTION_KEY=base64_encoded_key
SECRET_KEY=your_app_secret

> Note:
.env files should never be committed to version control.




---

Running Locally

Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000

Frontend

cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173


---

Deployment

Frontend

Deployed on Netlify

Static build via Vite


Backend

Deployed on Render

Long-running FastAPI service

Environment variables configured via Render dashboard



---

Design Philosophy

PRD-first execution — no assumptions, no filler tasks

Human-in-the-loop — preview before Jira writes

Minimal UI, maximum clarity

Single source of truth: Jira


FlowForge is not trying to replace product thinking — it’s designed to amplify it.


---

Status

Backend: ✅ Live

Frontend: ✅ Live

Jira integration: ✅ Working

AI task generation: ✅ Working

Authentication: ✅ Single-user system

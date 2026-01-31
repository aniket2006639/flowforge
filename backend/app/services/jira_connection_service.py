import requests
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models.jira_connection import JiraConnection
from app.core.security import encrypt_secret

def validate_jira_credentials(site_url: str, email: str, token: str):
    url = f"{site_url}/rest/api/3/myself"

    response = requests.get(
        url,
        auth=(email, token),
        timeout=10
    )

    if response.status_code != 200:
        raise Exception("Invalid Jira credentials")

def connect_jira(db: Session, user_id: str, site_url: str, email: str, token: str):

    validate_jira_credentials(site_url, email, token)

    encrypted = encrypt_secret(token)

    existing = db.query(JiraConnection).filter(
        JiraConnection.user_id == user_id
    ).first()

    if existing:
        existing.site_url = site_url
        existing.jira_email = email
        existing.encrypted_token = encrypted
        existing.updated_at = datetime.utcnow()
    else:
        existing = JiraConnection(
            user_id=user_id,
            site_url=site_url,
            jira_email=email,
            encrypted_token=encrypted
        )
        db.add(existing)

    db.commit()

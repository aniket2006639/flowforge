import requests
from sqlalchemy.orm import Session
from collections import defaultdict

from app.db.models.jira_connection import JiraConnection
from app.core.security import decrypt_secret
from app.utils.adf import text_to_adf


# ----------------------------------------------------
# INTERNAL: connection helper
# ----------------------------------------------------

def _get_connection(db: Session, user_id: str) -> JiraConnection:
    conn = db.query(JiraConnection).filter(
        JiraConnection.user_id == user_id
    ).first()

    if not conn:
        raise Exception("Jira not connected")

    return conn


# ----------------------------------------------------
# FETCH ISSUES
# ----------------------------------------------------

def fetch_issues(db: Session, user_id: str, project: str):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/search/jql"

    params = {
        "jql": f'project = "{project}"',
        "fields": "summary,status,parent",
        "maxResults": 50
    }

    response = requests.get(
        url,
        auth=(conn.jira_email, token),
        params=params,
        timeout=10
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(f"Jira API error: {data}")

    issues = []

    for issue in data.get("issues", []):
        parent = issue["fields"].get("parent")

        issues.append({
            "key": issue.get("key"),
            "title": issue["fields"].get("summary"),
            "status": issue["fields"]["status"].get("name"),
            "parent": parent["key"] if parent else None
        })

    return issues


# ----------------------------------------------------
# FETCH PROJECTS
# ----------------------------------------------------

def fetch_projects(db: Session, user_id: str):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/project"

    response = requests.get(
        url,
        auth=(conn.jira_email, token),
        timeout=10
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(f"Jira API error: {data}")

    return [
        {"key": p.get("key"), "name": p.get("name")}
        for p in data
    ]


# ----------------------------------------------------
# CREATE SINGLE ISSUE (internal)
# ----------------------------------------------------

def create_issue(
    db: Session,
    user_id: str,
    project: str,
    title: str,
    description: str,
    issue_type: str = "Task",
    parent_key: str | None = None
):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue"

    fields = {
        "project": {"key": project},
        "summary": title,
        "description": text_to_adf(description),
    }

    if parent_key:
        fields["parent"] = {"key": parent_key}
        fields["issuetype"] = {"name": "Sub-task"}
    else:
        fields["issuetype"] = {"name": issue_type}

    payload = {"fields": fields}

    response = requests.post(
        url,
        json=payload,
        auth=(conn.jira_email, token),
        timeout=10
    )

    data = response.json()

    if response.status_code not in (200, 201):
        raise Exception(f"Jira create error: {data}")

    return {
        "key": data.get("key"),
        "id": data.get("id")
    }


# ----------------------------------------------------
# BULK CREATE (parent + subtasks)
# ----------------------------------------------------

def bulk_create_issues(
    db: Session,
    user_id: str,
    project: str,
    tasks: list
):

    created = []

    for task in tasks:

        parent_result = create_issue(
            db=db,
            user_id=user_id,
            project=project,
            title=task["title"],
            description=task.get("description", ""),
            issue_type=task.get("type", "Task")
        )

        parent_key = parent_result["key"]

        subtask_keys = []

        for subtask in task.get("subtasks", []):
            sub = create_issue(
                db=db,
                user_id=user_id,
                project=project,
                title=subtask.get("title", ""),
                description=subtask.get("description", ""),
                parent_key=parent_key
            )
            subtask_keys.append(sub["key"])

        created.append({
            "parent": parent_key,
            "subtasks": subtask_keys
        })

    return created


# ----------------------------------------------------
# UPDATE ISSUE
# ----------------------------------------------------

def update_issue(
    db: Session,
    user_id: str,
    issue_key: str,
    title: str | None,
    description: str | None
):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue/{issue_key}"

    fields = {}

    if title is not None:
        fields["summary"] = title

    if description is not None:
        fields["description"] = text_to_adf(description)

    payload = {"fields": fields}

    response = requests.put(
        url,
        json=payload,
        auth=(conn.jira_email, token),
        timeout=10
    )

    if response.status_code not in (200, 204):
        raise Exception(response.text)

    return {"updated": issue_key}


# ----------------------------------------------------
# TRANSITIONS
# ----------------------------------------------------

def get_transitions(db: Session, user_id: str, issue_key: str):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue/{issue_key}/transitions"

    response = requests.get(
        url,
        auth=(conn.jira_email, token),
        timeout=10
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(data)

    return [
        {"id": t["id"], "name": t["name"]}
        for t in data.get("transitions", [])
    ]


def transition_issue(db, user_id, issue_key, transition_id):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue/{issue_key}/transitions"

    payload = {"transition": {"id": transition_id}}

    response = requests.post(
        url,
        json=payload,
        auth=(conn.jira_email, token),
        timeout=10
    )

    if response.status_code not in (200, 204):
        raise Exception(response.text)

    return {"moved": issue_key}


# ----------------------------------------------------
# COMMENTS
# ----------------------------------------------------

def add_comment(db, user_id, issue_key, text):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue/{issue_key}/comment"

    payload = {"body": text_to_adf(text)}

    response = requests.post(
        url,
        json=payload,
        auth=(conn.jira_email, token),
        timeout=10
    )

    data = response.json()

    if response.status_code not in (200, 201):
        raise Exception(data)

    return {"comment_id": data.get("id"), "issue": issue_key}


# ----------------------------------------------------
# DELETE ISSUE
# ----------------------------------------------------

def delete_issue(db, user_id, issue_key):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/issue/{issue_key}"

    response = requests.delete(
        url,
        auth=(conn.jira_email, token),
        timeout=10
    )

    if response.status_code not in (200, 204):
        raise Exception(response.text)

    return {"deleted": issue_key}


# ----------------------------------------------------
# KANBAN BOARD
# ----------------------------------------------------

def get_kanban_board(db, user_id, project):

    issues = fetch_issues(db, user_id, project)

    board = defaultdict(list)

    for issue in issues:
        board[issue["status"]].append(issue)

    return {
        "project": project,
        "columns": board
    }


# ----------------------------------------------------
# BATCH MOVE
# ----------------------------------------------------

def batch_move_issues(db, user_id, moves):

    results = []

    for move in moves:

        issue_key = move["issue"]
        target_status = move["to"]

        transitions = get_transitions(db, user_id, issue_key)

        match = next(
            (t for t in transitions if t["name"].lower() == target_status.lower()),
            None
        )

        if not match:
            results.append({
                "issue": issue_key,
                "status": "failed",
                "reason": "transition not found"
            })
            continue

        try:
            transition_issue(db, user_id, issue_key, match["id"])
            results.append({
                "issue": issue_key,
                "status": "moved",
                "to": target_status
            })
        except Exception as e:
            results.append({
                "issue": issue_key,
                "status": "failed",
                "reason": str(e)
            })

    return {"results": results}


# ----------------------------------------------------
# WORKFLOW METADATA
# ----------------------------------------------------

def get_workflow_metadata(db, user_id, project):

    conn = _get_connection(db, user_id)
    token = decrypt_secret(conn.encrypted_token)

    url = f"{conn.site_url}/rest/api/3/project/{project}/statuses"

    response = requests.get(
        url,
        auth=(conn.jira_email, token),
        timeout=10
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(data)

    statuses = set()

    for issue_type in data:
        for s in issue_type.get("statuses", []):
            statuses.add(s["name"])

    return {
        "project": project,
        "statuses": [{"name": s} for s in sorted(statuses)]
    }
def create_issue_with_subtasks(
    db: Session,
    user_id: str,
    project: str,
    title: str,
    description: str,
    issue_type: str,
    subtasks: list | None
):
    # Create parent issue
    parent = create_issue(
        db=db,
        user_id=user_id,
        project=project,
        title=title,
        description=description,
        issue_type=issue_type
    )

    parent_key = parent["key"]
    created_subtasks = []

    # Create subtasks if provided
    if subtasks:
        for s in subtasks:
            sub = create_issue(
                db=db,
                user_id=user_id,
                project=project,
                title=s["title"],
                description=s["description"],
                parent_key=parent_key
            )
            created_subtasks.append(sub["key"])

    return {
        "parent": parent_key,
        "subtasks": created_subtasks
    }

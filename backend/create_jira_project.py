import base64
import requests

email = "31240571@vupune.ac.in"          # ✅ your email
api_token = "ATATT3xFfGF0N_-a25xRlPGc3x4bAeRBpAQTObEWNcJAeYNMa-yVro37NJB3bIJ5Jfa4eW5WjYY2syq3erxyxoInli6uVRSwPBS3teSiYPQz9IZyfuxHNRaXMkrtphpZxTM1uhiBbSCtEOdX1__-fhHMxodioCVBG2D-clHjFtw2PRyyR8qTfp4=F52E018F"      # ❗ paste the token you generated
domain = "yuktix.atlassian.net"

ACCOUNT_ID = "712020:d86cc211-7bde-44ee-be70-913dd91b3dd3"

auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "key": "YUK",
    "name": "Yuktix Core",
    "projectTypeKey": "software",
    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-kanban-template",
    "leadAccountId": ACCOUNT_ID
}

response = requests.post(
    f"https://{domain}/rest/api/3/project",
    headers=headers,
    json=payload
)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)

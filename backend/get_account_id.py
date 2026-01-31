import base64
import requests

email = "31240571@vupune.ac.in"
api_token = "ATATT3xFfGF0N_-a25xRlPGc3x4bAeRBpAQTObEWNcJAeYNMa-yVro37NJB3bIJ5Jfa4eW5WjYY2syq3erxyxoInli6uVRSwPBS3teSiYPQz9IZyfuxHNRaXMkrtphpZxTM1uhiBbSCtEOdX1__-fhHMxodioCVBG2D-clHjFtw2PRyyR8qTfp4=F52E018F"
domain = "yuktix.atlassian.net"

auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()

r = requests.get(
    f"https://{domain}/rest/api/3/myself",
    headers={
        "Authorization": f"Basic {auth}",
        "Accept": "application/json"
    }
)

print(r.status_code)
print(r.json())

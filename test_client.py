import requests as rq

URL = "http://127.0.0.1:8000/api/user-view"

data = {
    "user_id": "testUser1"
}

response = rq.get(URL, data=data)

print(response.json())
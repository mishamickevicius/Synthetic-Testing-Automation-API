import requests as rq

URL = "http://127.0.0.1:8000/api/element-grab"

data = {
    "target_url": "https://website-status-checker-v1.web.app/"
}

response = rq.post(url=URL, data=data)

print(response.json())
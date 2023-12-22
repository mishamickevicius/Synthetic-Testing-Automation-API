import requests as rq

# Get Test

URL = "http://127.0.0.1:8000/api/user-view"

data = {
    "user_id": "testUser1"
}

response = rq.get(URL, data=data)

print(response.json())

# Delete Test

# data = {
#     'user_id': 'delete_this_user'
# }

# response = rq.delete(URL, data=data)
# print(response.status_code)

# Post Test
data = {
    "user_id":"testUser3"
}

response = rq.post(URL, data=data)
print("Post Response Code : ", response.status_code)
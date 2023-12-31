import requests as rq
import base64

# Get Test

URL = "http://127.0.0.1:8000/api/main-website-test"
# URL = "http://127.0.0.1:8000/api/test-group-view?test_group_name=Test Group 2&user_id=testUser2"

# data = {
#     "user_id": "testUser2",
#     "test_group_name":"Test Group 2"
# }

# response = rq.get(URL + "?user_id=testUser1&test")

# print(response.json())

# # Delete Test

# data = {
#     'user_id': 'testUser2',
#     'test_group_name':"API Test Group 2",
#     'test_id': '3'
# }

# response = rq.delete(URL, data=data)
# print(response.status_code)

# Post Test

data = {
    "user_id":"testUser2",
    "test_type":"group",
    "group_name":"Test Group 2"
}
# with open("/home/dude/Desktop/Projects/CyberSecurity Project/Synthetic-Testing-Automation/url_test_list.txt", 'rb') as file:
#     file_content = file.read()  # Read the file content as bytes
#     data["file"] = base64.b64encode(file_content).decode('utf-8')

response = rq.post(URL, data=data)
response_data = response.json()

count = 1

for url in list(response_data.keys()):
    if response_data[url] is None:
        continue
    else: 
        try:
            image_bytes = base64.b64decode(response_data[url].pop('screenshot_encoded'))
            with open(f"website_screenshot_{count}.png", "wb") as img:
                img.write(image_bytes)
            count += 1
        except KeyError:
            print("Key Error Happened")



print(response_data)




print("Image Saved")

print("Post Response Code : ", response.status_code)

# Patch Test

# data = {
#     "user_id":"testUser1",
#     "name":"Test Group 1",
#     'target': 'file'
# }

# with open("/home/dude/Desktop/Projects/CyberSecurity Project/Synthetic-Testing-Automation/url_test_list_3.txt", 'rb') as file:
#     file_content = file.read()  # Read the file content as bytes
#     data["change_value"] = base64.b64encode(file_content).decode('utf-8')

# response = rq.patch(URL, data=data)
# print("Patch Response Code : ", response.status_code)
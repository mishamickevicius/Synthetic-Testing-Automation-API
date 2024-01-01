import requests as rq
import base64

URL = "http://127.0.0.1:8000/api/"

# Make User 

# data = {
#     'user_id': 'FinalTestUser'
# }

# response = rq.post(URL + "user-view", data=data)

# print("User Post Response Code: ", response.status_code)

# response = rq.get(URL + "user-view?user_id=FinalTestUser")
# print(response.json())

# Make Test Group 

# data = {
#     'user_id': 'FinalTestUser',
#     'group_name':'FinalTestGroup',
# }

# with open("/home/dude/Desktop/Projects/CyberSecurity Project/Synthetic-Testing-Automation/final_test_list.txt", 'rb') as file:
#     file_content = file.read()  # Read the file content as bytes
#     data["file"] = base64.b64encode(file_content).decode('utf-8')

# r = rq.post(URL + "test-group-view", data=data)
# print("Test Group Post Response Code: ", r.status_code, "\n\n")

# r = rq.get(URL + "test-group-view?user_id=FinalTestUser&test_group_name=FinalTestGroup")
# print(r.json())

# Run Tests 

data = {
    "user_id":"FinalTestUser",
    "test_type":"group",
    "group_name":"FinalTestGroup"
}

response = rq.post(URL + 'main-website-test', data=data)
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
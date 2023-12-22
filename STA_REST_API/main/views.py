from .models import TestGroupModel, TestResultModel
from .serializers import TestGroupSerializer, TestResultSerializer

from django.contrib.auth.models import User, Group

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from selenium import webdriver
from selenium.webdriver.common.by import By


# Create your views here.
class UserView(APIView):
    """
    This class will handle all requests when it comes to users, such as
    getting info about user(GET), making a new user(POST), and 
    deleting the current logged in user (DELETE).
    """
    def get(self, request):
        # Gets the Test Groups and Previous Tests that corresponds to the user in the DB
        try:
            data = dict(request.data)
            # The user ID from Firebase /// Will be the username in django
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data["user_id"][0] 
            user = User.objects.get(username=user_id)
            groups = list(TestGroupModel.objects.filter(user=user)) # Get the test group of this user
            ran_tests = []
            for g in groups: # For each group, add all tests that have been run by the user to 'ran_tests'
                tests = list(TestResultModel.objects.filter(test_group=g, user=user))
                if len(tests) > 0:
                    for t in tests:
                        ran_tests.append(t)
                else:
                    continue
            d = {"user_id":user.username, "groups":[], "ran_tests":[]} # This is the final response dict
            for g in groups: # Loop through all groups and serialize data and add it to output_data
                data = TestGroupSerializer(g).data
                data['user'] = user_id
                d["groups"].append(data)
            for t in ran_tests: # Loop through all tests and serialize data and add to output_data
                data = TestResultSerializer(t).data
                data['user'] = user_id
                d["ran_tests"].append(data)
            return Response(data=d,status=200) 
        
        except Exception as err:
            print(err)
            return Response(data={"error": "User not found."}, status=404)
        
    def delete(self, request):
        # Deletes user that is given. 
        try:
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data["user_id"][0] 
            user = User.objects.get(username=user_id)
            user.delete()
            return Response(status=204)
        except Exception as err:
            print(err)
            return Response(data={"Error":"Failed to delete user"}, status=500)
        
    def post(self, request):
        try: 
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data["user_id"][0] 
            user = User.objects.create_user(username=user_id, password="mm374321",)
            user.save()
            # Add user to Group (default group will be created when a new user is added)
            group = Group.objects.get(name='Users')
            group.user_set.add(user)
            return Response({"Status": "User Created"}, status=204)
        except Exception as err:
            print("Error creating new user", err)
            return Response({"Error":"Something Went Wrong"}, status=500)


class WebsiteTest(APIView):
    """
    A class that has all the functions to get the different types of 
    data needed and has functions for get and post to handle requests.
    """

    # This is to save space and time for me.


@api_view(['POST'])
def webpage_screenshot(request):
    """
    This endpoint will allow the user to input a URL using the (target_url) id
    and it will return a png file of a screen shot of the website
    """
    # Put data from call into var
    data = dict(request.data)

    # Check what type the input of target_url is and set it to a var
    if isinstance(data['target_url'], list):
        target = data['target_url'][0]
    elif isinstance(data['target_url'], str):
        target = str(data['target_url'])
    else:
        # Return error if not a list or string
        return Response({'error': 'Invalid URL'}, status=400)
    
    # Set a webdriver
    driver = webdriver.Chrome()
    try:
        # Try to get the target and grab a tag from the target
        driver.get(target)
        title = driver.title
        # Make screenshot
        img = driver.get_screenshot_as_file("Backend_API/main/screenshots/test1.png")
        if img == False:
            return Response({"Error": "Couldn't take screenshot"}, status=500)
    except Exception as err:
        print(err)
        return Response({'error':'Page not found'}, status=400)
    return Response({
        "target": target,
        "pageTitle": title
    })
from .models import TestGroupModel, TestResultModel
from .serializers import TestGroupSerializer, TestResultSerializer

import base64
import time
import re

from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from selenium import webdriver
from selenium.webdriver.common.by import By


# Create your views here.
class UserView(APIView):
    """
    This class will handle all requests when it comes to users, such as
    getting info about user(GET), making a new user(POST), and 
    deleting the current logged in user (DELETE).
    """
    def get(self, request: Request):
        # Gets the Test Groups and Previous Tests that corresponds to the user in the DB
        try:
            # data = dict(request.data)
            # The user ID from Firebase /// Will be the username in django
            user_id = request.query_params.get('user_id', None)
            if user_id is None:
                return Response({'error': 'Missing parameters'}, status=400)
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
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data['user_id'][0] 
            user = User.objects.get(username=user_id)
            user.delete()
            return Response(status=204)
        except Exception as err:
            print(err)
            return Response(data={"Error":"Failed to delete user"}, status=500)
        
    def post(self, request):
        try: 
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data['user_id'][0] 
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
    API view that has all the functions to get the different types of 
    data needed and has functions for get and post to handle requests.
    Getting Information about a past scan(GET), Running a scan(POST), and
    Deleting a past scan(DELETE)
    """

    def get(self, request: Request):
        try:
            # data = dict(request.data)
            user_id = request.query_params.get('user_id', None)
            test_group_name = request.query_params.get('test_group_name', None) 

            if test_group_name is None or user_id is None:
                return Response({'error': 'Missing parameters'}, status=400)
            
            test_group = TestGroupModel.objects.filter(name=test_group_name, user=user).first()
            user = User.objects.get(username=user_id)
            if test_group is None:
                return Response({'error': f'No test group with name {test_group_name}'}, status=400)
            else:
                ran_tests = []
                tests = list(TestResultModel.objects.filter(test_group=test_group, user=user))
                if len(tests) > 0:
                    for t in tests:
                        ran_tests.append(t)
                else:
                    return Response({'status': f'No Ran Tests'}, status=200)
                d = {"user_id":user.username, "ran_tests":[]}
                for t in ran_tests: # Loop through all tests and serialize data and add to output_data
                    data = TestResultSerializer(t).data
                    data['user'] = user_id
                    d["ran_tests"].append(data)
                return Response(d, status=200)
                
        except Exception as err:
            print(err)
            return Response({'error':'Error with request'},status=500)
    

    def delete(self, request):
        # ! Be Careful with ID for frontend on this endpoint
        # ! Id is not user based 
        try:
            data = dict(request.data)
            test_id = int(data['test_id']) if isinstance(data['test_id'], str) else int(data['test_id'][0] )
            test = TestResultModel.objects.get(id=test_id)
            test.delete()
            return Response(status=204)
        except Exception as err:
            print(err)
            return Response({'error':'Error with request'},status=500)


    def separate_urls(self, errors:list):
        url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+\.com(/.*)'
        matches = []

        for error in errors:
            e = error['message']
            finds = re.findall(url_regex, e)
            for found_url in finds:
                # Replace the found URL with an empty string to get the string without the URL
                modified_string = re.sub(found_url, '', e)
                matches.append((found_url, modified_string.strip()))  # Strip removes any leading/trailing whitespace
        
        return matches

    def website_test(self, target):
        # * Return the results as a json object
        try:
            driver = webdriver.Chrome()
            start_time = time.time()
            driver.get(target)
            end_time = time.time()
            time.sleep(3)

            errors_list = []

            
            logs = driver.get_log('browser')
            for entry in logs:
                if entry['level'] == 'SEVERE':
                    entry.pop('timestamp')
                    entry.pop('level')
                    errors_list.append(entry)
                    # print(entry)
            

            separated_urls = self.separate_urls(errors_list)
            print(separated_urls)
            driver.close()
            print(f"Load Time ----> {end_time - start_time}")
            return {
                "run_time":round(end_time - start_time, 2),
                "errors":errors_list
                }
        except Exception as err:
            print(err)
            return None

    def post(self, request):
        # Run The Test function according to inputs 
        try:
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data['user_id'][0] 
            user = User.objects.get(username=user_id)
            test_type = data['test_type'] if isinstance(data['test_type'], str) else data['test_type'][0] 
            if test_type == 'group':
                group_name = data['group_name']
                group = TestGroupModel.objects.filter(name=group_name, user=user).first()
                if group is None:
                    return Response({'error': f'No test group with name {group_name}'}, status=400)  
                ## !!! This is where we loop through URLS and run test function through threads
            elif test_type == 'single':
                target_url = data['target_url'] if isinstance(data['target_url'], str) else data['target_url'][0] 
                test_results = self.website_test(target=target_url)
                if test_results is None:
                    return Response({'error': "Invalid Url"}, status=400)
                return Response({"results": test_results}, status=200)
        except Exception as err:
            print(err)
            return Response({'error':'Error with request'},status=500)



class TestGroupView(APIView):
    """
    API view that will handle requests related to the test groups set 
    by users. This will include getting info about a test group(GET), 
    adding new groups(POST), deleting groups(DELETE), and changing groups(PATCH)
    """
    def get(self, request: Request):
        try:
            # data = dict(request.data)
            group_name = request.query_params.get('test_group_name', None)
            user_id = request.query_params.get('user_id', None)
            
            if group_name is None or user_id is None:
                return Response({'error': 'Missing parameters'}, status=400)
            
            user = User.objects.get(username=user_id)
            test_group = TestGroupModel.objects.filter(user=user, name=group_name).first() 
            serializer = TestGroupSerializer(test_group)
            return Response(serializer.data)
        except Exception as err:
            print(err)
            return Response({'error':'Error with request'},status=500)
    
    def post(self, request):
        try:
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data['user_id'][0] 
            user = User.objects.get(username=user_id)
            group_name = data['name'] if isinstance(data['name'], str) else data['name'][0] 
            # Check if the name already is used
            check = TestGroupModel.objects.filter(name=group_name, user=user).first()
            if check is not None:
                return Response({"Status": "Name already taken"}, status=400)
            else:
                file = data['file'] if isinstance(data['file'], str) else data['file'][0] 
                decoded_file = base64.b64decode(file).decode("utf-8").split("\n")
                # Create a new instance of the model and save it in the database
                new_group = TestGroupModel(name=group_name, user=user, file_data=decoded_file)
                new_group.save()
                return Response(status=204)

        except Exception as err:
            print(err)
            return Response({'error': 'Error with request'}, status=500)
    def delete(self, request):
        try:
            data = dict(request.data)
            user_id = data['user_id'] if isinstance(data['user_id'], str) else data['user_id'][0] 
            group_name = data['test_group_name'] if isinstance(data['test_group_name'], str) else data['test_group_name'][0] 
            user = User.objects.get(username=user_id)
            test_group = TestGroupModel.objects.filter(user=user, name=group_name).first() 
            test_group.delete()
            return Response(status=204)
        except Exception as err:
            print(err)
            return Response({'error': 'Error with request'}, status=500)

    def patch(self, request):
        try:
            data = dict(request.data)
            user_id = data["user_id"] if isinstance(data['user_id'], str) else data['user_id'][0] 
            user = User.objects.get(username=user_id)
            group_name = data['name'] if isinstance(data['name'], str) else data['name'][0] 
            # The request will have a target which should be either name or file.
            target = data['target'] if isinstance(data['target'], str) else data['target'][0] 
            # The request will also have a value which the selected field will be changed to
            change_value = data['change_value'] if isinstance(data['change_value'], str) else data['change_value'][0] 
            test_group = TestGroupModel.objects.get(user=user, name=group_name)
            if target == 'name':
                test_group.name = change_value
                test_group.save()
                return Response(status=204)
            elif target == 'file':
                file = data['change_value'] if isinstance(data['change_value'], str) else data['change_value'][0] 
                decoded_file = base64.b64decode(file).decode("utf-8").split("\n")
                test_group.file_data = decoded_file
                test_group.save()
                return Response(status=204)


        except Exception as err:
            print(err)
            return Response({'error':'User ID missing or invalid.'}, status=400)
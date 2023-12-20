from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create your views here.


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
        return JsonResponse({'error': 'Invalid URL'}, status=400)
    
    # Set a webdriver
    driver = webdriver.Chrome()
    try:
        # Try to get the target and grab a tag from the target
        driver.get(target)
        title = driver.title
        # Make screenshot
        img = driver.get_screenshot_as_file("Backend_API/main/screenshots/test1.png")
        if img == False:
            return JsonResponse({"Error": "Couldn't take screenshot"}, status=500)
    except Exception as err:
        print(err)
        return JsonResponse({'error':'Page not found'}, status=400)
    return JsonResponse({
        "target": target,
        "pageTitle": title
    })
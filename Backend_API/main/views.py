from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create your views here.


@api_view(['POST'])
def element_grab(request):
    data = dict(request.data)
    target = str(data['target_url'])

    driver = webdriver.Chrome()
    try:
        driver.get(target)
        title = driver.title
    except Exception as err:
        print(err)
        return JsonResponse({'error':'Page not found'}, status=404)
    return JsonResponse({
        "target": target,
        "pageTitle": title
    })
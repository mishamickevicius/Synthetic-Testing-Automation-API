from django.urls import path
from .views import webpage_screenshot
urlpatterns = [
    path('webpage-screenshot', webpage_screenshot)
]
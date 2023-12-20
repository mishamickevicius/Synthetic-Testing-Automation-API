from django.urls import path
from . import views
urlpatterns = [
    path("webpage-screenshot", views.webpage_screenshot)
    ]
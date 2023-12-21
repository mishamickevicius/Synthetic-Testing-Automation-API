from django.urls import path
from . import views
urlpatterns = [
    path('webpage-screenshot', views.webpage_screenshot),
    path('main-website-test', views.WebsiteTest.as_view()),
    path('user-view', views.UserView.as_view())
]
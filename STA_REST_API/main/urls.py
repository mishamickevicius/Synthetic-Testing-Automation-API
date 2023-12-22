from django.urls import path
from . import views
urlpatterns = [
    path('main-website-test', views.WebsiteTest.as_view()),
    path('user-view', views.UserView.as_view()),
    path('test-group-view', views.TestGroupView.as_view())
]
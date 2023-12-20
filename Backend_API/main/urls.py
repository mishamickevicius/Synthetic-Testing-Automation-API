from django.urls import path
from .views import element_grab
urlpatterns = [
    path('element-grab', element_grab)
]
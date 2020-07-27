from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("brian", views.brian),
    path("<str:name>", views.greet, name="greet")
]
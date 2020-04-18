from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("signin", views.sign_in),
    path("register", views.register),
    path("process_login", views.process_login),
    path("process_registration", views.process_registration),
    path("logoff", views.logoff),
]
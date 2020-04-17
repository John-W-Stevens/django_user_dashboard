from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("/add_user", views.add_user),
    path("/process_new_user", views.process_new_user),
    path("/edit_user/<int:id>", views.edit_user),
    path("/profile", views.load_profile),
    path("/update/<int:id>", views.process_profile_update),
    path("/delete/<int:id>", views.process_profile_deletion),
]
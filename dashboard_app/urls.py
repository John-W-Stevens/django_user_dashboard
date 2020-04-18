from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path("/add_user", views.load_add_user_page),
    path("/process_new_user", views.process_new_user),
    path("/edit_profile/<int:profile_id>", views.load_edit_profile_page),
    path("/update_profile/<int:profile_id>", views.process_profile_update),
    path("/delete_profile/<int:id>", views.process_profile_deletion),
]
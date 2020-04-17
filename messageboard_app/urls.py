from django.urls import path
from . import views

urlpatterns = [
    path("/<int:id>", views.message_board),
    path("/<int:profile_id>/post_message", views.post_message),
    path("/<int:profile_id>/<int:message_id>/comment", views.post_comment),
]
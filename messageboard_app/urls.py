from django.urls import path
from . import views

urlpatterns = [
    path("/<int:id>", views.message_board),
    path("/<int:profile_id>/post_message", views.post_message),
    path("/<int:profile_id>/<int:message_id>/comment", views.post_comment),
    path("/edit/<int:message_id>", views.edit_message),
    path("/delete/<int:message_id>", views.delete_message),
    path("/edit/comment/<int:comment_id>", views.edit_comment),
    path("/delete/comment/<int:comment_id>", views.delete_comment),
]
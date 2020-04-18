from django.db import models
from login_and_registration_app.models import User
# Create your models here.

class MessageManager(models.Manager):
    def message_validations(request, postData):
        errors = {}
        if postData["message"] == "":
            errors["message"] = "Cannot submit empty messages."
        return errors

class CommentManager(models.Manager):
    def comment_validations(request, postData):
        errors = {}
        if postData["comment"] == "":
            errors["comment"] = "Cannot submit empty comments."
        return errors

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    author = models.ForeignKey(User, related_name="messages_posted", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="messages_received", on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    edited_by = models.IntegerField(default=0)
    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    edited_by = models.IntegerField(default=0)
    objects = CommentManager()


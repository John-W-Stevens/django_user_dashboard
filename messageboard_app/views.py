from django.shortcuts import render, redirect
from login_and_registration_app.models import User
from . import models

# Create your views here.
def message_board(request, id):

    profile = User.objects.filter(id=id)[0]
    user = User.objects.filter(id=int(request.session["user_id"]))[0]

    context = {
        "user": user,
        "profile": profile,
        "messages_posted": user.messages_posted.all().order_by("-created_at"),
        "messages_received": profile.messages_received.all().order_by("-created_at"),
    }
    return render(request, "message_board.html", context)

def post_message(request, profile_id):
    author = User.objects.filter(id=int(request.session["user_id"]))[0]
    profile = User.objects.filter(id=profile_id)[0]
    message = models.Message.objects.create(content=request.POST["message"], author=author, recipient=profile)
    
    return redirect(f"/message_board/{profile_id}")

def post_comment(request, profile_id, message_id):
    author = User.objects.filter(id=int(request.session["user_id"]))[0]
    profile = User.objects.filter(id=profile_id)[0]
    message = models.Message.objects.filter(id=message_id)[0]
    comment = models.Comment.objects.create(content=request.POST["comment"], author=author, message=message)
    
    return redirect(f"/message_board/{profile_id}")

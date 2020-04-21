from django.shortcuts import render, redirect
from login_and_registration_app.models import User
from . import models


def logged_user(request):
    return User.objects.filter(id=request.session["user_id"])[0]

# Create your views here.
def message_board(request, id):

    profile = User.objects.filter(id=id)[0]
    user = logged_user(request)
    
    try:
        errors = request.session["errors"]
    except KeyError:
        errors = None

    context = {
        "user": user,
        "profile": profile,
        "errors": errors,
        "messages_posted": user.messages_posted.all().order_by("-created_at"),
        "messages_received": profile.messages_received.all().order_by("-created_at"),
    }
    request.session["errors"] = None

    return render(request, "message_board.html", context)

def post_message(request, profile_id):
    author = logged_user(request)
    profile = User.objects.filter(id=profile_id)[0]

    # handle errors
    errors = models.Message.objects.message_validations(request.POST)    
    if len(errors) > 0:
        request.session["errors"] = errors
        return redirect(f"/message_board/{profile_id}")

    message = models.Message.objects.create(content=request.POST["message"], author=author, recipient=profile)
    return redirect(f"/message_board/{profile_id}")


def post_comment(request, profile_id, message_id):
    #modified with ajax
    author = logged_user(request)
    profile = User.objects.filter(id=profile_id)[0]
    message = models.Message.objects.filter(id=message_id)[0]

    comment = models.Comment.objects.create(content=request.POST["comment"], author=author, message=message) 
    comment.save()   
    context = {
        "user": logged_user(request),
        "message": message
    }
    return render(request, "comments.html", context)



def delete_message(request, message_id):
    message = models.Message.objects.filter(id=message_id)[0]
    user = logged_user(request)
    profile_id = message.recipient.id # the user's wall where the message is displayed

    if user == message.author or user.level == 9:
        message.delete()

    return redirect(f"/message_board/{profile_id}")

def delete_comment(request, comment_id):
    comment = models.Comment.objects.filter(id=comment_id)[0]
    user = logged_user(request)
    profile_id = comment.message.recipient.id # the user's wall where the comment is displayed

    if user == comment.author or user.level == 9:
        comment.delete()

    return redirect(f"/message_board/{profile_id}")

def edit_message(request, message_id):
    user = logged_user(request)
    message = models.Message.objects.filter(id=message_id)[0]
    profile_id = message.recipient.id # the user's wall where the message is displayed

    message.content = request.POST["edited_message"]
    message.edited = True
    message.save()

    return redirect(f"/message_board/{profile_id}")

def edit_comment(request, comment_id):
    user = logged_user(request)
    comment = models.Comment.objects.filter(id=comment_id)[0]
    profile_id = comment.message.recipient.id # the user's wall where the message is displayed

    comment.content = request.POST["edited_comment"]
    comment.edited = True
    comment.save()

    return redirect(f"/message_board/{profile_id}")
from django.shortcuts import render, redirect
from . import models
import bcrypt

def logged_user(request):
    return models.User.objects.filter(id=request.session["user_id"])[0]

def initialize_session(request):
    try:
        request.session["user_id"]
    except KeyError:
        request.session["user_id"] = None

def index(request):
    initialize_session(request)
    if request.session["user_id"] == None:
        context = {}
    else:    
        context = {
            "user": logged_user(request),
        }
    return render(request, "index.html", context)

def sign_in(request):

    try:
        errors = request.session["errors"]
    except KeyError:
        errors = None

    if request.session["user_id"] == None:
        context = {
            "user": "none",
            "errors": errors,
        }
    else:
        context = {
            "user": logged_user(request),
            "errors": errors,
        }
    request.session["errors"] = None

    return render(request, "sign_in.html", context)

def process_login(request):

    # handle errors
    errors = models.User.objects.login_validations(request.POST)    
    if len(errors) > 0:
        request.session["errors"] = errors
        return redirect("/signin")
    # login user
    else:
        request.session["user_id"] = models.User.objects.filter(email=request.POST["email"])[0].id
        return redirect("/dashboard")

def register(request):

    try:
        errors = request.session["errors"]
    except KeyError:
        errors = None

    if request.session["user_id"] == None:
        context = {
            "user": "none",
            "errors": errors,
        }
    else:
        context = {
            "user": logged_user(request),
            "errors": errors,
        }
    request.session["errors"] = None

    return render(request, "register.html", context)

def process_registration(request):

    errors = models.User.objects.registration_validations(request.POST)
    if len(errors) > 0:
        request.session["errors"] = errors
        return redirect("/register")

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    pw_confirm = request.POST["pw_confirm"]

    # use bcrypt to secure password
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # create new user
    new_user = models.User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)
    
    if len(models.User.objects.all()) == 1:
        new_user.level = 9 # make the first user an administrator    
    new_user.save()

    # log the user in with session
    request.session["user_id"] = new_user.id

    # direct the user to the the dashboard
    return redirect("/dashboard")

def logoff(request):
    del request.session["user_id"]
    return redirect("/")
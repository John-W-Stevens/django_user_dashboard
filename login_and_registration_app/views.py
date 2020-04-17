from django.shortcuts import render, redirect
from . import models
import bcrypt

def initialize_session(request):
    try:
        request.session["user_id"]
    except KeyError:
        request.session["user_id"] = None

def index(request):
    initialize_session(request)
    context = {}
    return render(request, "index.html", context)

def signin(request, errors=None):
    context = {"errors": errors}
    return render(request, "sign_in.html", context)

def process_login(request):

    # handle errors
    errors = models.User.objects.login_validations(request.POST)    
    if len(errors) > 0:
        return signin(request, errors=errors)
    # login user
    else:
        request.session["user_id"] = models.User.objects.filter(email=request.POST["email"])[0].id
        return redirect("/")

def register(request, errors=None):
    context = {"errors": errors}
    return render(request, "register.html", context)

def process_registration(request):

    errors = models.User.objects.registration_validations(request.POST)
    if len(errors) > 0:
        return register(request, errors=errors)

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    pw_confirm = request.POST["pw_confirm"]
    print(request.POST)

    # use bcrypt to secure password
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # create new user
    new_user = models.User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)
    new_user.save()

    # log the user in with session
    request.session["user_id"] = new_user.id

    # direct the user to the the dashboard
    return redirect("/")

def logoff(request):
    del request.session["user_id"]
    return redirect("/")
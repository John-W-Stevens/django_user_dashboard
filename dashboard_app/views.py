from django.shortcuts import render, redirect
from login_and_registration_app.models import User
import bcrypt

# Create your views here.
def dashboard(request):
    context = {
        "user": User.objects.filter(id=int(request.session["user_id"]))[0],
        "users": User.objects.all(),
    }
    return render(request, "dashboard.html", context)

def add_user(request, errors=None):
    user = User.objects.filter(id=int(request.session["user_id"]))[0]
    if user.level == 9:
        context = {"errors": errors}
        return render(request, "add_user.html", context)
    return redirect("/dashboard")

def process_new_user(request):

    errors = User.objects.registration_validations(request.POST)
    if len(errors) > 0:
        return add_user(request, errors=errors)
    
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    
    # use bcrypt to secure password
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # create new user
    new_user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)

    try:
        request.POST["admin"]
        new_user.level = 9
    except KeyError:
        new_user.level = 1

    new_user.save()

    return redirect("/dashboard")

def load_profile(request, errors=None):
    # current user
    user = User.objects.filter(id=int(request.session["user_id"]))[0]

    context = {
        "user": user,
        "profile": user,
        "errors": errors,
    }
    print(errors)
    return render(request, "profile.html", context)

def edit_user(request, id, errors=None):
    user = User.objects.filter(id=int(request.session["user_id"]))[0]

    if user.level != 9: # prevent access to this url for non-admins
        return redirect("/dashboard")

    context = {
        "user": user,
        "profile": User.objects.filter(id=id)[0],
        "errors": errors,
        }
    print(errors)
    return render(request, "profile.html", context)

def process_profile_update(request, id):
    """ This function handles all three forms coming from profile.html 
        It handles these forms differently based on whether a user is editing their own profile
        of an administrator is editing another user's profile 
        
        Input: id -> the profile id being updated """
    # input validation    
    errors = User.objects.update_profile_validations(request.POST, id)
    user = User.objects.filter(id=id)[0]

    # Form 1 (updates to first_name, last_name, email, and/or user_level)
    if len(request.POST) >= 4: 
        # return errors
        if len(errors) > 0:
            if id == int(request.session["user_id"]):
                return load_profile(request, errors=errors) # load_profile() returned if user is editing their own profile
            else:
                return edit_user(request, id, errors=errors) # edit_user() returned if admin is editing another user's profile
        # no errors, so update profile
        else:
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            if len(request.POST) == 5: # (an admin is editing the profile)
                if request.POST["user_level"] == "admin":
                    user.level = 9
            user.save()

    # Form 2 (update to profile password)
    elif len(request.POST) == 3:
        # return errors
        if len(errors) > 0:
            if id == int(request.session["user_id"]):
                return load_profile(request, errors=errors) # load_profile() returned if user is editing their own profile
            else:
                return edit_user(request, id, errors=errors) # edit_user() returned if admin is editing another user's profile
        # no errors, so update profile
        else:
            password = request.POST["password"]
            user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.save()

    # Form 3 (update to profile description)
    else:
        # no input validation so just update profile
        user.description = request.POST["description"]
        user.save()
        return load_profile(request) # only user's can modify their own profiles so return load_profile()

    if id == int(request.session["user_id"]):
        return load_profile(request) # load_profile() returned if user is editing their own profile
    else:
        return edit_user(request, id) # edit_user() returned if admin is editing another user's profile


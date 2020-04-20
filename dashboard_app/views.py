from django.shortcuts import render, redirect
from login_and_registration_app.models import User
import bcrypt

def display_post(request):
    print("..........................")
    print("Printing data from request.POST.......")
    for k,v in request.POST.items():
        print(f"Key: {k}, Value: {v}")
    print("..........................")
    print("Printing data from request.FILES.......")
    if request.FILES == {}:
        print("No files uploaded")
    else:
        for k,v in request.FILES.items():
            print(f"Key: {k}, Value: {v}")
    print("..........................")


def logged_user(request):
    return User.objects.filter(id=request.session["user_id"])[0]

def dashboard(request):

    # Handles an administrator deleting their own account
    try:
        User.objects.filter(id=request.session["user_id"])[0]
    except IndexError:
        return redirect("/")

    context = {
        "user": logged_user(request),
        "users": User.objects.all(),
    }
    return render(request, "dashboard.html", context)

def load_add_user_page(request):

    user = logged_user(request)
    if user.level != 9:
        return redirect("/dashboard")

    try:
        errors = request.session["errors"]
    except KeyError:
        errors = None

    context = {
        "user": user,
        "errors": errors,
    }

    request.session["errors"] = None

    return render(request, "add_user.html", context)

def process_credentials(request):
    # restrict access to anyone who isn't an admin
    display_post(request)
    if logged_user(request).level != 9:
        return redirect("/dashboard")
    if "add_user" in request.POST and User.objects.confirm_credentials(request.session, request.POST):
        return redirect("/dashboard/add_user")

    if "edit_user" in request.POST and User.objects.confirm_credentials(request.session, request.POST):
        profile_id = request.POST["profile_id"]
        return redirect(f"/dashboard/edit_profile/{profile_id}")
    
    if "delete_user" in request.POST:
        print("Wow")

    else:
        return redirect("/dashboard")


def process_new_user(request):
    # print(request.POST)

    errors = User.objects.registration_validations(request.POST)
    if len(errors) > 0:
        request.session["errors"] = errors
        return redirect("/dashboard/add_user")
    
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

def process_profile_deletion(request, id):
    # restrict access to this url for none-administrators
    if logged_user(request).level != 9:
        return redirect("/dashboard")

    if User.objects.confirm_credentials(request.session, request.POST):
        user = User.objects.get(id=id)
        user.delete()

    return redirect("/dashboard")
    
def process_profile_update(request, profile_id):
    # display_post(request)
    user = logged_user(request)
    profile = User.objects.filter(id=profile_id)[0]

    # restrict access to editing profiles to admin and profile owners
    if user.level != 9 and user != profile:
        return redirect("/dashboard")

    errors = User.objects.update_profile_validations(request.POST, profile_id)
    if len(errors) > 0:
        request.session["errors"] = errors
        return redirect(f"/dashboard/edit_profile/{profile_id}")
    
    # update profile
    profile.first_name = request.POST["first_name"]
    profile.last_name = request.POST["last_name"]
    profile.email = request.POST["email"]
    
    if request.POST["password"] != "":
        profile.password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

    if user != profile:
        if request.POST["user_level"] == "Admin":
            profile.level = 9
        else:
            profile.level = 1

    if request.POST["city"] != "":
        profile.city = request.POST["city"]
    if request.POST["state"] != "":
        profile.state = request.POST["state"]
    if request.POST["country"] != "":
        profile.country = request.POST["country"]

    if request.FILES != {}:
        # delete the old profile image
        profile.profile_photo.delete()
        # change the user's profile image
        profile.profile_photo = request.FILES["profile_image_upload"]

    profile.description = request.POST["description"]
    profile.save()



    return redirect(f"/dashboard/edit_profile/{profile_id}")

def load_edit_profile_page(request, profile_id):

    """ Loads edit_profile page """
    user = logged_user(request)
    profile = User.objects.filter(id=profile_id)[0]
    
    # restrict access to editing profiles to admin and profile owners
    if user.level != 9 and user != profile:
        return redirect("/dashboard")
    
    try:
        errors = request.session["errors"]
    except KeyError:
        errors = None

    context = {
        "user": user,
        "profile": profile,
        "errors": errors
    }
    request.session["errors"] = None

    return render(request, "profile.html", context)
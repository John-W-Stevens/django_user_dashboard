from django.db import models
import re
import datetime
import bcrypt

class UserManager(models.Manager):
    def registration_validations(self,postData):
        errors = {}

        # first_name
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "must have 2 or more letters"
        if len(postData["first_name"]) >= 2 and not postData["first_name"].isalpha():
            errors["first_name"] = "must only contain letters"
        
        # last_name
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "must have 2 or more letters"
        if len(postData["last_name"]) >= 2 and not postData["last_name"].isalpha():
            errors["last_name"] = "must only contain letters"
        
        # email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.filter(email=postData["email"]):
            errors["email"] = "This user already has an account"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
            
        # password
        if len(postData["password"]) < 8:
            errors["password"] = "must be 8 or more characters"
        if postData["password"] != postData["pw_confirm"]:
            errors["pw_confirm"] = "Passwords need to match"
        return errors
    
    def login_validations(self, postData):
        errors = {}
        users = User.objects.filter(email=postData["email"])

        if not users:
            errors["email"] = "Invalid email address"
            return errors
        else:
            pw = postData["password"]
            if not bcrypt.checkpw(pw.encode(), users[0].password.encode()):
                errors["password"] = "Invalid password"
        return errors
        
    def update_profile_validations(self, postData, id):
        # id is the profile ID
        user = User.objects.filter(id=id)[0]
        errors = {}

        # Updates made to user email, first_name, and/or last_name
        if len(postData) >= 4:
            
            new_email = postData["email"]
            if new_email != user.email:
                # make sure new email is valid
                EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                if not EMAIL_REGEX.match(postData['email']): # test whether a field matches the pattern            
                    errors['email'] = "Invalid email address!"
                # make sure email account isn't already registered
                if "email" not in errors:
                    for profile in User.objects.all():
                        if profile.email == new_email:
                            errors["email"] = "This account is already registered"
                            break

            first_name = postData["first_name"]
            if first_name != user.first_name:
                if len(postData["first_name"]) < 2:
                    errors["first_name"] = "must have 2 or more letters"
                if len(postData["first_name"]) >= 2 and not postData["first_name"].isalpha():
                    errors["first_name"] = "must only contain letters"

            last_name = postData["last_name"]
            if last_name != user.last_name:
                if len(postData["last_name"]) < 2:
                    errors["last_name"] = "must have 2 or more letters"
                if len(postData["last_name"]) >= 2 and not postData["last_name"].isalpha():
                    errors["last_name"] = "must only contain letters"
        
        # Updates made to user password
        if len(postData) == 3:
            # update user password
            if len(postData["password"]) < 8:
                errors["password"] = "must be 8 or more characters"
            if postData["password"] != postData["pw_confirm"]:
                errors["pw_confirm"] = "Passwords need to match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    description = models.TextField(null=True)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = UserManager()

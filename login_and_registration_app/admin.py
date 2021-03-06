from django.contrib import admin
from django.urls import path, include

# Register your models here.
from login_and_registration_app.models import User

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

# ****************
urlpatterns = [
# Your app's urls is lined to the project
    path('admin/',admin.site.urls),
    path('login_and_registration_app/', include('login_and_registration_app.urls')),
]
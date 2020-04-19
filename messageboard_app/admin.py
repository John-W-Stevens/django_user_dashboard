from django.contrib import admin
from django.urls import path, include

# Register your models here.
from messageboard_app.models import Message, Comment

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

# ****************
urlpatterns = [
# Your app's urls is lined to the project
    path('admin/',admin.site.urls),
    path('messageboard/', include('messageboard_app.urls')),
]
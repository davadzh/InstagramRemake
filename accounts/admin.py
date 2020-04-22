from django.contrib import admin
from .models import Publication, Profile_info, Notification, Comment

# Register your models here.

admin.site.register(Publication)
admin.site.register(Profile_info)
admin.site.register(Notification)
admin.site.register(Comment)

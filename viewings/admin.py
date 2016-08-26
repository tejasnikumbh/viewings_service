from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Viewing)
admin.site.register(models.Conversation)
admin.site.register(models.User)
admin.site.register(models.Office)
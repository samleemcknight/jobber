from django.contrib import admin
from .models import Event, Category, Profile, Photo
# Register your models here.
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Photo)
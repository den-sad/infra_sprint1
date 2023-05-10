from django.contrib import admin

# Register your models here.
from .models import Cat, Achievement

admin.site.register(Cat)
admin.site.register(Achievement)

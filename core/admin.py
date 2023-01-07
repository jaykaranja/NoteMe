from django.contrib import admin

from core.models import Category, Task

# Register your models here.

admin.site.register(Task)
admin.site.register(Category)
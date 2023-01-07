from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        id = f"{self.id}"
        return id
    

    
class Task(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    
    def __str__(self):
        name = self.content
        return name
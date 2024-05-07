from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    todo_title = models.CharField(max_length=100)
    todo_description = models.CharField(max_length=1000)
    is_completed = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self) -> str:
        return f"Username: {self.user.username} Todo title: {self.todo_title}"


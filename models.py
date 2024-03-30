from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def get_user():
    return get_user_model().objects.get(username='ishan').id
class Todo(models.Model):
    title = models.CharField(max_length=200)
    task = models.TextField()
    completed=models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    creator=models.ForeignKey(User,on_delete=models.CASCADE,default=get_user)
 
    def __str__(self):
        return self.title

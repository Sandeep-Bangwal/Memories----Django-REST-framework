from django.db import models
from account.models import User

class Posts(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200) 
    video = models.FileField(upload_to="videos", blank=True)
    images =  models.ImageField(upload_to="images", blank=True)

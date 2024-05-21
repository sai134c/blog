from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    images = models.ManyToManyField('PostAttachment')
    time_stamp = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self) -> str:
        return f"{self.author.username}'s - {self.time_stamp.date()}"

class PostAttachment(models.Model):
    image = models.ImageField(upload_to='post_att/')

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
      title = models.CharField(max_length=32)
      timestamp = models.DateTimeField(auto_now_add=True)
      user_id = models.IntegerField()
      image = models.FileField(upload_to='user-image-upload/', blank=True)
      text = models.CharField(max_length=16384, blank=True)

class Like(models.Model):
      user_id = models.IntegerField()
      post_id = models.IntegerField()
      timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
      user_id = models.IntegerField()
      post_id = models.IntegerField()
      text = models.CharField(max_length=128)
      timestamp = models.DateTimeField(auto_now_add=True)






from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from numpy import real


class User(AbstractUser):
    pass



class Post(models.Model):
    """Post contains all the info about a post
        - User who posted
        - Content of the post itself
        - date and time of the post
        - Likes (0 for first)
    """

    id = models.AutoField(primary_key = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    content = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.creator} created a Post on {self.date}"
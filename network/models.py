from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


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
        return f"User: {self.creator} created a Post on {self.content}"

    # make the serialize function to acess the items values in python 
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content, 
            "date" : self.date, 
            "likes" : self.likes
        }


class Follower(models.Model):
    """Display who is followign whom
        - Follower :
        - Followed
    """
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"User: {self.follower} follows User: {self.followed}"
    
    def is_valid_follower(self):
        return self.follower != self.followed


class Liked(models.Model):
    """Save who liked whose Post
    """

    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="liker")
    
    def __str__(self):
        return f"${self.post} was liked by ${self.user}"
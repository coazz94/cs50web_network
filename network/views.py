from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

# https://cs50.harvard.edu/web/2020/projects/4/network/

def index(request):

    # Get all the posts in of the db
    posts = Post.objects.all()

    return render(request, "network/index.html", {
        "posts" : posts, 
        "user_id" : request.user.id
    })


def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request):

    # get the content from the textarea with the name post    
    content = request.POST.get("post")

    # Create the user instance
    user = User.objects.get(id = request.user.id)
    # Create the post in the db
    new_post = Post(creator=user, content=content)
    new_post.save()
    
    # redirect in the end to the index page
    return HttpResponseRedirect(reverse("index"))



def user_page(request, user_id):

    """Profilepage should display
        - number of followers
        - number of user following
        - posts in reverse order
        - other users, show follow unfollow button 
    """

    return render(request, "network/user_page.html")
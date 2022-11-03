import json
from asyncio.streams import FlowControlMixin
from tkinter.messagebox import NO
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from requests import request
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import *

# https://cs50.harvard.edu/web/2020/projects/4/network/

def index(request):

    # Get all the posts in of the db sort them by date (- is descending)
    posts = Post.objects.all().order_by("-date")
    
    # Filter for the posts liked by this user
    likes = Liked.objects.filter(user=request.user.id)
    liked_posts = []

    # Add the post ids in a list
    for like in likes:
        liked_posts.append(like.post.id)


    # Make the paginator class, set to 3 posts per site
    p = Paginator(posts, 3)
    page_number = request.GET.get("page")
    posts = p.get_page(page_number)


    return render(request, "network/index.html", {
        "posts" : posts, 
        "user_id" : request.user.id, 
        "liked_posts" : liked_posts,

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


def following_page(request):

    # get the users that the logged in user is following
    following = Follower.objects.filter(follower=request.user.id)

    # create a list and append the following users ids
    list_following = []
    for user in following:
        list_following.append(user.followed.id)


    # filter the posts by the user the logged in user is following
    my_filter_qs = Q()
    for creator in list_following:
        my_filter_qs = my_filter_qs | Q(creator=creator)
    

    # Use the filter and check if the user is following anybody or not
    if len(list_following) > 0:
        posts_filtered = Post.objects.filter(my_filter_qs)
    else:
        posts_filtered = None


    return render(request,"network/following.html", {
        "posts" : posts_filtered
    })


def user_page(request, user_id):

    """Profilepage should display
        - number of followers
        - number of user following
        - posts in reverse order
        - other users, show follow unfollow button 
    """
    # get only the posts that the user created
    user_posts = Post.objects.filter(creator=user_id)
    user = User.objects.get(id = user_id)

    # Get the count of the followers and following of this user
    following = Follower.objects.filter(follower=user_id).count()
    followed = Follower.objects.filter(followed=user_id).count()

    # set the followstate as false for the logged in user, change it to true if the logged in user follows this user
    follow_state = False
    followers =  Follower.objects.filter(followed = user_id)

    for users in followers:
        if request.user.id == users.follower.id:
            follow_state = True
            break


    return render(request, "network/user_page.html", {
        "posts" : user_posts, 
        "user_searched" : user, 
        "following": following, 
        "followed" : followed,
        "follow_state" : follow_state
    })


def change_follow(request, user_searched_id):

    # get the 
    user_searched = User.objects.get(id=user_searched_id)

    # Get the info what button was clicked follow or unfollow
    if request.POST.get("action") == "follow":
        # make a instance for the logged in user
        follower = User.objects.get(id=request.user.id)
        # Create the enrty in the database
        new_following = Follower(followed=user_searched, follower=follower)
        new_following.save()

    else:
        # Find the query for the users and delete it 
        following_query = Follower.objects.filter(follower=request.user.id, followed=user_searched)
        following_query.delete()

    # return to the user Page again
    return HttpResponseRedirect(reverse("user_page", kwargs={"user_id" : user_searched_id}))

@csrf_exempt
@login_required
def posts(request, post_id):

    # Query for requested post
    try:
        # add user maybe TODO
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        post_info = post.serialize()
        return JsonResponse(post_info)

    # Update the post content
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        elif data.get("likes") is not None:
            post.likes = data["likes"] + post.likes
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def like_funct(request, post_id):

    # Update the post content
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            # if dislike delete the like object
            if data["like"] == 0:
                disliked = Liked.objects.filter(user=request.user.id, post=post_id)
                disliked.delete()
            # else add to the Liked instance a new one with the like of the current post
            else:
                liked = Liked(user=User.objects.get(id=request.user.id), post=Post.objects.get(id=post_id))  
                liked.save()

        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
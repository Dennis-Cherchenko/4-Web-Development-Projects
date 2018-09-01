from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .manager import *
import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from portfolios.forms import PostForm

# Import all the relevant models
from .models import Post, Like


def profile_view(request):

    # Returns the profile view

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "users/profile.html", {
        "user": request.user,
        "posts": getPostsForUserIdReverse(request.user.id)
    })

def portfolio_view(request):

    # Returns the portfolio view

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    author_id = request.POST.get("author_id")
    if author_id is None:
        author_id = request.user.id

    view_kind = request.POST.get("view_kind")
    if view_kind is None:
        view_kind = "Tile"

    return render(request, "portfolios/portfolio.html", {
        "user": request.user,
        "author": getUser(author_id),
        "posts": getPostsForUserIdReverse(author_id),
        "view_kind": view_kind,
        "view_kind_enum": view_kind_enum
    })



def newsfeed_view(request):

    # Returns the newsfeed view

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


    author_id = request.POST.get("author_id")
    if author_id is None:
        author_id = request.user.id

    likes_filter = request.POST.get("likes_filter")
    if likes_filter is None:
        likes_filter = "All time"

    return render(request, "portfolios/newsfeed.html", {
        "user": request.user,
        "most_liked_posts": getMostLikedPosts(6, likes_filter),
        "like_filters_enum": like_filters_enum,
        "likes_filter": likes_filter,
        "all_posts": getAllPostsReverseChronological()
    })


def post_view(request):

    # Returns the post view

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    post_id = request.POST.get("post_id")

    # Begin this block of logic handles different action
    # the user either liked a post,
    # the user added a comment
    # the user deleted a comment

    if post_id is None:
        return render(request, "portfolios/post.html", { "user": request.user })

    else:
        has_liked = getHasLiked(request.user.id, post_id)
        like = request.POST.get("like")
        new_comment = request.POST.get("new_comment")
        delete_comment_id = request.POST.get("delete_comment_id")

        if like is not None:
            if has_liked is False and like == "like":
                createLike(request.user.id, post_id)
                has_liked = True
            elif has_liked is True and like == "unlike":
                deleteLike(request.user.id, post_id)
                has_liked = False
        elif new_comment is not None and request:
            createComment(request.user.id, post_id, new_comment)
        elif delete_comment_id is not None:
            deleteComment(delete_comment_id)

        post = getPost(post_id)

    # end block

        return render(request, "portfolios/post.html", {
            "user": request.user,
            "author": getUser(post.user_id),
            "post": post,
            "has_liked": has_liked,
            "num_likes": getNumLikesForPost(post.id),
            "comments": getCommentsForPostChronologicalInBoxes(post_id)
        })


def search_view(request):

    # Returns the search view

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    search_term = request.POST.get("search_term")

    results = {}
    if search_term is not None:
        results = getSearchResultsForTerm(search_term)

    return render(request, "portfolios/search.html", {
        "user" : request.user,
        "results" : results
    })




def create_post_view(request):

    # Creates a new post

    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.save()
            return redirect('portfolio')
    else:
        form = PostForm()
    context = {
        "user": request.user,
    }
    return render(request, 'portfolios/create_post.html', {
        'form': form,
        'context' : context
    })


def login_view(request):

    # Login page

    username = request.POST.get("username")
    password = request.POST.get("password")

    if request.POST.get("isRegister") == "true":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if isEmpty(email) or isEmpty(first_name) or isEmpty(last_name):
            return render(request, "users/login.html", {"message": "Invalid credentials."})

        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

    user = authenticate(request, username=username, password=password)

    if user is not None :
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

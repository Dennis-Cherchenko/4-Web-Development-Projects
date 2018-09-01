from .models import Post, Like, Comment
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date, timedelta

# This is the manager class that containts a lot of 'helper' functions

like_filters_enum =  ["All time", "Last 3 days", "This week", "This month", "This year"]
view_kind_enum = ["Tile", "Stack"]

def isEmpty(item):
    return item is None or item == ""

def getAllPosts():
    return Post.objects.all()

def getPost(post_id):
    return getAllPosts().get(pk=post_id)

def getPostsForUserId(user_id):
    return getAllPosts().filter(user_id = user_id)

def getPostsForUserIdReverse(user_id):
    return getPostsForUserId(user_id).order_by('timestamp').reverse()

def getAllPostsReverseChronological():
    return getAllPosts().order_by('timestamp').reverse()

def getAllUsers():
    return User.objects.all()

def getUser(user_id):
    return getAllUsers().get(pk=user_id)

def containsTerm(term, items):
    for item in items:
        if term.lower() in item.lower():
            return True
    return False

def getUsersForTerm(term):
    # This functions returns all user model objects that containt the search term
    results = []
    for user in getAllUsers():
        for item in term.split():
            if containsTerm(item, [user.first_name, user.last_name, user.username, user.email]):
                results.append(user)
                break
    return results

def getPostsForTerm(term):
    # This functions returns all post model objects that containt the search term
    results = []
    for post in getAllPosts():
        for item in term.split():
            if containsTerm(item, [post.title, post.text]):
                results.append(post)
                break
    return results

def getSearchResultsForTerm(term):
    results = {}
    results["users"] = getUsersForTerm(term)
    results["posts"] = getPostsForTerm(term)
    return results

def getAllLikes():
    return Like.objects.all()

def getHasLiked(user_id, post_id):
    return getAllLikes().filter(user_id=user_id, post_id=post_id).count() is not 0

def createLike(user_id, post_id):
    return Like.objects.create(user_id=user_id, post_id=post_id)

def deleteLike(user_id, post_id):
    getAllLikes().filter(user_id=user_id, post_id=post_id).delete()

def getAllComments():
    return Comment.objects.all()

def createComment(user_id, post_id, text):
    return Comment.objects.create(user_id=user_id, post_id=post_id, text=text)

def deleteComment(comment_id):
    getAllComments().get(pk=comment_id).delete()

def getCommentsForPost(post_id):
    return getAllComments().filter(post_id=post_id)

def getCommentsForPostChronological(post_id):
    return getCommentsForPost(post_id).order_by('timestamp')

def getCommentsForPostChronologicalInBoxes(post_id):
    # This function allows for the releveant comment data to be displayed in the UI
    comments = []

    for comment in getCommentsForPostChronological(post_id):
        comments.append(Comment_Box(comment.id, \
            getUser(comment.user_id), comment.post_id, comment.text, comment.timestamp))
    return comments

class Comment_Box():
    # The purpose of this 'box' is to allow for an object that can be sent to the html and js easily
    def __init__(self, comment_id, author, post_id, text, timestamp):
        self.id = comment_id
        self.author = author
        self.post_id = post_id
        self.text = text
        self.timestamp = timestamp

def getNumLikesForPost(post_id):
    return getAllLikes().filter(post_id=post_id).count()

def getNumLikesForAllPosts():
    return getAllLikes().values('post_id').annotate(Count('post_id'))

def getNumLikesForAllPostsWithFilter(filter):
    # This function provided the filtering for likes
    if filter == "All time":
        return getNumLikesForAllPosts()
    else:
        if filter == "Last 3 days":
            start_date = date.today() - timedelta(days=3)
        elif filter == "This week":
            start_date = date.today() - timedelta(days=7)
        elif filter == 'This month':
            start_date = date.today() - timedelta(days=30)
        elif filter == "This year":
            start_date = date.today() - timedelta(days=365)

        return getNumLikesForAllPosts().filter(timestamp__gte=start_date, timestamp__lte=date.today())


def getPostsWithNoLikes():

    result_array = []

    num_likes_for_all_posts = getNumLikesForAllPosts()

    for post in getAllPosts():
        if getNumLikesForPost(post.id) == 0:
            result_array.append(post)

    return result_array

def getMostLikedPosts(num, filter):

    # Iterates through the recordrs to find the x most liked posts

    array = []

    for post in getNumLikesForAllPostsWithFilter(filter):
        if len(array) < num:
            array.append(post)
        else:
            for item in array:
                if post.get("post_id__count") > item.get("post_id__count"):
                    array.remove(item)
                    array.append(post)
                    break;

    # If the array above isn't full, it fulls the remain space to get to x
    # with posts with no likes

    returnArray = []

    for item in array:
        returnArray.append(getPost(item.get("post_id")))

    posts_with_no_likes = getPostsWithNoLikes()

    while len(returnArray) < num:
        if len(posts_with_no_likes) == 0:
            break
        else:
            returnArray.append(posts_with_no_likes[-1])
            posts_with_no_likes.pop(-1)

    return returnArray
from django.urls import include, path
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.newsfeed_view, name="index"),
    path("newsfeed", views.newsfeed_view, name="newsfeed"),
    path("portfolio", views.portfolio_view, name="portfolio"),
    path("admin/", admin.site.urls),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post", views.post_view, name="post"),
    path("profile", views.profile_view, name="profile"),
    path("portfolios/create_post", views.create_post_view, name="create_post"),
    path("search", views.search_view, name="search")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

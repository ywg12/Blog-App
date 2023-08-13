from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'postapi', PostsViewSet) 

urlpatterns = [
    path("home", views.starting_page, name= "starting-page"),
    path("posts", views.posts, name= "posts-page"),
    path("posts/<slug:slug>", views.post_detail, name= "post-detail-page"), #/posts/my-first-post
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
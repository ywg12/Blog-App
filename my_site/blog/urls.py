from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'postapi', PostsViewSet) 
urlpatterns = [
    #function-based calls
    # path("home", views.starting_page, name= "starting-page"),
    # path("posts", views.posts, name= "posts-page"),
    # path("posts/<slug:slug>", views.post_detail, name= "post-detail-page"), #/posts/my-first-post
    #class-based calls
    path("home/", StartingPageView.as_view(), name="starting-page"),
    path("posts/", PostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail-page"),  # /posts/my-first-post
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('search/', PostsViewSet.as_view({'get': 'search_by_title'}), name='search-posts-by-title'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
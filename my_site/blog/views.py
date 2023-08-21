from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostsSerializer
from .models import Post
from rest_framework.permissions import *
from rest_framework import permissions,viewsets
from rest_framework.pagination import PageNumberPagination



# Create your views here.
# Function based views
'''@permission_required('blog.view_post')
def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html",{
        "posts":latest_posts
    })
    
@permission_required('blog.view_post')    
def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html",{
        "all_posts":all_posts
    })
    
@permission_required('blog.view_author')    
def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html",{
        "post": identified_post,
        "post_tags": identified_post.tags.all()
    })
'''


class HasSpecificPermission(permissions.BasePermission):
    def __init__(self, permission_required):
        self.permission_required = permission_required
    
    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_required)    


class StartingPageView(PermissionRequiredMixin, View):
    permission_required = ['blog.view_post']  # Default required permission

    def get(self, request):
        latest_posts = Post.objects.all().order_by("-date")[:3]
        return render(request, "blog/index.html", {
            "posts": latest_posts
        })


class PostsView(PermissionRequiredMixin, View):
    permission_required = ['blog.view_post']
    def get(self, request):
        all_posts = Post.objects.all().order_by("-date")
        return render(request, "blog/all-posts.html", {
            "all_posts": all_posts
        })

class PostDetailView(PermissionRequiredMixin, View):
    permission_required = ['blog.view_author']
    def get(self, request, slug):
        identified_post = get_object_or_404(Post, slug=slug)
        return render(request, "blog/post-detail.html", {
            "post": identified_post,
            "post_tags": identified_post.tags.all()
        })

class CustomPagination(PageNumberPagination):
    page_size = 3  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 5

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    pagination_class = CustomPagination  # Use the custom pagination class    

    def get_permissions(self):
        permission_classes = [HasSpecificPermission('blog.view_post')]
        return permission_classes
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='title',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Search by title (case-insensitive)',
                required=True,
            ),
        ]
    )
    @action(detail=False, url_path='search', methods=['GET'])
    def search_by_title(self, request):
        title_query = request.query_params.get('title', '')
        posts = Post.objects.filter(title__icontains=title_query)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



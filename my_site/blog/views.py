from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.decorators import permission_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostsSerializer
from .models import Post
from rest_framework.permissions import *
from rest_framework import permissions


# Create your views here.
@permission_required('blog.view_post')
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


class HasSpecificPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Customize this logic based on your requirements
        # For example, check if the user has a specific permission
        return request.user.has_perm('blog.view_post')


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [HasSpecificPermission]

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

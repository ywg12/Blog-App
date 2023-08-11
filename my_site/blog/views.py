from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from .serializers import PostsSerializer
from .models import Post
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html",{
        "posts":latest_posts
    })
def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html",{
        "all_posts":all_posts
    })
def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html",{
        "post": identified_post,
        "post_tags": identified_post.tags.all()
    })
    
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-date")
    serializer_class = PostsSerializer  
    
class SignupAPIView(APIView):
    """This api will handle signup"""
    def post(self,request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            """If the validation success, it will created a new user."""
            serializer.save()
            res = { 'status' : status.HTTP_201_CREATED }
            return Response(res, status = status.HTTP_201_CREATED)
        res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)
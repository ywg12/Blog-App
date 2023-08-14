from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import PostsSerializer
from .models import Post
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
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    
    def search_by_title(self, request):
        title_query = request.query_params.get('title', '')
        posts = Post.objects.filter(title__icontains=title_query)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
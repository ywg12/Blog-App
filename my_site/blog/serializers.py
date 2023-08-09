from rest_framework import serializers
 
from .models import Post
 

class PostsSerializer(serializers.ModelSerializer):
    
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('title', 'date','content','author_name')
        
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.full_name()
        return None        
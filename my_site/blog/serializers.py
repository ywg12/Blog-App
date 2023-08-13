from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Post,Tag,Author
import re

str_reg = re.compile("^[a-zA-Z-\\s]+$")
 
#To use a single Serializer
'''class PostsSerializer(serializers.ModelSerializer):
    
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('title', 'date','content','author_name')
        
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.full_name()
        return None      '''  

#Using Nested Serializer        
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'

# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'     
        
# class PostSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer()  # Nesting AuthorSerializer that has froeign key field
#     tags = TagSerializer(many=True)  # Nesting TagSerializer for many-to-many relationship

#     class Meta:
#         model = Post
#         fields = '__all__' 
                  
           
           
class PostsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = '__all__'
        
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        
        post = Post.objects.create(**validated_data)
            
        for tag_id in tags_data:
            try:
                post.tags.add(tag_id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError("One or more tags not found.")
        
        return post
    

    def validate(self, data):
        title = data.get('title')
        is_valid = re.fullmatch(str_reg, title)
        if is_valid:
            return data
        raise serializers.ValidationError("Title can only have letters and spaces")




# class PostsSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=150)
#     excerpt = serializers.CharField(max_length=200)
#     content = serializers.CharField(max_length=1500)
    
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         return data

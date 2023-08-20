import os
from django.contrib import admin
from .models import Post, Author, Tag, UserProfile,UserImage
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author"),
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}
    
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['user', 'image']
    
#     def save_model(self, request, obj, form, change):
#         # Delete the old image if it exists
#         if obj.id:
#             old_obj = UserProfile.objects.get(id=obj.id)
#             if old_obj.image and obj.image != old_obj.image:
#                 old_obj.delete()
        
#         # Save the new image
#         super().save_model(request, obj, form, change)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_user_images']
    
    def get_user_images(self, obj):
        return ", ".join([str(image) for image in obj.userimage_set.all()])
    get_user_images.short_description = 'User Images'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserImage)  # Register UserImage here

        

        
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
# admin.site.register(UserProfile, ImageAdmin)
    
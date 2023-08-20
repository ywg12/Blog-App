import os
from django.contrib import admin
from .models import Post, Author, Tag, UserProfile
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author"),
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    
    def save_model(self, request, obj, form, change):
        # Delete the old image if it exists
        if obj.id:
            old_obj = UserProfile.objects.get(id=obj.id)
            if old_obj.image and obj.image != old_obj.image:
                old_obj.delete()
        
        # Save the new image
        super().save_model(request, obj, form, change)
        

        
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(UserProfile, ImageAdmin)

@receiver(pre_delete, sender=UserProfile)
def delete_user_profile_image(sender, instance, **kwargs):
    # Delete the image file from the media folder when the UserProfile instance is deleted
    if instance.image:
        instance.image.delete(save=False)
    
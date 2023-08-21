from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)
    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_address = models.EmailField()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="posts")
    tags = models.ManyToManyField(Tag)
    
    class Meta:
        db_table = 'posts'
    
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='user_images/', null=True, blank=True)

#     def __str__(self):
#         return self.user.username
    
#     def save(self, *args, **kwargs):
#         if self.image:
#             # Get the original image name
#             original_image_name = os.path.basename(self.image.name)
            
#             # Construct the new image name using username
#             new_image_name = f'{self.user.username}_{original_image_name}'
            
#             # Update the image name
#             self.image.name = new_image_name
        
#         super(UserProfile, self).save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserImage(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        if self.image:
            original_image_name = self.image.name
            
            new_image_name = f'{self.user_profile.user.username}_{original_image_name}'
            
            # Check if an image with the same filename exists
            existing_images = UserImage.objects.filter(
                user_profile=self.user_profile,
                image__contains=original_image_name
            )
            
            if existing_images.exists():
                # Delete existing images with the same filename and the image file
                for existing_image in existing_images:
                    existing_image.image.delete(save=False)
                    existing_image.delete()
            
            # Update the image filename and save
            self.image.name = new_image_name
        super(UserImage, self).save(*args, **kwargs)
     
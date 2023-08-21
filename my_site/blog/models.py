import datetime
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
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.image:
            
            current_timestamp = datetime.datetime.now()
            formatted_timestamp = current_timestamp.timestamp()
            # Get the original image name
            original_image_name = self.image.name
            
            # Construct the new image name using username
            new_image_name = f'{self.user.username}_{formatted_timestamp}_{original_image_name}'
            
            # Update the image name
            self.image.name = new_image_name
        
        super(UserProfile, self).save(*args, **kwargs)


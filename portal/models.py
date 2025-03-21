from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    excerpt = models.TextField(null=True)
    publish = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='image/portal_images/', null=True, blank=True)
    image_caption = models.CharField(max_length=100, default='Photo by Blog')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default=0)

    def clean(self):
        # Regular expression to find long unbroken words (more than 30 characters)
        long_word_pattern = re.compile(r'\b\w{30,}\b')

        if long_word_pattern.search(self.title):
            raise ValidationError({'title': "Title contains an unreasonably long word. Please use spaces."})
        
        if long_word_pattern.search(self.content):
            raise ValidationError({'content': "Content contains an unreasonably long word. Please use spaces."})

        if long_word_pattern.search(self.excerpt):
            raise ValidationError({'excerpt': "Excerpt contains an unreasonably long word. Please use spaces."})

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures validation is triggered before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
     
    



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content=models.TextField()
    publish=models.DateTimeField(auto_now_add=True)

    class meta:
        ordering=['publish']

    def __str__(self):
        return f'comment by {self.user}'
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    class Meta:
        ordering = ['-created_at']
    





    
# Create your models here.

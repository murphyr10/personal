from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='image/portal_images/', default='avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)

    
    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,  **kwargs):
    if created:
        Profile.objects.create(user=instance)





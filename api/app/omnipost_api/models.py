from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Platform(models.Model):
    """
    Configuration for a social media platform, eg. the details needed to connect to the platform's API
    """
    name = models.CharField(max_length=100, blank=False)
    configs = models.JSONField()
    # The configs field would contain the configuration details needed to connect to the platform's API
    actions = models.JSONField() 
    # Every actions would consist of a 'post' key with a list of actions that must
    # be performed to create a post on the platform

class PlatformInstance(models.Model):
    """
    An instance of a social media platform, e.g. a specific Twitter account
    """
    pass

class Post(models.Model):
    """
    A normal post. text and media (image or video)
    """
    pass

class ShortFormVideo(models.Model):
    """
    A short video, like reels, for any platform in general
    """
    pass

class Stories(models.Model):
    """
    Stories/status for any platform in general
    """
    pass

class Docs(models.Model):
    """
    Documents for any platform in general
    """
    remote_doc = models.URLField(blank=True, null=True)
    custom_doc = models.TextField(blank=True, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, blank=True, null=True)
    platform_instance = models.ForeignKey(PlatformInstance, on_delete=models.CASCADE, blank=True, null=True)
    
class Notifications(models.Model):
    """
    Any notifications from the platform
    """
    pass
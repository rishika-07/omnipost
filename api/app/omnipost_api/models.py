import json
from django.db import models
from django.contrib.auth.models import AbstractUser
import subprocess
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    pass

class Platform(models.Model):
    """
    Configuration for a social media platform, eg. the details needed to connect to the platform's API
    """
    name = models.CharField(max_length=100, blank=False)
    configs = models.JSONField(default=list)
    # The configs field would contain the configuration details needed to connect to the platform's API
    actions = models.JSONField(default=dict)
    # Every actions would consist of a 'post' key with a list of actions that must
    # be performed to create a post on the platform
    
class PlatformInstance(models.Model):
    """
    An instance of a social media platform, e.g. a specific Twitter account
    """
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credentials = models.JSONField(default=dict)
    
    def save(self, *args, **kwargs):
        # If this is a new instance being created
        if not self.pk:
            # Initialize credentials based on platform configs
            required_configs = self.platform.configs
            self.credentials = {key: "" for key in required_configs}
        super().save(*args, **kwargs)
    
    def get_credential(self, key):
        """Get a specific credential value"""
        return self.credentials.get(key)
    
    def set_credential(self, key, value):
        """Set a specific credential value"""
        if key in self.platform.configs:
            self.credentials[key] = value
        else:
            raise ValueError(f"Credential '{key}' not defined in platform configuration")
        
class Post(models.Model):
    """
    A normal post. text and media (image or video)
    """
    def validate_media_file(value):
        valid_mime_types = ['image/jpeg', 'image/png', 'video/mp4', 'video/avi']
        file_mime_type = value.file.content_type
        if file_mime_type not in valid_mime_types:
            raise ValidationError('Unsupported file type.')
        
    content = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to='media/', blank=True, null=True, validators=[validate_media_file])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_configs = models.JSONField(default=dict, blank=True, null=True)
    
    def create_post(self):
        """
        Create a post on the platform
        """
        # Get the actions needed to create a post
        platform_instances = PlatformInstance.objects.filter(user=self.user)
        
        for platform_instance in platform_instances:
            actions = platform_instance.platform.actions.get('post')
            for action in actions:
                # Execute the action
                # The action is a curl command to be executed
                # and might contain placeholders that must be replaced
                for key, value in platform_instance.credentials.items():
                    action = action.replace(key, value)
                if platform_instance.platform.name in self.post_configs:
                    for key, value in self.post_configs[platform_instance.platform.name].items():
                        action = action.replace(key, value)
                else:
                    self.post_configs[platform_instance.platform.name] = {}
                # Execute the action
                result = subprocess.run(action, shell=True, capture_output=True)
                if result.returncode != 0:
                    raise Exception(f"Error creating post on {platform_instance.platform.name}: {result.stderr}")
                response = json.loads(result.stdout)
                for key, value in response.items():
                    if key in self.post_configs:
                        self.post_configs[platform_instance.platform.name][key].update(value)
                    else:
                        self.post_configs[platform_instance.platform.name][key] = value


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
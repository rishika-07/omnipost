from django.contrib import admin

from .models import Platform, PlatformInstance, Post

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass

@admin.register(PlatformInstance)
class PlatformInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
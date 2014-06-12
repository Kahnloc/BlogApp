from django.contrib import admin
from .models import Post, Comment, Album, Tag, Image
from string import join 
# TEST

import os
from PIL import Image as PImage
from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT


class Commentinline(admin.TabularInline):
	model = Comment
	extra = 0


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_at',
	 'modified_at', 'published_at')
	inlines = (Commentinline,)
	list_filter = ('published_at',)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post')
	list_filter = ('email',)

class AlbumAdmin(admin.ModelAdmin):
	search_fields = ["title"]
	list_display = ["title"]

class TagAdmin(admin.ModelAdmin):
	list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
	search_fields = ["title"]
	list_display = ["__unicode__", "title", "user", "rating", "size", "tags_", "albums_", "thumbnail1", "created"]
	list_filter = ["tags", "albums", "user"]

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		obj.save()

	

admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
#from settings import MEDIA_URL
from django.conf import settings
MEDIA_URL = settings.MEDIA_URL
from edsite.blog.models import Post, Comment
from edsite.blog.forms import CommentForm

from edsite.blog.models import *

# Create your views here.
# /blog/
def main(request):
	"""Main listing"""
	albums = Album.objects.all()
	if not request.user.is_authenticated():
		albums = albums.filter(public=True)

	paginator = Paginator(albums, 10)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		albums = paginator.page(page)
	except (InvalidPage, EmptyPage):
		albums = paginator.page(paginator.num_pages)

	for album in albums.object_list:
		album.images = album.image_set.all()[:4]

	return render_to_response("photo/list.html", dict(albums=albums, user=request.user,
		media_url=MEDIA_URL))

def album(request, pk):
	"""Album listing."""
	num_images = 30
	if view == "full": num_images = 10

	album = Album.objects.get(pk=pk)
	if not album.public and not request.user.is_authenticated():
		return HttpResponse("Error: you need to be logged in to view this album.")

	images = album.image_set.all()
	paginator = Paginator(images, num_images)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		images = paginator.page(page)
	except (InvalidPage, EmptyPage):
		images = paginator.page(paginator.num_pages)

	return render_to_response("photo/album.html", dict(album=album, images=images, user=request.user,
		view=view, media_url=MEDIA_URL))

def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {
		'posts': posts
		})

# /blog/<post_id>/
def post_detail(request, post_id):
	post = Post.objects.get(id=post_id)
	form = CommentForm()
	return render(request, 'blog/post_detail.html',{
		'post': post,
		'form': form,
		})

# /blog/<post_id>/comment/
def post_comment(request, post_id):
	post = Post.objects.get(id=post_id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			# Save our data!
			comment = Comment(
				post=post,
				name=form.cleaned_data['name'],
				email=form.cleaned_data['email'],
				comment=form.cleaned_data['comment']
			)
			comment.save()
			return redirect(post.get_absolute_url())
	else:
		form = CommentForm()
	return render(request, 'blog/comment.html', {
		'post': post,
		'form': form,
		})
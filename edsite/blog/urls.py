from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'edsite.blog.views.post_list',
		name='post_list'),

	url(r'^(?P<post_id>\d+)/$',
		'edsite.blog.views.post_detail',
		name='post_detail'),

	url(r'^(?P<post_id>\d+)/comment/$',
		'edsite.blog.views.post_comment',
		name='post_comment'),

	url(r"^album/$", "edsite.blog.views.main",
		name='main_listing'),

	url(r"^album/(\d+)/$", "edsite.blog.views.album",
		name='album_listing'),

	url(r"^image/(\d+)/$", "edsite.blog.views.image",
		name='image_request'),

	url(r"^(\d+)/(full|thumbnails)/$", "edsite.blog.vews.album",
		name='album')
)
from django import template

register = template.Library()


@register.simple_tag
def comment_count(post):
	return post.comment_set.count()

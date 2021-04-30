from django import template

from main.views import main_tags

register = template.Library()


@register.filter(name='make_tags')
def make_tags(request, tag):
    new_request = request.GET.copy()
    if not request.GET.getlist('tags'):
        tags_list = list(main_tags)
    else:
        tags_list = new_request.getlist('tags')
    if tag.value in tags_list:
        tags_list.remove(tag.value)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag.value)
    return new_request.urlencode()


@register.filter(name='is_follower')
def is_follower(request, profile):
    return request.user.follower.filter(author=profile)


@register.filter(name='is_favorite')
def is_favorite(request, recipe):
    return request.user.favorites.filter(recipe=recipe).exists()


@register.filter(name='is_in_purchases')
def is_in_purchases(request, recipe):
    return request.user.shop_list.filter(recipe=recipe).exists()


@register.filter(name='purchases_count')
def purchases_count(request):
    return request.user.shop_list.count()

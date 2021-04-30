from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_post'),
    path('purchases/<int:recipe_id>', views.make_shoplist, name='purchases'),
    path('purchases', views.make_shoplist, name='purchases'),
    path('favorites/<int:recipe_id>', views.change_favorite, name='favorites'),
    path('favorites', views.change_favorite, name='favorites'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('subscriptions/<int:author_id>',
         views.subscriptions, name='subscriptions'),
    path('shop_list/', views.shop_list, name='shop_list'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('get_purchases/', views.get_purchases, name='get_purchases'),
    path('my_favorites/', views.my_favorites, name='my_favorites'),
    path('my_subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('<str:author>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete/',
         views.delete_recipe, name='delete_recipe')
]

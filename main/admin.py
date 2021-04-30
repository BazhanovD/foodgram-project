from django.contrib import admin

from main.models import (Recipe, Ingredient, Tag, Follow,
                         Favorite, ShopList, IngredientAmount)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('title',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShopList, ShopListAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)

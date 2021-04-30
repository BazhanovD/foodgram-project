import csv
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from main.forms import RecipeForm
from main.models import (Ingredient, IngredientAmount, Recipe,
                         Favorite, Tag, ShopList, Follow)
from main.utils import get_ingredients, main_tags

User = get_user_model()


def get_page(request, filters, page_to_show, args_to_page):
    tags = request.GET.getlist('tags')
    if not tags:
        tags = list(main_tags)
    recipes = Recipe.objects.filter(**filters).filter(
        tags__value__in=tags).distinct()
    tags_list = Tag.objects.all()
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, page_to_show, {
        'paginator': paginator,
        'page': page,
        'tags_list': tags_list,
        'tags': tags,
        **args_to_page
    })


def index(request):
    return get_page(request, {}, 'index.html', {})


@login_required
def my_favorites(request):
    return get_page(request, {'favorite_recipes__user': request.user},
                    'favorite.html', {})


def profile(request, author):
    profile = get_object_or_404(User, username=author)
    return get_page(request, {'author': profile}, 'authorRecipe.html',
                    {'profile': profile})


@login_required
def delete_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    recipe.delete()
    return redirect('profile', author=username)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save_recipe(request)
        return redirect('recipe',
                        recipe_id=recipe.id,
                        username=request.user.username
                        )

    texts = {'title': 'Создание рецепта', 'save_button': 'Создать рецепт'}
    return render(request, 'formRecipe.html', {'form': form,
                                               'texts': texts, 'edit': False})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect(
            'recipe',
            username=username,
            recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe)
    if form.is_valid():
        recipe = form.save_recipe(request, False)
        return redirect(
            'recipe',
            recipe_id=recipe.id,
            username=request.user.username
        )

    texts = {'title': 'Редактирование рецепта',
             'save_button': 'Сохранить рецепт'}
    return render(request, 'formRecipe.html',
                  {'form': form, 'recipe': recipe,
                   'texts': texts, 'edit': True})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(
        Recipe, pk=recipe_id
    )
    return render(request, 'singlePage.html', {'recipe': recipe})


def ingredients(request):
    if request.GET.get('query'):
        text = request.GET['query']
        ingr_list = list(Ingredient.objects.filter(
            title__istartswith=text).values())
        return JsonResponse(ingr_list, safe=False)


@login_required
def shop_list(request):
    if request.GET:
        recipe_id = request.GET.get('recipe_id')
        get_object_or_404(ShopList, user=request.user,
                          recipe__id=recipe_id).delete()
    purchases = Recipe.objects.filter(shop_list__user=request.user)
    return render(request, 'shopList.html', {'purchases': purchases, })


@login_required
def get_purchases(request):
    recipes = Recipe.objects.filter(shop_list__user=request.user)
    ingr = {}
    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        amount = recipe.recipe_amounts.values_list('quantity', flat=True)
        for key in range(len(ingredients)):
            title = ingredients[key][0]
            dimension = ingredients[key][1]
            quantity = amount[key]
            if title in ingr:
                ingr[title] = [ingr[title][0] + quantity, dimension]
            else:
                ingr[title] = [quantity, dimension]
    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['Ингридиент', 'Количество'])
    for key, value in ingr.items():
        writer.writerow([f'{key}', f'{value[0]}{value[1]}'])
    return response


@login_required
def my_subscriptions(request):
    subscriptions = User.objects.filter(
        following__user=request.user).annotate(recipe_count=Count('recipes'))
    all_recipes = {}
    for sub in subscriptions:
        all_recipes[sub] = Recipe.objects.filter(author=sub)[:3]
    paginator = Paginator(subscriptions, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {
        'paginator': paginator,
        'page': page,
        'all_recipes': all_recipes,
    }
                  )


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_exempt
def change_favorite(request, recipe_id=-1):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Favorite.objects.get_or_create(user=request.user,
                                                    recipe=recipe)
        return JsonResponse({'success': created})
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = Favorite.objects.filter(user=request.user,
                                          recipe=recipe).delete()
        return JsonResponse({'success': removed})


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_exempt
def make_shoplist(request, recipe_id=-1):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = ShopList.objects.get_or_create(user=request.user,
                                                    recipe=recipe)
        return JsonResponse({'success': created})
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = ShopList.objects.filter(user=request.user,
                                          recipe=recipe).delete()
        return JsonResponse({'success': removed})


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_exempt
def subscriptions(request, author_id=-1):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        _, created = Follow.objects.get_or_create(user=request.user,
                                                  author=author)
        if request.user == author or not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(user=request.user,
                                        author=author).delete()
        return JsonResponse({'success': removed})

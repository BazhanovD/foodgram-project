from django.forms import ModelForm, CheckboxSelectMultiple
from django.shortcuts import get_object_or_404

from .models import Recipe, Ingredient, IngredientAmount
from .utils import get_ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('text', 'title', 'tags', 'image', 'cooking_time')
        required = ('text', 'title')
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }

    def save_recipe(self, request, new=True):
        recipe = self.save(commit=False)
        recipe.author = request.user
        recipe.save()
        if new is False:
            recipe.recipe_amounts.all().delete()
        ingredients = get_ingredients(request)
        for title, quantity in ingredients.items():
            if int(quantity) < 1:
                return False
            ingredient = get_object_or_404(Ingredient, title=title)
            amount = IngredientAmount(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity)
            amount.save()
        self.save_m2m()
        return recipe

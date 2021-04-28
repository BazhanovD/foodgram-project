from django.forms import ModelForm, CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('text', 'title', 'tags', 'image', 'cooking_time')
        required = ('text', 'title')
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }

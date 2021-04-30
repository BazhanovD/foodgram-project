from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    style = models.CharField(max_length=30)


class Ingredient(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    dimension = models.CharField(max_length=10)


class Recipe(models.Model):
    title = models.CharField(max_length=200, null=True)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='main/', blank=True, null=True)
    cooking_time = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount',
        through_fields=('recipe', 'ingredient'))

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipes', )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')

    def __str__(self):
        return self.recipe.title


class ShopList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shop_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shop_list')

    def __str__(self):
        return self.recipe.title


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_amounts')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.ingredient.title

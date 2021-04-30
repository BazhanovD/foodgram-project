main_tags = ['breakfast', 'lunch', 'dinner']


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingr = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingr]
    return ingredients

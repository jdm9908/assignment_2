def validate_recipe(recipe):
    # Data quality rules: title, ingredients, instructions must not be empty
    if not recipe.get('title') or not recipe.get('ingredients') or not recipe.get('instructions'):
        return False
    # Servings, prep_time, cook_time should be present
    if not recipe.get('servings') or not recipe.get('prep_time') or not recipe.get('cook_time'):
        return False
    # Ingredients and instructions should be lists with at least 2 items
    if len(recipe['ingredients']) < 2 or len(recipe['instructions']) < 2:
        return False
    return True

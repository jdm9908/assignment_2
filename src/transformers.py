def transform_recipe(recipe):
    # Example transformation: add total_time, ingredient count, and summary
    total_time = None
    try:
        # Simple time extraction (assumes minutes)
        prep = int(''.join(filter(str.isdigit, recipe.get('prep_time', '0'))))
        cook = int(''.join(filter(str.isdigit, recipe.get('cook_time', '0'))))
        total_time = prep + cook
    except Exception:
        total_time = None
    summary = f"{recipe.get('title', '')}: {len(recipe.get('ingredients', []))} ingredients, {len(recipe.get('instructions', []))} steps."
    recipe['total_time'] = total_time
    recipe['ingredient_count'] = len(recipe.get('ingredients', []))
    recipe['summary'] = summary
    return recipe

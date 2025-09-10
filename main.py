import requests
from bs4 import BeautifulSoup
import json

def extract_recipe(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title = soup.find('h1', class_='entry-title').get_text(strip=True) if soup.find('h1', class_='entry-title') else None

    # Extract ingredients
    ingredients = []
    for ing in soup.select('.wprm-recipe-ingredient'):  # WPRM plugin used on Sally's site
        ingredients.append(ing.get_text(strip=True))

    # Extract instructions
    instructions = []
    for step in soup.select('.wprm-recipe-instruction-text'):
        instructions.append(step.get_text(strip=True))

    # Extract servings, prep time, cook time
    servings = soup.select_one('.wprm-recipe-servings').get_text(strip=True) if soup.select_one('.wprm-recipe-servings') else None
    prep_time = soup.select_one('.wprm-recipe-prep_time').get_text(strip=True) if soup.select_one('.wprm-recipe-prep_time') else None
    cook_time = soup.select_one('.wprm-recipe-cook_time').get_text(strip=True) if soup.select_one('.wprm-recipe-cook_time') else None

    recipe = {
        'title': title,
        'servings': servings,
        'prep_time': prep_time,
        'cook_time': cook_time,
        'ingredients': ingredients,
        'instructions': instructions
    }
    return recipe

if __name__ == '__main__':
    url = input('Enter Sally recipe URL: ')
    recipe = extract_recipe(url)
    print(json.dumps(recipe, indent=2, ensure_ascii=False))

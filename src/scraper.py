import requests
from bs4 import BeautifulSoup
import time
import json
import re
from validators import validate_recipe
from transformers import transform_recipe
import os

# --- Extract Recipe Logic ---
def extract_recipe(url):
    import re
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract title
    title = None
    h1 = soup.find('h1')
    if h1:
        title = h1.get_text(strip=True)
    # Extract ingredients from tasty-recipes-ingredients class
    ingredients = []
    ingredients_section = soup.find(class_='tasty-recipes-ingredients')
    if ingredients_section:
        for li in ingredients_section.find_all('li'):
            text = li.get_text(strip=True)
            if text and text not in ingredients:
                ingredients.append(text)
    # Fallback: old logic if not found
    if not ingredients:
        import re
        headings = soup.find_all(lambda tag: tag.name in ['h2', 'h3', 'h4'] and re.search(r'ingredient', tag.get_text(strip=True), re.I))
        for heading in headings:
            next_tag = heading
            while True:
                next_tag = next_tag.find_next_sibling()
                if not next_tag or (next_tag.name in ['h2', 'h3', 'h4']):
                    break
                if next_tag.name in ['ul', 'ol']:
                    for li in next_tag.find_all('li'):
                        text = li.get_text(strip=True)
                        if text and text not in ingredients:
                            ingredients.append(text)
        if not ingredients:
            for ul in soup.find_all(['ul', 'ol']):
                for li in ul.find_all('li'):
                    text = li.get_text(strip=True)
                    if text and len(text.split()) > 2 and text not in ingredients:
                        ingredients.append(text)

    # Extract instructions from tasty-recipes-instructions class
    instructions = []
    instructions_section = soup.find(class_='tasty-recipes-instructions')
    if instructions_section:
        for li in instructions_section.find_all('li'):
            text = li.get_text(strip=True)
            if text:
                instructions.append(text)
        # If no <li>, try paragraphs
        if not instructions:
            for p in instructions_section.find_all('p'):
                text = p.get_text(strip=True)
                if text:
                    instructions.append(text)
    # Fallback: old logic if not found
    if not instructions:
        instructions_heading = soup.find(lambda tag: tag.name in ['h2', 'h3', 'h4'] and 'instruction' in tag.get_text(strip=True).lower())
        if instructions_heading:
            next_list = instructions_heading.find_next(['ul', 'ol'])
            if next_list:
                for li in next_list.find_all('li'):
                    instructions.append(li.get_text(strip=True))
    # Extract servings, prep time, cook time, total time from their respective classes
    def get_text_by_class(cls):
        el = soup.find(class_=cls)
        return el.get_text(strip=True) if el else None

    prep_time = get_text_by_class('prep-time')
    cook_time = get_text_by_class('cook-time')
    total_time = get_text_by_class('total-time')
    servings = get_text_by_class('yield')

    # Fallback to regex if not found
    page_text = soup.get_text(" ", strip=True)
    if not servings:
        servings_match = re.search(r"(serves|yield)\s*:?\s*([\w\d\-]+)", page_text, re.I)
        if servings_match:
            servings = servings_match.group(2)
    if not prep_time:
        prep_match = re.search(r"prep time\s*:?\s*([\w\s\d]+)", page_text, re.I)
        if prep_match:
            prep_time = prep_match.group(1).strip()
    if not cook_time:
        cook_match = re.search(r"cook time\s*:?\s*([\w\s\d]+)", page_text, re.I)
        if cook_match:
            cook_time = cook_match.group(1).strip()

    recipe = {
        'title': title,
        'servings': servings,
        'prep_time': prep_time,
        'cook_time': cook_time,
        'total_time': total_time,
        'ingredients': ingredients,
        'instructions': instructions
    }
    return recipe
# --- End Extract Recipe Logic ---

def exponential_backoff(retries):
    return min(2 ** retries, 60)

def scrape_recipe(url, max_retries=2):
    retries = 0
    while retries < max_retries:
        try:
            raw_data = extract_recipe(url)
            if not validate_recipe(raw_data):
                raise ValueError("Validation failed")
            processed = transform_recipe(raw_data)
            return processed
        except Exception as e:
            wait = exponential_backoff(retries)
            print(f"Error: {e}. Retrying in {wait} seconds...")
            time.sleep(wait)
            retries += 1
    print(f"Max retries ({max_retries}) reached for {url}. Skipping.")
    return None

def get_recipe_urls(index_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(index_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all links to recipes (assume links under /.../ and containing 'recipe' or ending with a slash)
    recipe_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://sallysbakingaddiction.com/') and ('recipe' in href or href.endswith('/')):
            # Filter out index/category pages
            if not any(x in href for x in ['category', 'index', 'ingredient', 'video', 'about', 'contact', 'privacy', 'disclosure', 'faq']):
                # Ignore if last path segment starts with a digit or URL contains '#comments'
                last_segment = href.rstrip('/').split('/')[-1]
                if (not last_segment or not last_segment[0].isdigit()) and ('#comments' not in href):
                    recipe_links.add(href)
    return list(recipe_links)

def save_output(data, path):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    index_url = "https://sallysbakingaddiction.com/recipe-index/"
    print(f"Crawling recipe index: {index_url}")
    urls = get_recipe_urls(index_url)
    print(f"Found {len(urls)} recipes. Scraping until 10 valid recipes...")
    all_results = []
    attempted = 0
    i = 0
    while len(all_results) < 10 and i < len(urls):
        url = urls[i]
        print(f"[{len(all_results)+1}/10] Scraping: {url}")
        result = scrape_recipe(url)
        attempted += 1
        if result:
            all_results.append(result)
        else:
            print(f"[SKIP] Validation failed for: {url}")
        i += 1
    print(f"Scraped {len(all_results)} valid recipes out of {attempted} attempted.")
    save_output(all_results, "assignment_2/data/sample_output.json")
    print(f"Data saved to assignment_2/data/sample_output.json")

#
## Scraper Concepts

### 1. Data Quality Assurance
- Validation rules ensure each recipe has a non-empty title, ingredients, instructions, servings, prep time, and cook time.
- Ingredients and instructions must be lists with at least 2 items.
- Only recipes passing validation are saved.

### 2. Respectful Scraping
- Exponential backoff is used for failed requests, increasing wait time up to 60 seconds.
- Each recipe is retried up to 2 times before skipping.

### 3. Business Logic
- Data transformation pipeline (`transform_recipe`) adds total time, ingredient count, and a summary string for each recipe.
- Value-added calculations include ingredient count and total time.
- All results are exported as a single JSON file (`assignment_2/data/sample_output.json`).
#
## Scraper Logic & User-Driven Improvements

- **Ingredient Extraction:** Ingredients are extracted from the HTML element with class `tasty-recipes-ingredients`. If not found, fallback logic uses headings and list items.
- **Instruction Extraction:** Instructions are extracted from the class `tasty-recipes-instructions`, with fallback to headings and lists.
- **Time & Servings Extraction:** Prep time, cook time, total time, and servings are extracted from their respective classes: `prep-time`, `cook-time`, `total-time`, and `yield`. Fallback to regex if missing.
- **URL Filtering:**
	- Ignores recipe URLs where the last path segment starts with a number (to avoid collections).
	- Ignores URLs containing `#comments`.
- **Validation Logic:** The scraper continues until 10 valid recipes are collected, skipping failed validations so the output always contains 10 recipes.

## Usage Notes
- To rerun the scraper, execute `python src/scraper.py` (or use the full Python path if needed).
- To customize extraction for other recipe card formats, update the class names in `extract_recipe`.
- For further filtering, adjust the logic in `get_recipe_urls`.

- Output is now saved to `assignment_2/data/sample_output.json`.
# AI_USAGE.md

## Prompts Used

### Exact Prompts Used
- "make a web scraper application for sally for https://sallysbakingaddiction.com/ to extract the important data of the recepie"
- "debug this"
- "use the source code to make it null, when i ran it the values were null"
- "use this url https://sallysbakingaddiction.com/triple-chocolate-layer-cake/"
- "okay now its not getting the servings, prep_time, cook_time, and ingredients please fix that"
- "add the features below..."
- "how do i download pip"
- "Exception has occurred: ModuleNotFoundError No module named 'requests'"
- "the ingrediants list includes other information in some of the recipes"
- "how does this scarper extract the ingrediants"
- "there is a recepie card on the bottom, can we use that instead, how do i find where to scrape that"
- "instructions: Class: tasty-recipes-notes ingrediants: Class: tasty-recipes-ingredients"
- "the instructions class is 'tasty-recipes-instructions'"
- "the class for prep_time is prep-time the class for cook time is cook-time the class for total time is total-time The class for servings is yield"
- "okay, i want to ignore the reciepes that start with a number because they are a collection of reciepes and we want to aim for one"
- "I want to change it so it does not scrape #comments pages"
- "Also please add it where if a valiation is failed, it does not go up in iteration so we alwayus have 10 recipes"
- "now please go through out past conversations and add it to the ai usage log"
- "how do i commit this to my github"
- "git : The term 'git' is not recognized as the name of a cmdlet, function, script file, or operable program."
- "Requirements: Pre-Implementation Planning..."
- "create something for this please"
- "Your scraper should demonstrate these concepts: Data Quality Assurance, Respectful Scraping, Business Logic"
- "add scraper concepts in this please"
- "3. AI Tool Documentation...add for all of the prompts i have given you"

## AI-Generated vs Human-Written Code

### Code Origin
- All code in `src/` was generated or refactored with AI assistance based on user prompts and requirements.
- User provided requirements, feedback, and specific logic/class names; AI generated, patched, and improved code accordingly.
- Documentation and strategy files were also AI-generated based on user requests.

## Bugs Found & Fixes

### Bugs Found in AI Suggestions & Fixes
- Initial selectors did not match site structure; fixed by updating extraction logic to use correct classes.
- Ingredient extraction included unrelated info; improved filtering logic.
- Instructions and time fields were missing; added extraction by class and fallback logic.
- Validation logic did not guarantee 10 valid recipes; loop logic updated.
- URLs for collections and comments were not filtered; added URL filtering.
- `re` import error in fallback logic; moved import to top of function.
- Output path was inconsistent; standardized to `assignment_2/data/sample_output.json`.

## Performance Comparisons

### Performance Comparisons
- Not tested for speed, but retry/backoff logic prevents hammering the site.
- Validation and transformation pipelines ensure data quality and value.
- Scraper is designed to be efficient and respectful, with retry limits and exponential backoff.

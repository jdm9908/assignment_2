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
- "make a web scraper application for sally for https://sallysbakingaddiction.com/ to extract the important data of the recepie"
- "debug this"
- "use the source code to make it null, when i ran it the values were null"
- "use this url https://sallysbakingaddiction.com/triple-chocolate-layer-cake/"
- "okay now its not getting the servings, prep_time, cook_time, and ingredients please fix that"
- "add the features below..."

## AI-Generated vs Human-Written Code
- All code in `src/` was generated with AI assistance.
- User provided requirements and feedback, AI generated and refactored code.

## Bugs Found & Fixes
- Initial selectors did not match site structure; fixed by updating extraction logic.
- Imports in `scraper.py` may need to be changed from relative to absolute for direct execution.

## Performance Comparisons
- Not tested for speed, but retry/backoff logic prevents hammering the site.
- Validation and transformation pipelines ensure data quality and value.

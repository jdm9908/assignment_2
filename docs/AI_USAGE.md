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

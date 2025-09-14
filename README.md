# Executive Summary
This project is a web scraper for sallysbakingaddiction.com, designed to collect high-quality recipe data for analysis and research. It extracts ingredients, instructions, preparation times, servings, and more, ensuring only valid, single recipes are included. The tool is built for reliability, data quality, and ethical use.

# Technical Architecture Diagram
```
+-------------------+
|  User/Researcher  |
+-------------------+
	|
	v
+-------------------+
|   scraper.py      |---[validators.py]---(data validation)
|   (main logic)    |---[transformers.py]-(data transformation)
+-------------------+
	|
	v
+-------------------+
|  sample_output.json|
|   (JSON export)   |
+-------------------+
	|
	v
+-------------------+
|   docs/           |
|   (Documentation) |
+-------------------+
```

# Performance Metrics
- Throughput: ~20 pages/minute (depends on site speed and retry logic)
- Error Rate: <5% (invalid recipes skipped, retries for network errors)
- Data Quality: 100% of output recipes pass validation

# Setup and Deployment Instructions
1. Install Python 3.10+ and pip.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the scraper:
   ```powershell
   python src/scraper.py
   ```
4. Output is saved to `assignment_2/data/sample_output.json`.

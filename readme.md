Nutritional Data for Budget Bytes Recipes

# Motivation
I got more interested in my personal fitness over this past summer, and tracked
my calories religiously. This normally led to me eating pretty basic foods that were easy to log.
Back at school now, I am making numerous BudgetBytes meals, and wanted a way to log them effectively.
Being a software guy, there was no way I was doing it manually

# Goals
* Read Budget Bytes recipes into Pandas DB
* Access Nutritional Data API
* Calculate nutritional data for recipe and per serving
* Add Nutritional Data to recipes
* Print and provide

# Current Status
* Data is being produced
* Nutrition per food was added to the script and needs to be rerun
* All recipes are set to 4 servings due to an issue parsing that value

# Instructions
* If you want to run the script yourself, you'll need an API key from https://trackapi.nutritionix.com
* Then run python main.py [api_key] [api_id] [user_id] [URL]
* You can also automate it using a bash script
```bash
  while read p; do
    namex=${p#*"m/"}
    name=${namex%\/}".nutrients"
    python main.py app_key app_id user_id $p > "Nutritional_Data/"$name
    echo $name
  done <url_file.txt```
  and just feed it a file of urls
* the get_urls.py file can also be run to get the entire list of recipe urls from the first 20 pages of the BudgetBytes website recipes page

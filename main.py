#!/usr/bin/env python
import urllib.request
from bs4 import BeautifulSoup
import sys
import requests

class Recipe:
    def __init__(self, name="Unnamed Recipe", servings=1, ingredients=[], nutrients=None):

        self.name = name

        self.servings = servings

        self.ingredients = ingredients

        if nutrients:
            self.nutrients = nutrients
        else:
            self.nutrients = {  "calories": 0,
                            "total_fat": 0,
                            "saturated_fat": 0,
                            "cholesterol": 0,
                            "sodium": 0,
                            "total_carbohydrate": 0,
                            "dietary_fiber": 0,
                            "sugars": 0,
                            "protein": 0,
                            "potassium": 0,
                            "p": 0
                            }
        self.nutrients_per_serving = {}
        if self.servings != 1:
            for key in self.nutrients:
                self.nutrients_per_serving[key] = float(self.nutrients[key])/self.servings
        else:
            self.nutrients_per_serving = self.nutrients

    def __repr__(self):
        val = "Recipe: %s\nServings: %s\n\nIngredients:\n" % (self.name, self.servings)
        for ingredient in self.ingredients:
            val += str(ingredient) + "\n"
        val += "\nNutrition:\n"
        for key in self.nutrients:
            val += str(key) + ": " + str(self.nutrients[key]) + "\n"

        val += "\nNutrition per Serving:\n"
        for key in self.nutrients_per_serving:
            val += str(key) + ": " + str(self.nutrients_per_serving[key]) + "\n"
        return val

    def update(self):
        if self.servings != 1:
            for key in self.nutrients:
                self.nutrients_per_serving[key] = float(self.nutrients[key])/self.servings


class Ingredient:

    def __init__(self, amount, unit, name):
        self.amount = amount
        self.unit = unit
        self.name = name

    def __repr__(self):
        if not self.unit:
            if not self.amount:
                return "%s" % self.name
            return "%s %s" % (self.amount, self.name)
        return "%s %s %s" % (self.amount, self.unit, self.name)

def getSite(url):
    site = urllib.request.urlopen(url)
    return BeautifulSoup(site, 'html.parser')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print ("Please provide recipe link")
        exit()
    key = sys.argv[1]
    id = sys.argv[2]
    user = sys.argv[3]

    recipe_page = sys.argv[4]
    content = getSite(recipe_page)
    recipe_name = content.find('h1', class_='title').getText()
    recipe_servings = 4#content.find("input", class_='wprm-recipe-servings')
    #print(recipe_servings)
    ingredients_raw = content.findAll("li", class_="wprm-recipe-ingredient")
    ingredients = []
    for ingredient in ingredients_raw:
        amount = ingredient.find("span", class_='wprm-recipe-ingredient-amount')
        if amount != None:
            amount = amount.getText()
        unit = ingredient.find("span", class_='wprm-recipe-ingredient-unit')
        if unit != None:
            unit = unit.getText()
        name = ingredient.find("span", class_='wprm-recipe-ingredient-name').getText()
        #print(amount, unit, name)
        new_thing = Ingredient(amount, unit, name)
        #print(new_thing)
        ingredients.append(new_thing)

    ingredient_string = ""
    for ingredient in ingredients:
        ingredient_string = ingredient_string + str(ingredient) + ", "

    headers = {
        "Content-Type":"application/json",
        "x-app-key": key,
        "x-app-id": id,
        "x-remote-user-id": user
    }


    data_string = "{\"query\": \"%s\"}" % ingredient_string

    response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients", data=data_string, headers=headers)
    data = response.json()

    recipe = Recipe(recipe_name, recipe_servings, ingredients=ingredients)

    for food in data['foods']:
        for key in recipe.nutrients:
            if food["nf_" + key]:
                recipe.nutrients[key] += food["nf_" + key]

    recipe.update()
    print(recipe)

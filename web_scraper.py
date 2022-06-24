# here we shall scrape the webpage for ingredients list and for instructions. honestly I don't even want the pantry
# matcher in my life i want a skip all the annoying blog info and just give me the recipe in a pretty format
# oh also this will include the click on recipes functionality
# class name that contains the link class="card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom"
# once you get to the webpage, find the array called recipe ingredient

import urllib.request
import re
import ast
import pantry_processor

pantry = pantry_processor.read_pantry('Pantry.xlsx', 'Pantry1')

ingredient_substitutes = {
    # unfortunately, common substitutions like this dictionary are beyond the scope of my time. but maybe one day.
    "butter": "margarine",
    "vanilla sugar": "vanilla extract",
    "almond milk": "milk",
    "chocolate chunks": "chocolate chips",
    "confectioner's sugar": "powdered sugar",
    "icing sugar": "powdered sugar"
}


def open_allrecipes():
    recipe_search = input("enter recipe you would like to make: ")
    recipe_search_updated = "https://www.allrecipes.com/search/results/?search=" + recipe_search.replace(" ", "+")
    f = urllib.request.urlopen(recipe_search_updated)
    data = f.read().decode()

    return data


def open_recipe_from_search_page(data):
    search_for_string = 'class="card__titleLink manual-link-behavior elementFont__title margin-8-bottom"'
    the_url_should_be_in_here = re.compile(r'<a class="card__titleLink manual-link-behavior elementFont__titleLink '
                                           r'margin-8-bottom"\n\s*.*\n\s*href=(.*)\n[^>]*')
    url = re.findall(the_url_should_be_in_here, data)
    return re.findall(the_url_should_be_in_here, data)


def collect_ingredients_and_instructions(recipe_webpage):
    f = urllib.request.urlopen(recipe_webpage)
    data = f.read().decode()
    ingredient_finder = re.compile('(recipeIngredient.*],)\n', re.DOTALL)
    m = re.search(ingredient_finder, data)
    recipe = m.groups()
    recipe_divided = recipe[0].split("recipeInstruction")

    # but maybe we should keep it because we may need it later, and it's a rather small file anyway
    # we should definitely keep it. We'll deal with that later though - maybe a separate method
    # called divide to temporarily divide it for the checker portion?
    # ingredient_array = recipe_divided[0]

    return recipe_divided


def look_for_matching_recipe():
    recipe_search = open_allrecipes()
    recipe_results = open_recipe_from_search_page(recipe_search)
    # print(len(recipe_results))

    not_present_count = []
    for recipe in recipe_results:
        recipe_minus_extra_quotes = recipe.replace('"', '')

        full_recipe = collect_ingredients_and_instructions(recipe_minus_extra_quotes)
        ingredients = full_recipe[0]
        just_the_array_but_in_an_unnecessary_tuple = ast.literal_eval(ingredients.strip('recipeIngredient": '))
        ingredients_array = just_the_array_but_in_an_unnecessary_tuple[0]

        not_present = []
        for ingredient in ingredients_array:
            present = True
            for my_ingredient in pantry:
                if my_ingredient in ingredient:
                    # print(f"{ingredient} is in pantry")
                    present = True
                    break
                else:
                    present = False
            if not present:
                not_present.append(ingredient)
        # print(not_present)
        not_present_count.append(not_present)

        # do the matching thing on the ingredients half to the
    least_missing = 0
    for i in range(0, len(not_present_count)):
        if len(not_present_count[i]) < len(not_present_count[least_missing]):
            least_missing = i

    print(recipe_results[i])


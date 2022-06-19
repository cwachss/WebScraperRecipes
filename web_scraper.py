# here we shall scrape the webpage for ingredients list and for instructions. honestly I don't even want the pantry
# matcher in my life i want a skip all the annoying blog info and just give me the recipe in a pretty format
# oh also this will include the click on recipes functionality
# class name that contains the link class="card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom"
# once you get to the webpage, find the array called recipe ingredient

import urllib.request
import re


def open_allrecipes():
    recipe_search = input("enter recipe you would like to make")
    recipe_search_updated = "https://www.allrecipes.com/search/results/?search=" + recipe_search.replace(" ", "+")
    f = urllib.request.urlopen(recipe_search_updated)
    data = f.read().decode()

    return data


def open_recipe_from_search_page(data):
    search_for_string = 'class="card__titleLink manual-link-behavior elementFont__title margin-8-bottom"'
    the_url_should_be_in_here = re.compile("search_for_string\n.*\nhref=(.*)\n", re.DOTALL)
    return re.findall(the_url_should_be_in_here, data)


def collect_ingredients(recipe_webpage):
    f = urllib.request.urlopen(recipe_webpage)
    data = f.read().decode()
    ingredient_finder = re.compile('(recipeIngredient.*],)', re.DOTALL)
    m = re.search(ingredient_finder, data)
    ingredient_array = m.groups()
    return ingredient_array


webpage = open_allrecipes()
#
print(open_recipe_from_search_page(webpage))
print(collect_ingredients("https://www.allrecipes.com/recipe/25040/chocolate-chip-cookies-v/"))

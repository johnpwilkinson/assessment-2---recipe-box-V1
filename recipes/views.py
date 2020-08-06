from django.shortcuts import render
from recipes.models import Recipe, Author
# Create your views here.

def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': my_recipes, })

def recipe(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe.html', {'recipe': my_recipe})

def author(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    authors_recipes = Recipe.objects.filter(author=author_id)
    return render(request, 'author.html', {'author': my_author, 'recipes': authors_recipes } )
from django.shortcuts import render, HttpResponseRedirect, reverse
from recipes.models import Recipe, Author
from recipes.forms import AddRecipeForm, AddAuthorForm
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
    return render(request, 'author.html', {'author': my_author, 'recipes': authors_recipes})


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                instructions=data.get('instructions'),
                time_required=data.get('time_required'),
                author= data.get('author')
            )
            return HttpResponseRedirect(reverse('homepage'))


    form = AddRecipeForm()
    return render(request, 'generic_form.html', {"form":form})

def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
    
    form = AddAuthorForm()
    return render(request, 'generic_form.html', {"form": form})
from django.shortcuts import render, HttpResponseRedirect, reverse
from recipes.models import Recipe, Author, Favorite
from recipes.forms import AdminRecipeForm, AddAuthorForm, LoginForm, SignupForm, UserRecipeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404


# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': my_recipes, })


def recipe(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe.html', {'recipe': my_recipe})

def fav_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.create(author=request.user.author, recipe=recipe)
    return HttpResponseRedirect(reverse('homepage'))


def author(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    authors_recipes = Recipe.objects.filter(author=author_id)
    favorites = Favorite.objects.filter(author=author_id)
    return render(request, 'author.html', {'author': my_author, 'recipes': authors_recipes, 'favorites': favorites})


@login_required
def add_recipe(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AdminRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Recipe.objects.create(
                    title=data.get('title'),
                    author=data.get('author'),
                    description=data.get('description'),
                    time_required=data.get('time_required'),
                    instructions=data.get('instructions')
                )
                return HttpResponseRedirect(reverse('homepage'))
        form = AdminRecipeForm()
    else:
        if request.method == "POST":
            form = UserRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Recipe.objects.create(
                    title=data.get('title'),
                    author=request.user.author,
                    description=data.get('description'),
                    time_required=data.get('time_required'),
                    instructions=data.get('instructions')
                )
                return HttpResponseRedirect(reverse('homepage'))
        form = UserRecipeForm()
    return render(request, "generic_form.html", {'form': form})

@login_required
def edit_recipe_view(request, recipe_id):
    edit_recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = UserRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            edit_recipe.title = data['title']
            edit_recipe.description = data['description']
            edit_recipe.time_required = data['time_required']
            edit_recipe.instructions = data['instructions']
            edit_recipe.save()
        return HttpResponseRedirect(reverse('homepage'))
    data = {
        'title': edit_recipe.title,
        'description': edit_recipe.description,
        'time_required': edit_recipe.time_required,
        'instructions': edit_recipe.instructions
    }
    form = UserRecipeForm(initial=data)
    return render(request, 'generic_form.html', {'form': form})

@staff_member_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                'username'), password=data.get('password'))
            Author.objects.create(name=data.get(
                'username'), user=new_user, bio=data.get('bio'))
        return HttpResponseRedirect(reverse('homepage'))

    form = AddAuthorForm()
    return render(request, 'generic_form.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                # return HttpResponseRedirect(reverse("homepage"))
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

                # figure out bad log in page

    form = LoginForm()
    return render(request, 'generic_form.html', {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                "username"), password=data.get("password"))
            Author.objects.create(name=data.get("username"), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form})

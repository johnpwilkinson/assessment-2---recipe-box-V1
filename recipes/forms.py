from django import forms
from recipes.models import Author, Recipe
from django.contrib.auth.models import User

class UserRecipeForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=200)
    instructions = forms.CharField(widget=forms.Textarea)
class AdminRecipeForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=200)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.Form):
    username= forms.CharField(max_length=240)
    password= forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username= forms.CharField(max_length=240)
    password= forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username= forms.CharField(max_length=240)
    password= forms.CharField(widget=forms.PasswordInput)   
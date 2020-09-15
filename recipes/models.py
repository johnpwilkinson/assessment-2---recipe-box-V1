from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField(default="this is my bio")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    time_required = models.CharField(max_length=20)
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self
    
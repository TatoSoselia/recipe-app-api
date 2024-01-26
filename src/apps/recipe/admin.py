from django.contrib import admin
from apps.recipe.models import Recipe, Tag, Ingredient

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)

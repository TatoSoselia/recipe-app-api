from django.contrib import admin
from apps.recipe.models import Recipe, Tag

admin.site.register(Recipe)
admin.site.register(Tag)

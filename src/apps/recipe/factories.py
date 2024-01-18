import factory
from factory.django import DjangoModelFactory

from apps.recipe.models import Recipe
from apps.user.factories import UserFactory


class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=3)
    time_minutes = factory.Faker('random_int', min=5, max=120)
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    link = factory.Faker('url')

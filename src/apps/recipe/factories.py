import factory
from factory.django import DjangoModelFactory

from apps.user.factories import UserFactory


class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = "recipe.Recipe"

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=3)
    time_minutes = factory.Faker('random_int', min=5, max=120)
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    link = factory.Faker('url')


class TagFactory(DjangoModelFactory):

    class Meta:
        model = "recipe.Tag"

    name = factory.Faker('sentence', nb_words=3)
    user = factory.SubFactory(UserFactory)


class IngredientFactory(DjangoModelFactory):

    class Meta:
        model = "recipe.Ingredient"

    name = factory.Faker('sentence', nb_words=3)
    user = factory.SubFactory(UserFactory)

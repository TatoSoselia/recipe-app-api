import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.Faker("password")
    name = factory.Faker('name')

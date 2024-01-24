import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'user.User'

    email = factory.Faker("email")
    password = factory.Faker("password")
    name = factory.Faker('name')

import random

import factory

from projeto_final_poo.db.models import Address, Client, Schedule, Service


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Sequence(lambda n: f'test{n}')
    phone_number = factory.Faker('phone_number', locale='pt_BR')


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    street = factory.Faker('street_address')
    neighborhood = factory.Faker('street_name')
    reference = factory.Faker('secondary_address')
    number = factory.Faker('building_number')
    client_id = 1


class ServiceFactory(factory.Factory):
    class Meta:
        model = Service

    type = factory.Sequence(lambda n: f'service_type_{n}')
    description = factory.Faker('sentence', nb_words=4)
    price = factory.LazyAttribute(
        lambda _: round(random.uniform(10.00, 500.00), 2)
    )


class ScheduleFactory(factory.Factory):
    class Meta:
        model = Schedule

    date = factory.Faker('date_this_year')
    shift = factory.Faker(
        'random_element', elements=['morning', 'afternoon', 'evening']
    )
    description = factory.Faker('sentence', nb_words=6)
    client_id = 1
    service_id = 1

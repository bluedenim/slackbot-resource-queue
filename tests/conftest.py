import pytest
from mock import MagicMock

from van.res_reservation import (
    ResourceReservation,
    ResourceReservationProcessor,
)
from van.userstore import UserStore

MOCK_USERS = [
    {'id': f'user_{i}', 'name': f'User {i}', 'real_name': f'Real User {i}'}
    for i in range(1, 4)
]


@pytest.fixture
def user_store():
    mocked_load_users = MagicMock()
    mocked_load_users.return_value = MOCK_USERS
    mocked_client = MagicMock()
    mocked_store = UserStore(mocked_client)
    mocked_store._load_users = mocked_load_users

    return mocked_store


@pytest.fixture
def resource_reservation():
    reservation = ResourceReservation()
    reservation.queue('printer', 'user_1')
    reservation.queue('printer', 'user_2')

    reservation.queue('printer2', 'user_1')
    return reservation


@pytest.fixture
def reservation_processor(resource_reservation, user_store):
    processor = ResourceReservationProcessor(user_store)
    processor.reservations = resource_reservation
    return processor

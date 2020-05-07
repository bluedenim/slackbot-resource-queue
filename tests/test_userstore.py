import pytest
from mock import MagicMock

from tests.conftest import MOCK_USERS
from van.userstore import UserStore


@pytest.fixture
def slack_web_client():
    mocked_client = MagicMock()
    mocked_api_call = MagicMock(return_value={
        'ok': True,
        'members': MOCK_USERS,
    })
    mocked_users_info = MagicMock()

    mocked_client.api_call = mocked_api_call
    mocked_client.users_info = mocked_users_info
    return mocked_client


def test_load_users(slack_web_client):
    user_store = UserStore(slack_web_client)
    assert user_store._load_users() == MOCK_USERS


def test_load_users_error(slack_web_client):
    slack_web_client.api_call = MagicMock(side_effect=Exception('ha ha ha'))
    user_store = UserStore(slack_web_client)
    with pytest.raises(Exception):
        user_store._load_users()


def test_lookup_user_info(slack_web_client):
    user_info = {
        'id': '12345',
        'name': 'jsmith',
    }
    slack_web_client.users_info.return_value = user_info
    user_store = UserStore(slack_web_client)
    assert user_store.lookup_user_info('12345') == user_info


def test_lookup_user_info_error(slack_web_client):
    slack_web_client.users_info.side_effect = Exception('ha ha ha')
    user_store = UserStore(slack_web_client)
    assert user_store.lookup_user_info('12345') is None


def test_get_users(slack_web_client):
    user_store = UserStore(slack_web_client)
    user_store._load_users = MagicMock(return_value=MOCK_USERS)
    users = user_store.get_users()

    for mock_user in MOCK_USERS:
        assert users[mock_user['id']] == mock_user
        assert user_store.get_cached_user_info(mock_user['id']) == mock_user


def test_search_for_user(slack_web_client):
    user_store = UserStore(slack_web_client)
    user_store._load_users = MagicMock(return_value=MOCK_USERS)

    for mock_user in MOCK_USERS:
        assert user_store.search_for_user(mock_user['name']) == mock_user
        assert user_store.search_for_user(mock_user['real_name']) == mock_user


if __name__ == '__main__':
    pytest.main()

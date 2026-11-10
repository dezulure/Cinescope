import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from config.credentials import ADMIN_CREDS


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):  # session — фикстура
    return ApiManager(session=session)  # session — объект requests.Session


@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(api_manager, authenticated_superadmin, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user


@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user):
    api_manager.auth_api.register_user(test_user)
    api_manager.auth_api.authenticate(user_creds=(test_user["email"], test_user["password"]))
    return test_user


@pytest.fixture(scope="function")
def authenticated_superadmin(api_manager):
    api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))


@pytest.fixture(scope="function")
def test_movie():
    return {
        "name": DataGenerator.generate_random_name_movie(),
        "imageUrl": DataGenerator.generate_random_image_url(),
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_description(),
        "location": DataGenerator.generate_location(),
        "published": DataGenerator.generate_random_published_status(),
        "genreId": DataGenerator.generate_genre_id()

    }


@pytest.fixture(scope="function")
def incomplete_test_movie():
    return {
        "imageUrl": DataGenerator.generate_random_image_url(),
        "description": DataGenerator.generate_description(),
        "location": DataGenerator.generate_location(),
        "published": DataGenerator.generate_random_published_status(),

    }


@pytest.fixture(scope="function")
def test_movie_update():
    return {
        "name": DataGenerator.generate_random_name_movie(),
        "imageUrl": DataGenerator.generate_random_image_url(),
        "price": DataGenerator.generate_random_price()

    }


@pytest.fixture(scope="function")
def test_movie_update_incorrect():
    return {
        "name": "",
        "imageUrl": DataGenerator.generate_random_int(),
        "price": "null"

    }


@pytest.fixture(scope="function")
def created_movie(api_manager, test_movie, authenticated_superadmin):
    response = api_manager.movies_api.create_movie(test_movie).json()
    test_movie["id"] = response["id"]
    yield test_movie
    api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))
    api_manager.movies_api.delete_movie(test_movie["id"], expected_status=200)


@pytest.fixture(scope="function")
def movie_to_delete(api_manager, test_movie, authenticated_superadmin):
    return api_manager.movies_api.create_movie(test_movie).json()

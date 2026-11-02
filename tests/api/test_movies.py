import pytest
from config.credentials import USERS_CREDS,ADMIN_CREDS


class TestMoviesPositive:
    def test_create_movie(self, api_manager, test_movie, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_data = create_response.json()
        assert create_data["name"] == test_movie["name"]
        assert create_data["description"] == test_movie["description"]
        assert create_data["location"] == test_movie["location"]

    def test_get_movies(self, api_manager, authenticated_user):
        get_response = api_manager.movies_api.get_movies({"pageSize": 20, "page": 5, "locations": "MSK"})
        get_data = get_response.json()
        assert get_data["pageSize"] == 20
        assert get_data["page"] == 5

        for location in get_data["movies"]:
            assert location["location"] == "MSK"

    def test_get_movie(self, api_manager, authenticated_superadmin, test_movie):
        create_response = api_manager.movies_api.create_movie(test_movie)
        movie_id = create_response.json()["id"]
        api_manager.auth_api.reset_session_headers()
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        get_response = api_manager.movies_api.get_current_movie(movie_id)
        assert get_response.json()["id"] == movie_id

    def test_delete_movie(self, api_manager, test_movie, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_id = create_response.json()["id"]
        delete_response = api_manager.movies_api.delete_movie(create_id)
        delete_id = delete_response.json()["id"]
        assert delete_id == create_id
        get_response = api_manager.movies_api.get_current_movie(delete_id, expected_status=404)
        assert get_response.status_code == 404

    def test_update_movie(self, api_manager, test_movie, test_movie_update, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_data = create_response.json()
        movie_id = create_data["id"]
        update_response = api_manager.movies_api.update_movie(movie_id,test_movie_update)
        update_data = update_response.json()
        assert update_data["id"] == movie_id

        for field in ("name", "imageUrl", "price"):
            assert update_data[field] != create_data[field]

        get_response = api_manager.movies_api.get_current_movie(movie_id)
        saved_data = get_response.json()

        for field in ("name", "imageUrl", "price"):
            assert saved_data[field] == update_data[field]


class TestMovieNegative:
    def test_create_movie_by_user(self, api_manager, test_movie, authenticated_user):
        api_manager.movies_api.create_movie(test_movie, expected_status=403)

    def test_create_movie_incomplete_body(self, api_manager, incomplete_test_movie, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(incomplete_test_movie, expected_status=400)
        response_data = create_response.json()
        assert response_data["error"] == "Bad Request"

        for field in ("name", "price", "genreId"):
            assert (
                    f"Поле {field} не может быть пустым"
                    in response_data["message"]
            )

    def test_delete_movie_by_user(self, api_manager, test_movie, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_id = create_response.json()["id"]
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        api_manager.movies_api.delete_movie(create_id, expected_status=403)
        api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))
        get_response = api_manager.movies_api.get_current_movie(create_id)
        assert get_response.json()["id"] == create_id

    def test_update_movie_by_user(self, api_manager, test_movie, authenticated_superadmin, test_movie_update):
        create_response = api_manager.movies_api.create_movie(test_movie)
        before = create_response.json()
        create_id = create_response.json()["id"]
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        api_manager.movies_api.update_movie(create_id, test_movie_update, expected_status=403)
        api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))
        after = api_manager.movies_api.get_current_movie(create_id).json()
        for field in ("name", "imageUrl", "price"):
            assert after[field] == before[field]

    def test_update_movie_incorrect_body(self, api_manager, test_movie, authenticated_superadmin,test_movie_update_incorrect):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_id = create_response.json()["id"]
        update_response = api_manager.movies_api.update_movie(create_id, test_movie_update_incorrect,expected_status=400)
        update_data = update_response.json()
        assert update_data["error"] == "Bad Request"
        assert update_data["message"]

    def test_get_movies_invalid_page(self, api_manager, authenticated_user):
        response = api_manager.movies_api.get_movies({"page": 0},expected_status=400)
        response_data = response.json()

        assert response_data["error"] == "Bad Request"
        assert "Поле page имеет минимальную величину 1" in response_data["message"]

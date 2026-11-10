from config.credentials import USERS_CREDS, ADMIN_CREDS


class TestMoviesNegative:
    def test_create_movie_by_user(self, api_manager, test_movie, authenticated_user):
        api_manager.movies_api.create_movie(test_movie, expected_status=403)

    def test_create_movie_incomplete_body(self, api_manager, incomplete_test_movie, authenticated_superadmin):
        create_response = api_manager.movies_api.create_movie(incomplete_test_movie, expected_status=400)
        response_data = create_response.json()
        assert response_data["error"] == "Bad Request"

        assert "name should not be empty" in response_data["message"]
        assert "Поле name должно быть строкой" in response_data["message"]
        for field in ("price", "genreId"):
            assert f"Поле {field} должно быть числом" in response_data["message"]

    def test_delete_movie_by_user(self, api_manager, created_movie):
        create_id = created_movie["id"]
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        api_manager.movies_api.delete_movie(create_id, expected_status=403)
        api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))
        get_response = api_manager.movies_api.get_current_movie(create_id)
        assert get_response.json()["id"] == create_id

    def test_update_movie_by_user(self, api_manager, created_movie, test_movie_update):
        before = created_movie
        create_id = created_movie["id"]
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        api_manager.movies_api.update_movie(create_id, test_movie_update, expected_status=403)
        api_manager.auth_api.authenticate(user_creds=(ADMIN_CREDS["email"], ADMIN_CREDS["password"]))
        after = api_manager.movies_api.get_current_movie(create_id).json()
        for field in ("name", "imageUrl", "price"):
            assert after[field] == before[field]

    def test_update_movie_incorrect_body(self, api_manager, created_movie, test_movie_update_incorrect):
        create_id = created_movie["id"]
        update_response = api_manager.movies_api.update_movie(create_id, test_movie_update_incorrect, expected_status=400)
        update_data = update_response.json()
        assert update_data["error"] == "Bad Request"
        assert "Поле price должно быть числом" in update_data["message"]
        assert "Поле imageUrl должно быть строкой" in update_data["message"]

    def test_get_movies_invalid_page(self, api_manager, authenticated_user):
        response = api_manager.movies_api.get_movies({"page": 0}, expected_status=400)
        response_data = response.json()

        assert response_data["error"] == "Bad Request"
        assert "Поле page имеет минимальную величину 1" in response_data["message"]

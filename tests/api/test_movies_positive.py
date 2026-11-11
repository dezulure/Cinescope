from config.credentials import USERS_CREDS, ADMIN_CREDS


class TestMoviesPositive:
    def test_create_movie(self,api_manager,created_movie):
        get_data = api_manager.movies_api.get_current_movie(movie_id=created_movie["id"]).json()
        assert get_data["name"] == created_movie["name"]
        assert get_data["description"] == created_movie["description"]
        assert get_data["location"] == created_movie["location"]

    def test_get_movies(self, api_manager, authenticated_user):
        get_response = api_manager.movies_api.get_movies({"pageSize": 20, "page": 5, "locations": ["MSK"]})
        get_data = get_response.json()
        assert get_data["pageSize"] == 20
        assert get_data["page"] == 5

        for location in get_data["movies"]:
            assert location["location"] == "MSK"

    def test_get_movie(self, api_manager, created_movie):
        movie_id = created_movie["id"]
        api_manager.auth_api.authenticate(user_creds=(USERS_CREDS["email"], USERS_CREDS["password"]))
        get_response = api_manager.movies_api.get_current_movie(movie_id)
        assert get_response.json()["id"] == movie_id

    def test_delete_movie(self, api_manager, test_movie, authenticated_superadmin):
        create_id = api_manager.movies_api.create_movie(test_movie).json()["id"]
        delete_response = api_manager.movies_api.delete_movie(create_id)
        delete_id = delete_response.json()["id"]
        assert delete_id == create_id
        api_manager.movies_api.get_current_movie(delete_id, expected_status=404)

    def test_update_movie(self, api_manager, created_movie, test_movie_update):
        movie_id = created_movie["id"]
        update_response = api_manager.movies_api.update_movie(movie_id, test_movie_update)
        update_data = update_response.json()
        assert update_data["name"] == test_movie_update["name"]
        assert update_data["price"] == test_movie_update["price"]
        assert update_data["imageUrl"] == test_movie_update["imageUrl"]

        get_response = api_manager.movies_api.get_current_movie(movie_id)
        saved_data = get_response.json()
        assert saved_data["name"] == update_data["name"]
        assert saved_data["price"] == update_data["price"]
        assert saved_data["imageUrl"] == update_data["imageUrl"]

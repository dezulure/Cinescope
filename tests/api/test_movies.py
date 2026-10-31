import pytest


class TestMoviesPositive:
    @pytest.mark.usefixtures("authenticated_superadmin")
    def test_create_movie(self, api_manager, test_movie):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_data = create_response.json()
        assert create_data["name"] == test_movie["name"]
        assert create_data["description"] == test_movie["description"]
        assert create_data["location"] == test_movie["location"]

    @pytest.mark.usefixtures("authenticated_user")
    def test_get_movies(self, api_manager):
        get_response = api_manager.movies_api.get_movies({"pageSize": 20, "page": 5, "locations": "MSK"})
        get_data = get_response.json()
        assert get_data["pageSize"] == 20
        assert get_data["page"] == 5
        for location in get_data["movies"]:
            assert location["location"] == "MSK"

    # @pytest.mark.usefixtures("authenticated_user")
    # def test_get_movie(self, api_manager, test_movie):

    @pytest.mark.usefixtures("authenticated_superadmin")
    def test_delete_movie(self, api_manager, test_movie):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_id = create_response.json()["id"]
        delete_response = api_manager.movies_api.delete_movie(create_id)
        delete_id = delete_response.json()["id"]
        assert delete_id == create_id
        get_response = api_manager.movies_api.get_current_movie(delete_id, expected_status=404)
        assert get_response.status_code == 404

    @pytest.mark.usefixtures("authenticated_superadmin")
    def test_update_movie(self, api_manager, test_movie, test_movie_update):
        create_response = api_manager.movies_api.create_movie(test_movie)
        create_id = create_response.json()["id"]
        update_response = api_manager.movies_api.update_movie(create_id, test_movie_update)
        update_data = update_response.json()
        assert create_response.json()["name"] != update_data["name"]
        assert create_response.json()["imageUrl"] != update_data["imageUrl"]
        assert create_response.json()["price"] != update_data["price"]

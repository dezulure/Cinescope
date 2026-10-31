from utils.data_generator import DataGenerator
import pytest


class TestAuth:

    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    def test_get_user_info(self, api_manager, registered_user):
        response = api_manager.user_api.get_user_info(user_id=registered_user["id"])
        response_data = response.json()

        assert response_data["id"] == registered_user["id"]
        assert response_data["email"] == registered_user["email"]

    @pytest.mark.usefixtures("authenticated_superadmin")
    def test_register_more_user_and_delete_them(self, api_manager, test_user):
        ids = []
        for _ in range(3):
            user_data = test_user.copy()
            user_data["email"] = DataGenerator.generate_random_email()

            response = api_manager.auth_api.register_user(user_data)
            ids.append(response.json()["id"])

        api_manager.user_api.delete_users(*ids)

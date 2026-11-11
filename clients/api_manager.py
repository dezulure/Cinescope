from clients.auth_api import AuthApi
from clients.movies_api import MoviesApi
from clients.user_api import UserApi

class ApiManager:
    def __init__(self,session):
        # Сохраняем сессию, чтобы все API-классы использовали один requests.Session
        self.session = session
        # Создаём API-клиенты, передавая им ту же сессию
        self.auth_api = AuthApi(session)  #AuthApi сохраняет ту же сессию
        self.user_api = UserApi(session)  #UserApi сохраняет ту же сессию
        self.movies_api = MoviesApi(session)  # MoviesApi сохраняет ту же сессию

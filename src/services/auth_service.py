from src.handlers.auth.auth_handler import AuthHandler
from src.utils.logger import log_time

class AuthService:
    def __init__(self, session):
        self.auth_handler = AuthHandler(session)

    def login(self, email: str, password: str):
        log_time('Authenticate user')
        user = self.auth_handler.authenticate_user(email, password)
        token = self.auth_handler.create_token(user)
        log_time('Create Token')
        
        return token
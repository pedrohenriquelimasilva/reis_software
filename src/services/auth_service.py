from src.handlers.auth.auth_handler import AuthHandler

class AuthService:
    def __init__(self, session):
        self.auth_handler = AuthHandler(session)

    def login(self, email: str, password: str):
        user = self.auth_handler.authenticate_user(email, password)
        token = self.auth_handler.create_token(user)
        
        return token
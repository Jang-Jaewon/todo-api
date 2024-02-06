import random
from datetime import datetime, timedelta

import bcrypt
from jose import jwt


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "d2d702cad782adc8f3cf1667f10b7d0d47496c1a0fc16a6bacc542c9c15ddec7"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {"sub": username, "exp": datetime.now() + timedelta(days=1)},
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        return payload["sub"]

    @staticmethod
    def create_otp() -> int:
        return random.randint(1000, 9999)

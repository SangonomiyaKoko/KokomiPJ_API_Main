# -*- coding: utf-8 -*-

import hashlib
from jose import jwt

class API_Secruity:
    _instance = None
    SECRET_KEY = "kokomi"
    ALGORITHM = "HS256"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def encode_password(
        self,
        password: str
    ) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def encode_token(
        self,
        to_encode: dict
    ) -> str:
        encoded_str = jwt.encode(
            claims=to_encode, 
            key=self.SECRET_KEY, 
            algorithm=self.ALGORITHM
        )
        return encoded_str

    def decode_token(
        self,
        token: str
    ) -> tuple[str, str] | tuple[None, None]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            role: str = payload.get("role")
            return username, role
        except:
            return None, None
        
    def create_access_token(
        self, 
        data: dict
    ) -> str:
        to_encode = data.copy()
        encoded_str = self.encode_token(to_encode=to_encode)
        return encoded_str

    def verify_password(
        self, 
        plain_password: str, 
        hashed_password: str
    ) -> bool:
        hashed_plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
        if hashed_plain_password == hashed_password:
            return True
        else:
            return False
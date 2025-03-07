from datetime import datetime, timedelta
from hashlib import sha256
import json
from app.config import Config
from app.modules.token import Token


class User:
    def __init__(self, username: str, password: str = None):
        self.username = username
        self.password = sha256(password.encode()).hexdigest() if password else None
        self._db = Config()._database

    def authenticate(self, token: str) -> bool:
        """Authenticate user with token"""
        try:
            data = self._db.execute(
                "SELECT client_tokens FROM users WHERE username = ?",
                (self.username,),
            )
            data = json.loads(data[0][0])
        except Exception:
            return False

        expired_keys = [
            key for key in data.keys()
            if datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f") < datetime.now()
        ]

        for key in expired_keys:
            del data[key]

        self._db.execute(
            "UPDATE users SET client_tokens = ? WHERE username = ?",
            (json.dumps(data), self.username),
        )

        return any(token in v for v in data.values())

    def register(self, inviteid: str) -> tuple[bool, bool]:
        """Register new user with invite"""
        if not self._db.execute("SELECT * FROM invites WHERE url = ?", (inviteid,)):
            return False, True

        try:
            self._db.execute(
                "INSERT INTO users VALUES (?, ?, '{}')",
                (self.username, self.password),
            )
            return True, False
        except Exception:
            return False, False

    def login(self, password: str) -> str | bool:
        """Login user and return token"""
        try:
            data = self._db.execute(
                "SELECT client_tokens FROM users WHERE username = ?",
                (self.username,),
            )
            data = json.loads(data[0][0])         
        except Exception:
            return False

        expired_keys = [
            key for key in data.keys()
            if datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f") < datetime.now()
        ]

        for key in expired_keys:
            del data[key]

        self._db.execute(
            "UPDATE users SET client_tokens = ? WHERE username = ?",
            (json.dumps(data), self.username),
        )

        check = self._db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (self.username, password),
        )

        if check:
            token = Token.generate_token()

            data = self._db.execute(
                "SELECT client_tokens FROM users WHERE username = ?",
                (self.username,),
            )
            data = json.loads(data[0][0])
            data[str(datetime.now() + timedelta(days=7))] = token
            self._db.execute(
                "UPDATE users SET client_tokens = ? WHERE username = ?",
                (json.dumps(data), self.username),
            )
            return token
        return False

    def logout(self, token: str) -> bool:
        """Logout user by removing token"""
        try:
            data = self._db.execute(
                "SELECT client_tokens FROM users WHERE username = ?",
                (self.username,),
            )
            data = json.loads(data[0][0])
            data = {k: v for k, v in data.items() if v != token}
            self._db.execute(
                "UPDATE users SET client_tokens = ? WHERE username = ?",
                (json.dumps(data), self.username),
            )
            return True
        except Exception:
            return False

    def info(self) -> dict:
        """Return user info"""
        try:
            data = self._db.execute(
                "SELECT * FROM users WHERE username = ?",
                (self.username,),
            )
            return {
                "username": data[0][0],
                "password": data[0][1],
                "client_tokens": json.loads(data[0][2]),
            }
        except Exception:
            return {}

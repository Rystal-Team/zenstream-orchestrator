from app.config import Config
from random import choice
from string import ascii_letters, digits


class Invite:
    def __init__(self):
        self._db = Config()._database

    def validate(self, inviteid: str) -> bool:
        """
        Validate an invite URL.

        Args:
            inviteid (str): The invite URL to validate

        Returns:
            bool: True if invite exists, False otherwise
        """
        result = self._db.execute("SELECT * FROM invites WHERE url = ?", (inviteid,))
        return bool(result)

    def generate(self) -> str:
        """
        Generate a new invite URL.

        Returns:
            str: The invite URL
        """
        inviteid = "".join(choice(ascii_letters + digits) for _ in range(64))
        self._db.execute("INSERT INTO invites VALUES (?)", (inviteid,))
        return inviteid

    def delete(self, inviteid: str) -> bool:
        """
        Delete an invite URL.

        Args:
            inviteid (str): The invite URL to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if type(self._db.execute("DELETE FROM invites WHERE url = ?", (inviteid,))) is list:
            return True
        return False
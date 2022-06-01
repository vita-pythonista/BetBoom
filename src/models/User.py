import hashlib
from typing import List

from . import Contact


class User:
    user_id: int = 1
    password_hash: str
    login: str
    contacts: List[Contact]

    def __init__(self, login: str, password: str):
        self.user_id = self.reserve_user_id()
        self.login = login
        self.password_hash = self.calculate_password_hash(password)
        self.contacts = []

    def api_mapping(self) -> dict:
        return {
            'login': self.login,
            'contacts': [contact.api_mapping() for contact in self.contacts],
        }

    @classmethod
    def reserve_user_id(cls) -> int:
        cls.user_id += 1
        return cls.user_id

    @staticmethod
    def calculate_password_hash(password: str) -> str:
        return hashlib.md5(bytes(password, 'utf8')).hexdigest()

    def check_password(self, password: str):
        return self.calculate_password_hash(password) == self.password_hash

    def add_contact(self, contact: Contact) -> bool:
        if contact not in self.contacts:
            self.contacts.append(contact)
            return True
        return False

    def remove_contact(self, contact_id: int) -> bool:
        removed = False
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                self.contacts.remove(contact)
                removed = True
        return removed


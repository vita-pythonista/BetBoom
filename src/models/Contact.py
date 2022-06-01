class Contact:
    contact_id: int = 1
    contact_type: str
    content: str

    def __init__(self, contact_type: str, content: str):
        self.contact_id = self.reserve_contact_id()
        self.contact_type = contact_type
        self.content = content

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False
        return self.contact_type == other.contact_type and self.content == other.content

    def api_mapping(self) -> dict:
        return {
            'id': self.contact_id,
            'type': self.contact_type,
            'content': self.content
        }

    @classmethod
    def reserve_contact_id(cls) -> int:
        cls.contact_id += 1
        return cls.contact_id

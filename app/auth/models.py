from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.email = row["email"]
        self.user_name = row["user_name"]
        self.is_active = bool(row.get("is_active", 1))
    
    @staticmethod
    def from_row(row):
        if not row:
            return None
        return User(row)
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, row:dict, roles:list=None, permissions:list=None):
        self.id = row["id"]
        self.email = row["email"]
        self.user_name = row["user_name"]
        self.is_active = bool(row.get("is_active", 1))

        self.roles = [r.lower() for r in (roles or [])]
        self.permissions = [p.lower() for p in (permissions or [])]
    
    def has_role(self, role_name:str) -> bool:
        return role_name in self.roles
    
    def has_permission(self, permission_name:str) -> bool:
        return permission_name in self.permissions

    @classmethod
    def from_row(cls, row:dict, roles:list=None, permissions:list=None) -> "User":
        if not row:
            return None
        return cls(row, roles, permissions)
    
import json

class User:
    def __init__(self, username, password, pairs=None):
        self.username = username
        self.password = password
        self.pairs = pairs if pairs is not None else []
        
    def add_pair(self, website, password):
        self.pairs.append({"website": website, "password": password})
        
    def list_pairs(self):
        return self.pairs
        
    def to_dict(self):
        return{
            "username": self.username,
            "password": self.password,
            "pairs": self.pairs
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"], data["pairs"])
    
    @staticmethod
    def read_users_from_json(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                users_data = data.get("users", [])
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []
            
        return [User.from_dict(user_data) for user_data in users_data]
    
    @staticmethod
    def write_users_to_json(users, filename):
        data = {"users": [user.to_dict() for user in users]}
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            
    
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class User:
    def __init__(self, username, password, pairs=None):
        self.username = username
        self.password = password
        self.pairs = pairs if pairs is not None else []
        
    def add_pair(self, website, password):
        key = self.derive_key()
        cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')
        encrypted_password = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
        self.pairs.append({"website": website, "password": b64encode(encrypted_password).decode('utf-8')})
        
    def list_pairs(self):
        decrypted_pairs = []
        key = self.derive_key()
        for pair in self.pairs:
            cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')
            encrypted_password = b64decode(pair['password'])
            decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')
            decrypted_pairs.append({"website": pair['website'], "password": decrypted_password})
        return decrypted_pairs
    
    def derive_key(self):
        return PBKDF2(self.password,b'salt', 32, 100000)
        
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
            
    
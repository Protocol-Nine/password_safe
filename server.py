import socket
import hashlib
import json
from user import User  # Import the User class from your existing project

def handle_request(request):
    parts = request.split()
    command = parts[0]
    if command == "LOG_IN":
        return handle_login(parts[1], parts[2])
    elif command == "LIST_PAIRS":
        return handle_list_pairs(parts[1])
    else:
        return "ERROR: Invalid command"

def handle_login(username, password):
    users = User.read_users_from_json("users.json")
    for user in users:
        if user.username == username:
            salt = bytes.fromhex(user.password[:32])
            salted_password = salt + password.encode('utf-8')
            hashed_password = hashlib.sha256(salted_password).hexdigest()
            if hashed_password == user.password[32:]:
                return "SUCCESS"
            else:
                return "FAILURE: Invalid username or password"
    return "FAILURE: Invalid username or password"

def handle_list_pairs(username):
    users = User.read_users_from_json("users.json")
    for user in users:
        if user.username == username:
            pairs = user.list_pairs()
            return pairs
    return None  # Return None if the user is not found


def start_server():
    server_address = ('', 8888)  # Listen on all available interfaces, port 8888
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)  # Allow only one client to connect at a time

    print("Server started. Listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request}")

        response = handle_request(request)
        print(f"Sending response: {response}")

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    start_server()

import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import json

def send_request(request):
    server_address = ('192.168.0.233', 8888)  # IP address of Raspberry Pi
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    client_socket.sendall(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response

def log_in():
    username = entryName.get()
    password = entryPassword.get()
    request = f"LOG_IN {username} {password}"
    response = send_request(request)
    if response == "SUCCESS":
        buttonListPairs.config(state=tk.NORMAL)
        buttonAddPair.config(state=tk.NORMAL)
        entryName.config(state=tk.DISABLED)
        entryPassword.config(state=tk.DISABLED)
        buttonLogIn.config(text="Log Out")
        buttonLogIn.config(command=log_out)
    else:
        messagebox.showerror("Error", "Login failed. Please try again.")

def log_out():
    buttonListPairs.config(state=tk.DISABLED)
    buttonAddPair.config(state=tk.DISABLED)
    entryName.config(state=tk.NORMAL)
    entryPassword.config(state=tk.NORMAL)
    buttonLogIn.config(text="Log In")
    buttonLogIn.config(command=log_in)

def list_pairs():
    # Retrieve password pairs from the server
    username = entryName.get()
    request = f"LIST_PAIRS {username}"
    response = send_request(request)
    
    try:
        pairs = json.loads(response)
        if pairs:
            pair_info = "\n".join([f"Website: {pair['website']}, Password: {pair['password']}" for pair in pairs])
            messagebox.showinfo("Password Pairs", pair_info)
        else:
            messagebox.showinfo("Password Pairs", "No password pairs found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding server response.")

def add_pair():
    # Get website and password from the user
    website = simpledialog.askstring("Input", "Enter website:")
    password = simpledialog.askstring("Input", "Enter password:")
    if website and password:
        username = entryName.get()
        request = f"ADD_PAIR {username} {website} {password}"
        response = send_request(request)
        if response == "SUCCESS":
            messagebox.showinfo("Success", "Password pair added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add password pair.")
    else:
        messagebox.showerror("Error", "Please enter both website and password.")

# GUI setup
app = tk.Tk()
app.geometry("300x200")
app.title("Password Safe")

labelName = tk.Label(app, text="Username:")
labelName.pack()
entryName = tk.Entry(app)
entryName.pack()

labelPassword = tk.Label(app, text="Password:")
labelPassword.pack()
entryPassword = tk.Entry(app, show="*")
entryPassword.pack()

buttonLogIn = tk.Button(app, text="Log In", command=log_in)
buttonLogIn.pack()

buttonListPairs = tk.Button(app, text="List Password Pairs", command=list_pairs, state=tk.DISABLED)
buttonListPairs.pack()

buttonAddPair = tk.Button(app, text="Add Password Pair", command=add_pair, state=tk.DISABLED)
buttonAddPair.pack()

app.mainloop()

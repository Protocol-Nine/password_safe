import tkinter as tk
from tkinter import messagebox
import socket

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
        messagebox.showinfo("Success", "Logged in successfully.")
        # Enable buttons to interact with the server's database
        buttonListPairs.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Error", "Login failed. Please try again.")

def list_pairs():
    # Retrieve password pairs from the server and display them in a messagebox
    username = entryName.get()
    request = f"LIST_PAIRS {username}"
    response = send_request(request)
    messagebox.showinfo("Password Pairs", response)

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

app.mainloop()
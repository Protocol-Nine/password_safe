import os
import hashlib
import tkinter
from tkinter import messagebox

from user import User

def generate_salt():
    # Generates a 16 byte salt
    return os.urandom(16)

def get_users():
    try:
        users = User.read_users_from_json("users.json")
    except FileNotFoundError:
        users = []
    return users

def add():
    #accepting input from the user
    username = entryName.get()
    # accepting password input from the user
    password = entryPassword.get()
    if username and password:
        salt = generate_salt()
        salted_password = salt + password.encode('utf-8')
        hashed_password = salt.hex() + hashlib.sha256(salted_password).hexdigest()
        
        new_user = User(username, hashed_password)
        
        users = get_users()
            
        users.append(new_user)
        User.write_users_to_json(users, "users.json")
        messagebox.showinfo("Success", "Password added.")
    else:
        messagebox.showerror("Error", "Please enter both fields")
        
def check():
    # Check if the password for a specified user is correct.
    username = entryName.get()
    password = entryPassword.get()
    
    passwords = {}
    
    users = get_users()
        
    user_found = False
    for user in users:
        if user.username == username:
            salt = bytes.fromhex(user.password[:32])
            salted_password = salt + password.encode('utf-8')
            hashed_password = hashlib.sha256(salted_password).hexdigest()
            if hashed_password == user.password[32:]:
                user_found = True
                messagebox.showinfo("Passwords", "Correct Password.")
            break
    if not user_found:
        messagebox.showinfo("Passwords", "Username or Password is Incorrect.")
        
def delete():
    # Removes a user password pair from the password file for the current user input
    username = entryName.get()
    temp_passwords = []
    try:
        with open("passwords.txt", 'r') as file:
            for line in file:
                lineValues = line.split(' ')
                if lineValues[0] != username:
                    temp_passwords.append(line)
        #writing the modified data back to the file
        with open("passwords.txt", 'w') as file:
            for line in temp_passwords:
                f.write(line)
        messagebox.showinfo(
            "Success", f"User {username} deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting user {username}: {e}")
        
        
def clear():
    # Clear the contents of the passwords file
    open("passwords.txt", 'w').close()
    messagebox.showinfo("Success", "Cleared password list.")
        
        
if __name__ == "__main__":
    app = tkinter.Tk()
    app.geometry("560x270")
    app.title("ELE 408 Password Manager")
    
    # Username block
    labelName = tkinter.Label(app, text="USERNAME:")
    labelName.grid(row=0, column=0, padx=15, pady=15)
    entryName = tkinter.Entry(app)
    entryName.grid(row=0, column=1, padx=15, pady=15)
    
    # Password block
    labelPassword = tkinter.Label(app, text="PASSWORD:")
    labelPassword.grid(row=1, column=0, padx=10, pady=5)
    entryPassword = tkinter.Entry(app)
    entryPassword.grid(row=1, column=1, padx=10, pady=5)
    
    # Add button
    buttonAdd = tkinter.Button(app, text="Add", command=add)
    buttonAdd.grid(row=2, column=0, padx=15, pady=8, sticky="we")
    
    # Check button
    buttonGet = tkinter.Button(app, text="Validate Pair", command=check)
    buttonGet.grid(row=2, column=1, padx=15, pady=8, sticky="we")
    
    # Delete button
    buttonDelete = tkinter.Button(app, text="Delete User Entry", command=delete)
    buttonDelete.grid(row=3, column=1, padx=15, pady=8, sticky="we")
    
    #Clear button
    buttonClear = tkinter.Button(app, text="Clear", command=clear)
    buttonClear.grid(row=3, column=0, padx=15, pady=8, sticky="we")
    
    app.mainloop()
import os
import hashlib
import tkinter
from tkinter import messagebox

from user import User

def generate_salt():
    # Generates a 16 byte salt
    return os.urandom(16)

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
        
        users = User.read_users_from_json("users.json")
            
        users.append(new_user)
        User.write_users_to_json(users, "users.json")
        messagebox.showinfo("Success", "User added.")
    else:
        messagebox.showerror("Error", "Please enter both fields")
        
def log_in():
    # Check if the password for a specified user is correct.
    username = entryName.get()
    password = entryPassword.get()
    
    passwords = {}
    
    users = User.read_users_from_json("users.json")
        
    user_found = False
    for user in users:
        if user.username == username:
            salt = bytes.fromhex(user.password[:32])
            salted_password = salt + password.encode('utf-8')
            hashed_password = hashlib.sha256(salted_password).hexdigest()
            if hashed_password == user.password[32:]:
                user_found = True
                messagebox.showinfo("Passwords", "Correct Password.")
                
                buttonAddPair.config(state=tkinter.NORMAL)
                buttonListPairs.config(state=tkinter.NORMAL)
                labelWebsite.config(state=tkinter.NORMAL)
                entryWebsite.config(state=tkinter.NORMAL)
                labelPairPassword.config(state=tkinter.NORMAL)
                entryPairPassword.config(state=tkinter.NORMAL)
                
                labelName.config(state=tkinter.DISABLED)
                entryName.config(state=tkinter.DISABLED)
                labelPassword.config(state=tkinter.DISABLED)
                entryPassword.config(state=tkinter.DISABLED)
                buttonAdd.config(state=tkinter.DISABLED)
                buttonClear.config(state=tkinter.DISABLED)
                buttonDelete.config(state=tkinter.DISABLED)
                
                buttonLogIn.config(text="Log Out")
                buttonLogIn.config(command=log_out)
            break
    if not user_found:
        messagebox.showinfo("Passwords", "Username or Password is Incorrect.")
        

def log_out():
    buttonAddPair.config(state=tkinter.DISABLED)
    buttonListPairs.config(state=tkinter.DISABLED)
    labelWebsite.config(state=tkinter.DISABLED)
    entryWebsite.config(state=tkinter.DISABLED)
    labelPairPassword.config(state=tkinter.DISABLED)
    entryPairPassword.config(state=tkinter.DISABLED)
        
    labelName.config(state=tkinter.NORMAL)
    entryName.config(state=tkinter.NORMAL)
    labelPassword.config(state=tkinter.NORMAL)
    entryPassword.config(state=tkinter.NORMAL)
    buttonAdd.config(state=tkinter.NORMAL)
    buttonClear.config(state=tkinter.NORMAL)
    buttonDelete.config(state=tkinter.NORMAL)
    
    buttonLogIn.config(text="Log In")
    buttonLogIn.config(command=log_in)

def add_pair():
    #Add a password pair for the current user
    username = entryName.get()
    website = entryWebsite.get()
    password = entryPairPassword.get()
    
    users = User.read_users_from_json("users.json")
    
    for user in users:
        if user.username == username:
            user.add_pair(website, password)
            User.write_users_to_json(users, "users.json")
            messagebox.showinfo("success", "Password pair added.")
            break
        
def list_pairs():
    # List all password pairs for the current user
    username = entryName.get()
    
    users = User.read_users_from_json("users.json")
    
    for user in users:
        if user.username == username:
            pairs = user.list_pairs()
            if pairs:
                messagebox.showinfo("Password Pairs", "\n".join([f"Website: {pair['website']}, Password: {pair['password']}" for pair in pairs]))
            else:
                messagebox.showinfo("Password Pairs", "No password pairs found.")
            break
        
def delete():
    # Removes a user password pair from the password file for the current user input
    username = entryName.get()
    
    users = User.read_users_from_json("users.json")
    
    users = [user for user in users if user.username != username]
    
    User.write_users_to_json(users, "users.json")
    
    messagebox.showinfo("Success", f"User {username} deleted permanently")
        
        
def clear():
    # Clear the contents of the passwords file
    with open("users.json", "w") as file:
        file.write("{}")
    messagebox.showinfo("Success", "Cleared password list.")
        
        
if __name__ == "__main__":
    app = tkinter.Tk()
    app.geometry("560x450")
    app.title("ELE 408 Password Safe")
    
    # Username block
    labelName = tkinter.Label(app, text="USERNAME:")
    labelName.grid(row=0, column=0, padx=15, pady=15)
    entryName = tkinter.Entry(app)
    entryName.grid(row=0, column=1, padx=15, pady=15)
    
    # Password block
    labelPassword = tkinter.Label(app, text="PASSWORD:")
    labelPassword.grid(row=1, column=0, padx=10, pady=5)
    entryPassword = tkinter.Entry(app, show="*")
    entryPassword.grid(row=1, column=1, padx=10, pady=5)
    
    # Add button
    buttonAdd = tkinter.Button(app, text="Add User", command=add)
    buttonAdd.grid(row=2, column=0, padx=15, pady=8, sticky="we")
    
    # LogIn button
    buttonLogIn = tkinter.Button(app, text="Log In", command=log_in)
    buttonLogIn.grid(row=2, column=1, padx=15, pady=8, sticky="we")    
    
    # Delete button
    buttonDelete = tkinter.Button(app, text="Delete User Entry", command=delete)
    buttonDelete.grid(row=3, column=1, padx=15, pady=8, sticky="we")
    
    #Clear button
    buttonClear = tkinter.Button(app, text="Clear Userbase", command=clear)
    buttonClear.grid(row=3, column=0, padx=15, pady=8, sticky="we")
    
    # Add password pair button
    buttonAddPair = tkinter.Button(app, text="Add Password Pair", command=add_pair, state=tkinter.DISABLED)
    buttonAddPair.grid(row=4, column=0, padx=15, pady=8, sticky="we")
    
    # List password pairs button
    buttonListPairs = tkinter.Button(app, text="List Password Pairs", command=list_pairs, state=tkinter.DISABLED)
    buttonListPairs.grid(row=4, column=1, padx=15, pady=8, sticky="we")
    
    # Website block
    labelWebsite = tkinter.Label(app, text="WEBSITE:", state=tkinter.DISABLED)
    labelWebsite.grid(row=5, column=0, padx=15, pady=15)
    entryWebsite = tkinter.Entry(app, state=tkinter.DISABLED)
    entryWebsite.grid(row=5, column=1, padx=15, pady=15)
    
    # Password Pair
    labelPairPassword = tkinter.Label(app, text="PAIR PASSWORD", state=tkinter.DISABLED)
    labelPairPassword.grid(row=6, column=0, padx=15, pady=15)
    entryPairPassword = tkinter.Entry(app, show="*", state=tkinter.DISABLED)
    entryPairPassword.grid(row=6, column=1, padx=15, pady=15)
    
    
    
    app.mainloop()
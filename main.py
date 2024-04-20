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
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        with open("passwords.txt", 'a') as f:
            f.write(f"{username} {salt.hex()} {hashed_password}\n")
        messagebox.showinfo("Success", "Password added.")
    else:
        messagebox.showerror("Error", "Please enter both fields")
        
def check():
    # Check if the password for a specified user is correct.
    username = entryName.get()
    
    passwords = {}
    try:
        with open("passwords.txt", 'r') as file:
            for line in file:
                lineValues = line.split(' ')
                passwords[lineValues[0]] = (bytes.fromhex(lineValues[1]), lineValues[2].strip())
    except:
        print("ERROR")
    
    if passwords:
        message = "Incorrect Password."
        for name, (salt, hashed_password) in passwords.items():
            if name == username:
                salted_password = salt + entryPassword.get().encode('utf-8')
                input_hashed_password = hashlib.sha256(salted_password).hexdigest()
                if input_hashed_password == hashed_password:
                    message = f"Correct Password."
                break
        else:
            message = "No Such Username Exists."
        messagebox.showinfo("Passwords", message)
    else:
        messagebox.showinfo("Passwords", "EMPTY LIST!!")
        
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
    buttonGet = tkinter.Button(app, text="Check", command=check)
    buttonGet.grid(row=2, column=1, padx=15, pady=8, sticky="we")
    
    # Delete button
    buttonDelete = tkinter.Button(app, text="Delete", command=delete)
    buttonDelete.grid(row=3, column=1, padx=15, pady=8, sticky="we")
    
    #Clear button
    buttonClear = tkinter.Button(app, text="Clear", command=clear)
    buttonClear.grid(row=4, column=0, padx=15, pady=8, sticky="we")
    
    app.mainloop()
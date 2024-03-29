import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import pickle
import hashlib
import ttkthemes
from tkinter import ttk
from ttkthemes.themed_tk import ThemedTk

passwords = []

def save_passwords(filename="passwords.bin"):
    with open(filename, "wb") as file:
        pickle.dump(passwords, file)

def load_passwords(filename="passwords.bin"):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            try:
                return pickle.load(file)
            except (pickle.UnpicklingError, EOFError):
                messagebox.showerror("Error", "Failed to load passwords. The file may be corrupted.")
    return []

def save_master_password_hash(master_password_hash):
    with open("master_password.txt", "wb") as file:
        file.write(master_password_hash)

def load_master_password_hash():
    if os.path.exists("master_password.txt"):
        with open("master_password.txt", "rb") as file:
            master_password_hash = file.read()
            return master_password_hash
    else:
        return None

def verify_master_password():
    master_password = simpledialog.askstring("Master Password", "Enter the master password:", show='*')
    if master_password:
        saved_hash = load_master_password_hash()
        if saved_hash:
            if hashlib.sha256(master_password.encode()).digest() == saved_hash:
                loaded_passwords = load_passwords()
                create_password_manager(loaded_passwords)
            else:
                messagebox.showerror("Error", "Incorrect master password")
        else:
            save_master_password_hash(hashlib.sha256(master_password.encode()).digest())
            create_password_manager([])

def add_password(website_entry, username_entry, password_entry, password_listbox):
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if website and username and password:
        passwords.append((website, username, password))
        messagebox.showinfo("Success", "Password added successfully!")
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        update_password_list(password_listbox, passwords)
        save_passwords()

def update_password_list(password_listbox, loaded_passwords):
    password_listbox.delete(0, tk.END)
    for website, username, _ in loaded_passwords:
        password_listbox.insert(tk.END, f"{website} ({username})")

def view_password(password_listbox, loaded_passwords):
    selected_index = password_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        website, username, password = loaded_passwords[index]
        messagebox.showinfo("Password", f"Website: {website}\nUsername: {username}\nPassword: {password}")
    else:
        messagebox.showerror("Error", "Please select a password entry from the list.")

def delete_password(password_listbox, loaded_passwords):
    selected_index = password_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        del loaded_passwords[index]
        update_password_list(password_listbox, loaded_passwords)
        save_passwords()
        messagebox.showinfo("Success", "Password deleted successfully!")
    else:
        messagebox.showerror("Error", "Please select a password entry from the list.")

def exit_app(root):
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def create_password_manager(loaded_passwords):
    root = ThemedTk(theme="arc")
    root.title("Secured Password Manager")

    website_label = ttk.Label(root, text="Website:")
    website_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    website_entry = ttk.Entry(root)
    website_entry.grid(row=0, column=1, padx=5, pady=5)

    username_label = ttk.Label(root, text="Username:")
    username_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    username_entry = ttk.Entry(root)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    password_label = ttk.Label(root, text="Password:")
    password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    password_entry = ttk.Entry(root, show='*')
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = ttk.Button(root, text="Add", command=lambda: add_password(website_entry, username_entry, password_entry, password_listbox))
    add_button.grid(row=3, column=0, padx=5, pady=5)

    password_listbox = tk.Listbox(root, width=40, selectmode=tk.SINGLE)
    password_listbox.grid(row=4, column=0, rowspan=4, columnspan=2, padx=5, pady=5)

    view_button = ttk.Button(root, text="View", command=lambda: view_password(password_listbox, loaded_passwords))
    view_button.grid(row=4, column=2, padx=5, pady=5)

    delete_button = ttk.Button(root, text="Delete", command=lambda: delete_password(password_listbox, loaded_passwords))
    delete_button.grid(row=5, column=2, padx=5, pady=5)

    exit_button = ttk.Button(root, text="Exit", command=lambda: exit_app(root))
    exit_button.grid(row=6, column=2, padx=5, pady=5)

    update_password_list(password_listbox, loaded_passwords)

    root.mainloop()

verify_master_password()


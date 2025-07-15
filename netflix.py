import tkinter as tk
from tkinter import PhotoImage 
import subprocess
import os

SESSION_FILE="session.txt"

def get_logged_in_user(): 
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE,"r") as file:
            data=file.read().strip().split(",")
            if len(data)==2:
                return data[0],data[1] 
    return None,None

def is_logged_in():
    username, role =get_logged_in_user()
    return username is not None

def logout_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    update_menu()
    
def open_register():
    subprocess.Popen(["python","register.py"])
    
def open_login():
    subprocess.Popen(["python","login.py"])
    root.destroy()
    
def open_dashboard():
    subprocess.Popen(["python","dashboard.py"])

def open_view_movies():
    subprocess.Popen(["python","view-movies.py"])

def open_insert_movies():
    subprocess.Popen(["python","insert-movies.py"])
    
def update_menu():
    for widget in root.winfo_children():
        widget.destroy()
    try:
        logo= PhotoImage(file="netflix.png")
        tk.Label(root, image=logo,bg="black").pack(pady=10)
        root.logo=logo
    except Exception as e:
        tk.Label(root,text="Netflix",font=("Arial",24,"bold"), fg="#e50914", bg="black").pack(pady=10)
    
    username, role=get_logged_in_user()
    if username:
        tk.Label(root,text="Καλωσήρθες στο μενού!",font=("Arial",16,"bold"),fg="white",bg="black").pack(pady=20)
        tk.Button(root, text="Πίνακας Ελέγχου",command=open_dashboard, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        if role=='admin':
            tk.Button(root, text="Προσθήκη Ταινίας",command=open_insert_movies, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        elif role=='customer':
            tk.Button(root, text="Προβολή Ταινιών",command=open_view_movies, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        tk.Button(root, text="Αποσύνδεση",command=logout_user, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
    else:
        tk.Label(root,text="Καλωσήρθες στο μενού!",font=("Arial",16,"bold"),fg="white",bg="black").pack(pady=20)
        tk.Button(root, text="Εγγραφή χρήστη",command=open_register, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        tk.Button(root, text="Σύνδεση χρήστη",command=open_login, width=20, bg="#e50914",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        tk.Button(root, text="Έξοδος",command=root.destroy, width=20, bg="gray",fg="white", font=("Arial",12,"bold")).pack(pady=10)
        
root=tk.Tk()
root.title("Κεντρικό Μενού")
root.configure(bg="black")
root.geometry("400x500")
update_menu()

root.mainloop()
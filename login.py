import tkinter as tk
from tkinter import messagebox
import mysql.connector
from connection import create_connection
from hashlib import sha256
import subprocess 
import os 

SESSION_FILE="session.txt" 

def save_session(username,role):
    with open(SESSION_FILE,"w") as file: 
                                        
                                        
        file.write(f"{username},{role}")
        
def login_user():
    identifier=entry_identifier.get().strip() 
    password=entry_password.get().strip()
    
    if not identifier or not password:
        messagebox.showerror("Σφάλμα","Όλα τα πεδία είναι υποχρεωτικά!")
        return

    password_hash=sha256(password.encode()).hexdigest()
    
    connection=create_connection()
    if not connection:
        messagebox.showerror("Σφάλμα","Αποτυχία σύνδεσης στη βάση δεδομένων.")
        return

    try:
        cursor=connection.cursor()
        
        cursor.execute(
            "SELECT username,role FROM users WHERE (username =%s OR email=%s) AND password_hash=%s",
            (identifier,identifier,password_hash)
        )
        user=cursor.fetchone()
        
        if user:
            username,role=user
            save_session(username,role)
            messagebox.showinfo("Επιτυχία",f"Καλώς ήρθες, {username} ({role})!")
            root.destroy()             
            
            if role=='admin':
                subprocess.Popen(["python","netflix.py"])                                                                                 
            else: 
                subprocess.Popen(["python","netflix.py"])
        else:
            messagebox.showerror("Σφάλμα","Λάθος όνομα χρήστη, email ή κωδικός πρόσβασης.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Σφάλμα",f"Αποτυχία ελέγχου διαπιστευτηρίων {err}")
    finally:
        cursor.close()
        connection.close()
        
root=tk.Tk()
root.title("Σύνδεση Χρήστη")

tk.Label(root,text="Όνομα χρήστη ή Email:").grid(row=0, column=0, padx=10, pady=10,sticky="e")
entry_identifier=tk.Entry(root,width=30)
entry_identifier.grid(row=0,column=1,padx=10,pady=10)

tk.Label(root,text="Κωδικός Πρόσβασης:").grid(row=1,column=0,padx=10,pady=10,sticky="e")
entry_password=tk.Entry(root,width=30,show="*")
entry_password.grid(row=1,column=1,padx=10,pady=10)

tk.Button(root, text="Σύνδεση", command=login_user).grid(row=2,column=0,columnspan=2,pady=20)

root.mainloop()
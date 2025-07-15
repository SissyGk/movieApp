import tkinter as tk
from tkinter import messagebox
import mysql.connector
from connection import create_connection
from hashlib import sha256

def register_admin():
    username=entry_username.get().strip()
    email=entry_email.get().strip()
    password=entry_password.get().strip()
    
    if not username or not email or not password:
        messagebox.showerror("Σφάλμα","Όλα τα πεδία είναι υποχρεωτικά!")
        return
    password_hash=sha256(password.encode()).hexdigest()
    
    connection=create_connection()
    if not connection:
        messagebox.showerror("Σφάλμα","Αποτυχία σύνδεσης στη βάση δεδομένων.")
        return
    
    try:
        cursor=connection.cursor()
        cursor.execute("Select * from users where username =%s",(username,))
        if cursor.fetchone():
            messagebox.showwarning("Σφάλμα","Το όνομα χρήστη υπάρχει ήδη")
            return
        cursor.execute("Select * from users where email =%s",(email,))
        if cursor.fetchone():
            messagebox.showwarning("Σφάλμα","Το email υπάρχει ήδη")
            return
        
        cursor.execute("INSERT into users(username,email,password_hash,role) values(%s,%s,%s,%s)",(username,email,password_hash,'admin'))
        connection.commit()
        messagebox.showinfo("Επιτυχία","O διαχειριστής δημιουργήθηκε με επιτυχία!")
        
        
        entry_username.delete(0,tk.END)
        entry_email.delete(0,tk.END)
        entry_password.delete(0,tk.END)
    
    except mysql.connector.Error as err:
        messagebox.showerror("Σφάλμα",f"Αποτυχία καταχώρησης: {err}")
    
    finally:
        cursor.close()
        connection.close()
    

root=tk.Tk()
root.title("Εγγραφή Διαχειριστή")


tk.Label(root, text="Όνομα Χρήστη:").grid(row=0,column=0,padx=10,pady=10,sticky="e")
entry_username=tk.Entry(root,width=30)
entry_username.grid(row=0,column=1,padx=10,pady=10)

tk.Label(root, text="Email:").grid(row=1,column=0,padx=10,pady=10,sticky="e")
entry_email=tk.Entry(root,width=30)
entry_email.grid(row=1,column=1,padx=10,pady=10)

tk.Label(root, text="Κωδικός πρόσβασης:").grid(row=2,column=0,padx=10,pady=10,sticky="e")
entry_password=tk.Entry(root,width=30,show="*")
entry_password.grid(row=2,column=1,padx=10,pady=10)

tk.Button(root, text="Εγγραφή Διαχειριστή",command=register_admin).grid(row=3, column=0,columnspan=2,pady=20)

root.mainloop()
        
        
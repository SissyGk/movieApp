import tkinter as tk
import os

SESSION_FILE = "session.txt" 

def get_logged_in_user(): 
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE,"r") as file:
            return file.read().strip()
        return None

def logout_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    root.destroy()
    import subprocess
    subprocess.Popen(["python","netflix.py"])
    
def close_dashboard():
    root.destroy()
    
  
username=get_logged_in_user()


root=tk.Tk()
root.title("Πίνακας Ελέγχου")


welcome_message=f"Καλωσήρθες, {username}!" if username else "Καλωσήρθες!"
tk.Label(root, text=welcome_message, font=("Arial",16)).pack(pady=20)
tk.Button(root, text="Έξοδος",command=close_dashboard).pack(pady=10)


root.mainloop()
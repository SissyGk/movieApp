import tkinter as tk
from tkinter import messagebox
from connection import create_connection
from PIL import Image, ImageTk
import os
import subprocess

def fetch_movies():
    connection = create_connection()
    if not connection:
        messagebox.showerror("Σφάλμα","Αποτυχία σύνδεσης στη βάση δεδομένων.")
        return[]

    try:
        cursor=connection.cursor()
        cursor.execute("Select id, title, image_path from movies")
        movies=cursor.fetchall()
        return movies
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Aποτυχία ανάκτησης ταινιών:{e}")
        return[]
    
    finally:
        cursor.close()
        connection.close()
        
        

def open_movie_details(movie_id):
    try:
        subprocess.Popen(["python","detail-movie.py",str(movie_id)])
    except Exception as e:
        messagebox.showerror("Σφάλμα",f"Αποτυχία ανοίγματος λεπτομερειών ταινίας:{e}")
        
def all_movies():
    movies=fetch_movies()
    if movies:
        for movie_id, title, image_path in movies:
            frame=tk.Frame(movie_list_frame, bg="black",pady=10)
            frame.pack(fill=tk.X)
            
            try:
                if image_path and os.path.exists(image_path):
                    img=Image.open(image_path)
                    img=img.resize((80,120))
                    photo=ImageTk.PhotoImage(img)
                    img_label=tk.Label(frame,image=photo,bg="black")
                    img_label.image=photo
                    img_label.pack(side=tk.LEFT,padx=10)
                else:
                    tk.Label(frame,text="[Χωρίς εικόνα]",font=("Arial",10,"italic"),
                             fg="white",bg="black").pack(side=tk.LEFT,padx=10)
            except Exception as e:
                tk.Label(frame,text="[Χωρίς εικόνα]",font=("Arial",10,"italic"),
                             fg="white",bg="black").pack(side=tk.LEFT,padx=10)
                
            title_label=tk.Label(frame,text=title,font=("Arial",12,"bold"),
                                     fg="white",bg="black")
            title_label.pack(anchor="w")
            details_button=tk.Button(frame,text="Προβολή λεπτομερειών",
                                         command=lambda m_id=movie_id:open_movie_details(m_id),
                                         bg="#e50914",
                                         fg="white",
                                         font=("Arial",10),
                                         width=20
                                         )
            details_button.pack(anchor="w",pady=5)

root=tk.Tk()
root.title("Λίστα Ταινιών")
root.configure(bg="black")
root.geometry("600x700")

tk.Label(root,text="Διαθέσιμες Ταινίες",font=("Arial",16,"bold"),fg="white",bg="black").pack(pady=10)

movie_list_frame=tk.Frame(root,bg="black")
movie_list_frame.pack(fill=tk.BOTH,expand=True)
all_movies()
root.mainloop()
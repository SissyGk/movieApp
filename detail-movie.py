import tkinter as tk
from tkinter import messagebox
from connection import create_connection
import sys
import os
from PIL import Image,ImageTk


def fetch_movie_details(movie_id):
    connection=create_connection()
    if not connection:
        messagebox.showerror("Σφάλμα","Αποτυχία σύνδεσης στη βάση δεδομένων.")
        return None
    try:
        cursor=connection.cursor()
        cursor.execute("""Select title,release_year,genre,director,
                       duration_minutes,rating,image_path from movies
                       where id=%s""",(movie_id,))
        return cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Σφάλμα",f"Αποτυχία ανάκτησης λεπτομερειών ταινίας:{e}")
        return None
    finally:
        cursor.close()
        connection.close()
        

if len(sys.argv) <2:
    messagebox.showerror("Σφάλμα","Δεν δόθηκε ID ταινίας.")
    sys.exit()
    
movie_id=sys.argv[1]

movie_details=fetch_movie_details(movie_id)
if not movie_details:
    sys.exit()
    
title,release_year,genre,director,duration,rating,image_path=movie_details

root=tk.Tk()
root.title(f"Λεπτομέρειες Ταινίας: {title}")
root.configure(bg="black")
root.geometry("500x700")

tk.Label(root,text=title,font=("Arial",20,"bold"),fg="white",bg="black").pack(pady=10)

details_text=(
    f"Έτος Κυκλοφορίας: {release_year}\n"
    f"Είδος: {genre}\n"
    f"Σκηνοθέτης: {director}\n"
    f"Διάρκεια: {duration}\n"
    f"Βαθμολογία: {rating}"
)

tk.Label(root,text=details_text,font=("Arial",14),fg="white",bg="black",justify="left").pack(pady=10)

if image_path and os.path.exists(image_path):
    try:
        img=Image.open(image_path)
        img=img.resize((300,450))
        photo=ImageTk.PhotoImage(img)
        img_label=tk.Label(root,image=photo,bg="black")
        img_label.image=photo
        img_label.pack(pady=20)
    except Exception as e:
        tk.Label(root,text="[Η εικόνα δεν είναι διαθέσιμη]",font=("Arial",10,"italic"),
                 fg="white",bg="black").pack(pady=20)
    tk.Label(root,text="[Η εικόνα δεν είναι διαθέσιμη]",font=("Arial",10,"italic"),
             fg="white",bg="black").pack(pady=20)
    
tk.Button(root,text="Επιστροφή",command=root.destroy,bg="#e50914",fg="white",font=("Arial",12,"bold")).pack(pady=10)

root.mainloop()
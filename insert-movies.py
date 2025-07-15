import tkinter as tk
from tkinter import messagebox, filedialog
from connection import create_connection
import os
import shutil

SESSION_FILE="session.txt"
MOVIES_FOLDER="movies" 

def get_logged_in_user():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE,"r") as file:
            data=file.read().strip().split(",")
            if len(data)==2:
                return data[0],data[1] #username,role
    return None,None

def select_image():
    filepath=filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg;*.jpeg;*.gif")])
    if filepath:
        entry_image_path.delete(0,tk.END)
        entry_image_path.insert(0,filepath)

def insert_movie():
    title=entry_title.get().strip()
    release_year=entry_release_year.get().strip()
    genre=entry_genre.get().strip()
    director=entry_director.get().strip()
    duration=entry_duration.get().strip()
    rating=entry_rating.get().strip()
    image_path=entry_image_path.get().strip()
    
    if not title or not release_year:
        messagebox.showerror("Σφάλμα","Τα πεδία 'Τίτλος' και 'Έτος κυκλοφορίας' είναι υποχρεωτικά.")
        return
    
    try:
        release_year=int(release_year)
        if duration:
            duration=int(duration)
        if rating:
            rating=float(rating)
    except ValueError:
        messagebox.showerror("Σφάλμα","Τα πεδία 'Έτος κυκλοφορίας', 'Διάρκεια' και 'Βαθμολογία' πρέπει να είναι αριθμητικά!")
        return
    
    
    movie_folder=os.path.join(MOVIES_FOLDER,title)
    if not os.path.exists(movie_folder):
        os.makedirs(movie_folder)
        new_image_path=os.path.join(movie_folder,os.path.basename(image_path))
    
    try:
        shutil.copy(image_path,new_image_path)
    except Exception as e:
        messagebox.showerror("Σφάλμα",F"Αποτυχία μετακίνησης εικόνας:{e}")
        return
    
    
    connection=create_connection()
    if not connection:
        messagebox.showerror("Σφάλμα","Αποτυχία σύνδεσης στη βάση δεδομένων")
        return
    
    try:
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO movies(title,release_year,genre,director,duration_minutes,rating,image_path) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                       (title,release_year,genre,director,duration,rating,new_image_path))
        connection.commit()
        messagebox.showinfo("Επιτυχία","Η ταινία προστέθηκε με επιτυχία!")
        
        entry_title.delete(0,tk.END)
        entry_release_year.delete(0,tk.END)
        entry_genre.delete(0,tk.END)
        entry_director.delete(0,tk.END)
        entry_duration.delete(0,tk.END)
        entry_rating.delete(0,tk.END)
        entry_image_path.delete(0,tk.END)
    except Exception as e:
        messagebox.showerror("Σφάλμα",f"Αποτυχία εισαγωγής: {e}")
    finally:
        cursor.close()
        connection.close()
        
username,role=get_logged_in_user()

if role!='admin':
    messagebox.showerror("Πρόσβαση απορρίφθηκε","Μόνο οι διαχειριστές μπορούν να έχουν πρόσβαση σε αυτή τη σελίδα.")
    exit()


  
root=tk.Tk()
root.title("Προσθήκη Ταινίας")    
root.configure(bg="black")
    

tk.Label(root,text="Τίτλος:",fg="white",bg="black").grid(row=0,column=0,padx=10,pady=5,sticky="e")
entry_title=tk.Entry(root,width=40)
entry_title.grid(row=0,column=1,padx=10,pady=5)

tk.Label(root,text="Έτος Κυκλοφορίας:",fg="white",bg="black").grid(row=1,column=0,padx=10,pady=5,sticky="e")
entry_release_year=tk.Entry(root,width=40)
entry_release_year.grid(row=1,column=1,padx=10,pady=5)

tk.Label(root,text="Είδος:",fg="white",bg="black").grid(row=2,column=0,padx=10,pady=5,sticky="e")
entry_genre=tk.Entry(root,width=40)
entry_genre.grid(row=2,column=1,padx=10,pady=5)

tk.Label(root,text="Σκηνοθέτης:",fg="white",bg="black").grid(row=3,column=0,padx=10,pady=5,sticky="e")
entry_director=tk.Entry(root,width=40) 
entry_director.grid(row=3,column=1,padx=10,pady=5)

tk.Label(root,text="Διάρκεια (λεπτά):",fg="white",bg="black").grid(row=4,column=0,padx=10,pady=5,sticky="e")
entry_duration=tk.Entry(root,width=40)
entry_duration.grid(row=4,column=1,padx=10,pady=5)

tk.Label(root,text="Βαθμολογία:",fg="white",bg="black").grid(row=5,column=0,padx=10,pady=5,sticky="e")
entry_rating=tk.Entry(root,width=40)
entry_rating.grid(row=5,column=1,padx=10,pady=5)

tk.Label(root,text="Μονοπάτι Εικόνας:",fg="white",bg="black").grid(row=6,column=0,padx=10,pady=5,sticky="e")
entry_image_path=tk.Entry(root,width=40)
entry_image_path.grid(row=6,column=1,padx=10,pady=5)

tk.Button(root,text="Επιλογή Εικόνας",command=select_image,bg="#e50914",fg="white",font=("Arial",12,"bold"),width=20).grid(row=7,column=0,columnspan=2,pady=5)
tk.Button(root,text="Προσθήκη",command=insert_movie,bg="#e50914",fg="white",font=("Arial",12,"bold"),width=20).grid(row=8,column=0,columnspan=2,pady=20)
    

root.mainloop()
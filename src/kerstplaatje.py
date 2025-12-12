import tkinter as tk
from PIL import Image, ImageTk

bestand = r"C:\Users\iw00\Pictures\figuur76.png"

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

img = Image.open(bestand)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Nieuw: gebruik Resampling.LANCZOS
img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo, bg="black")
label.pack(expand=True)

# Sluit op ENTER
root.bind("<Return>", lambda e: root.destroy())
root.mainloop()

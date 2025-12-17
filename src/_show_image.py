import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


class ImageOverlay:
    def __init__(self):
        self.root = None
        self.photo = None  # Bewaar referentie om garbage collection te voorkomen
    
    def open(self, bestand: Path):
        if self.root is not None:
            self.close()
        
        self.root = tk.Tk()
        
        # Verwijder window decorations en maak transparant voor focus
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Krijg schermafmetingen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Bereken afmetingen voor onderste helft
        window_height = screen_height // 2
        y_position = 0 #screen_height // 2
        
        # Positioneer het venster
        self.root.geometry(f"{screen_width}x{window_height}+0+{y_position}")
        self.root.configure(bg="black")
        
        # Maak het venster click-through (geen focus bij klikken)
        self.root.wm_attributes("-transparentcolor", "")
        
        # Bind ENTER om te sluiten
        self.root.bind("<Return>", lambda e: self.close())
        
        # Open en resize de afbeelding
        img = Image.open(bestand)
        img = img.resize((screen_width, window_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        
        # Toon de afbeelding
        label = tk.Label(self.root, image=self.photo, bg="black")
        label.pack(expand=True, fill=tk.BOTH)
        
        # Start de mainloop in een aparte thread of gebruik update
        self.root.update()
    
    def close(self):
        if self.root is not None:
            self.root.destroy()
            self.root = None
            self.photo = None
    
    def is_open(self):
        return self.root is not None and self.root.winfo_exists()
    
    def update(self):
        if self.is_open():
            self.root.update() #type: ignore

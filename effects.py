#!/usr/bin/env python3
import csv
import os
import random
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk

BESTAND = "vragen.csv"
AFBEELDING = r"C:\Users\iw00\Pictures\CARGILL.jpg"  # voorbeeldplaatje

# ------------------ ASCII-KERSTBOOM + SNEEUW ------------------
def print_kerstboom():
    kerstboom = """
        \033[33m*\033[0m
       \033[32m***\033[0m
      \033[32m*****\033[0m
     \033[32m*******\033[0m
    \033[32m*********\033[0m
       \033[33m|||\033[0m
    """
    print(kerstboom)
    print("\033[31mWelkom bij de kerstquiz!\033[0m\n")

def sneeuw_lijn(breedte=50):
    return "".join(random.choice([" ", "\u2744"]) for _ in range(breedte))

def print_sneeuw(lijnen=5, breedte=50):
    for _ in range(lijnen):
        print(sneeuw_lijn(breedte))

# ------------------ VRAAG-CSV LOGICA ------------------
def lees_vragen():
    vragen = []
    with open(BESTAND, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if not row["gedaan"].strip():
                vragen.append(row)
    return vragen

def schrijf_afgevinkt(vraagregel):
    with open(BESTAND, newline='', encoding='utf-8') as f:
        oude_regels = list(csv.DictReader(f, delimiter=';'))
    for r in oude_regels:
        if r["vraag"] == vraagregel["vraag"]:
            r["gedaan"] = "x"
    with open(BESTAND, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["categorie","vraag","antwoord","gedaan"], delimiter=';')
        writer.writeheader()
        writer.writerows(oude_regels)

# ------------------ PLAATJE FULLSCREEN (Tkinter) ------------------
def toon_afbeelding(bestand):
    if not os.path.exists(bestand):
        return
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    img = Image.open(bestand)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    img = img.resize((w,h), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=photo, bg="black")
    label.pack(expand=True)
    root.bind("<Return>", lambda e: root.destroy())
    root.mainloop()

# ------------------ HOOFDFUNCTIE ------------------
def main():
    vragenlijst = lees_vragen()
    if not vragenlijst:
        print("Er zijn geen openstaande vragen meer.")
        return

    for vraag in vragenlijst:
        # scherm schoonmaken
        os.system("cls")  # Windows
        print_kerstboom()
        print_sneeuw(10, 50)

        # toon vraag
        print(vraag["vraag"])
        input("\n")

        print("\nAntwoord:")
        print(vraag["antwoord"])

        # wacht op een getal om door te gaan
        while True:
            invoer = input("\nVoer een getal in om verder te gaan: ").strip()
            if invoer.isdigit():
                break
            print("Ongeldige invoer, alleen een getal is toegestaan.")

        # markeer vraag als gedaan
        schrijf_afgevinkt(vraag)

    os.system("cls")
    print_kerstboom()
    print("\033[32mAlle openstaande vragen zijn behandeld! Fijne Kerst!\033[0m")

if __name__ == "__main__":
    if not os.path.exists(BESTAND):
        print("CSV-bestand ontbreekt.")
    else:
        main()

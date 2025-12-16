import csv
import os

from dataclasses import dataclass
from pathlib import Path
from terminal_effects import print_kerstboom, print_sneeuw
from play_audio import start_audio, stop_audio

# import winsound
# import time
# import threading

_stop_flag = False
VRAGENLIJST_BESTAND = Path("vragen.csv")

@dataclass
class vraag():
    categorie: str
    vraag: str
    bestand: Path
    antwoord: str
    gedaan: str

def lees_vragen(vragenlijst_bestand: Path) -> list:
    vragen = []
    
    with vragenlijst_bestand.open(newline='', encoding='utf-8') as f:
        bestand = csv.DictReader(f, delimiter=';')
        
        for row in bestand:
            if not row["gedaan"].strip():
                vragen.append(vraag(
                    categorie=row["categorie"],
                    vraag=row["vraag"],
                    bestand=Path(row["bijlage"]),
                    antwoord=row["antwoord"],
                    gedaan=row["gedaan"]
                ))
    
    return vragen

def kerstbingo(vragenlijst: list) -> None:
    global _stop_flag
    try:
        if not vragenlijst:
            print("Er zijn geen openstaande vragen meer.")
            return

        while any(not v.gedaan for v in vragenlijst):

            invoer = ""
            thread = None

            # Welkom bericht, altijd weergeven
            print_kerstboom()
            print_sneeuw()
            print("\033[1m\033[31mWelkom bij deel 2 van de TAI-NW Kerstbingo! \033[0m \033[0m \n")

            while True:
                invoer = input("Voer een categorie in: ").strip()
            
                if invoer.strip().lower() == "exit":
                    os.system("cls")  
                    print("Programma afgesloten.")
                    exit(0)

                if invoer.isdigit():
                    if invoer in ["1", "2", "3", "4"]:
                        break
                    else:
                        print("Ongeldige invoer, alleen een getal gelijk aan of lager dan 4 is toegestaan.")
                else:
                    print("Ongeldige invoer, alleen een getal is toegestaan.")
            
            # Vind openstaande vraag
            open_vragen = [v for v in vragenlijst if not v.gedaan and v.categorie == invoer]

            # Open vraag gevonden
            if open_vragen:
                huidige_vraag = open_vragen[0]
                huidige_vraag.gedaan = "x"
                
                # Check bestand: audio
                if huidige_vraag.bestand.exists() & (huidige_vraag.bestand.suffix.lower() == ".wav"):
                    thread = start_audio(huidige_vraag.bestand)
                    print(f'Muziekvraag: \033[1m{huidige_vraag.vraag}\033[0m')

                # Check bestand: afbeelding
                elif huidige_vraag.bestand.exists() & (huidige_vraag.bestand.suffix.lower() in (".jpg",".png")):
                    print(f'Afbeelding: \033[1m{huidige_vraag.vraag}\033[0m')

                # Geen bestand, enkel een vraag
                else:
                    print(f'Vraag: \033[1m{huidige_vraag.vraag}\033[0m')
                
                input("ENTER voor het antwoord...")

                if thread:
                    stop_audio(thread)
                    
                print(f'Antwoord: \033[1m{huidige_vraag.antwoord}\033[0m')
                input("")
                os.system("cls")

            # Geen open vraag gevonden
            else:
                print(f'Er zijn geen openstaande vragen meer in categorie {invoer}.')
                input("")
                os.system("cls")

        print("\nAlle openstaande vragen zijn behandeld.")
        input("")
        os.system("cls")

    except KeyboardInterrupt:
        os.system("cls")  
        print("\nProgramma afgesloten met Ctrl-C.")

if __name__ == "__main__":
    if not VRAGENLIJST_BESTAND.exists():
        print("CSV-bestand ontbreekt.")
    else:
        os.system("cls")  
        kerstbingo(vragenlijst=lees_vragen(VRAGENLIJST_BESTAND))

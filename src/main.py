import csv
import os
import winsound
import time
import threading
from dataclasses import dataclass
from pathlib import Path

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
    try:
        if not vragenlijst:
            print("Er zijn geen openstaande vragen meer.")
            return

        while any(not v.gedaan for v in vragenlijst):

            invoer = ""
            os.system("cls")  # Wis het scherm voordat je een nieuwe vraag toont

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
                        os.system("cls")  
                        print("Ongeldige invoer, alleen een getal gelijk aan of lager dan 4 is toegestaan.")
                else:
                    os.system("cls")  
                    print("Ongeldige invoer, alleen een getal is toegestaan.")

            open_vragen = [v for v in vragenlijst if not v.gedaan and v.categorie == invoer]

            if not open_vragen:
                break

            huidige_vraag = open_vragen[0]
            huidige_vraag.gedaan = "x"

            os.system("cls")
            print(f'Vraag: {huidige_vraag.vraag}')
            input("")
            
    #             AUDIOBESTAND = "test.wav"
    #             global _stop_flag

    #             if not os.path.exists(AUDIOBESTAND):
    #                 print("WAV-bestand ontbreekt.")
    #                 return

    #             thread = start_audio(AUDIOBESTAND)

    #             input("Van welke artiest is dit nummer?")

    #             print(f'Antwoord: {vraag["antwoord"]}')
    #             stop_audio(thread)
    #             input("")

    #         if invoer == "2":
    #             print(f'Vraag {vraag["categorie"]}: {vraag["vraag"]}')
    #             input("")
    #             print(f'Antwoord: {vraag["antwoord"]}')
    #             input("")

    #         schrijf_afgevinkt(vraag)
    
        print("\nAlle openstaande vragen zijn behandeld.")

    except KeyboardInterrupt:
        os.system("cls")  
        print("\nProgramma afgesloten met Ctrl-C.")

if __name__ == "__main__":
    if not VRAGENLIJST_BESTAND.exists():
        print("CSV-bestand ontbreekt.")
    else:
        kerstbingo(vragenlijst=lees_vragen(VRAGENLIJST_BESTAND))

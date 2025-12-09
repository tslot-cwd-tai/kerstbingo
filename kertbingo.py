import csv
import os
import winsound
import time
import threading

_stop_flag = False
BESTAND = "vragen.csv"

def audio_afspelen(AUDIOBESTAND):
    global _stop_flag
    winsound.PlaySound(AUDIOBESTAND, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
    while not _stop_flag:
        time.sleep(0.1)
    # Stop audio expliciet
    winsound.PlaySound(None, winsound.SND_FILENAME)

def start_audio(AUDIOBESTAND):
    global _stop_flag
    _stop_flag = False
    thread = threading.Thread(target=audio_afspelen, args=(AUDIOBESTAND,), daemon=True)
    thread.start()
    return thread

def stop_audio(thread):
    global _stop_flag
    _stop_flag = True
    thread.join()  # wacht tot thread klaar is

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
        writer = csv.DictWriter(f, fieldnames=["categorie", "vraag", "antwoord", "gedaan"], delimiter=';')
        writer.writeheader()
        writer.writerows(oude_regels)


def main():
    vragenlijst = lees_vragen()
    try:
        if not vragenlijst:
            print("Er zijn geen openstaande vragen meer.")
            return

        for vraag in vragenlijst:
            
            invoer = ""
            os.system("cls")  # Wis het scherm voordat je een nieuwe vraag toont

            while True:
                invoer = input("Voer een getal in (bijv. 1 om verder te gaan): ").strip()
            
                if invoer.strip().lower() == "exit":
                    print("Programma afgesloten.")
                    exit(0)

                if invoer.isdigit():
                    break
                else:
                    print("Ongeldige invoer, alleen een getal is toegestaan.")

            if invoer == "1":
                AUDIOBESTAND = "test.wav"
                global _stop_flag

                if not os.path.exists(AUDIOBESTAND):
                    print("WAV-bestand ontbreekt.")
                    return

                # thread = threading.Thread(target=audio_afspelen, args=(AUDIOBESTAND,), daemon=True)
                thread = start_audio(AUDIOBESTAND)
                # thread.start()

                input("Van welke artiest is dit nummer?")

                # _stop_flag = True
                # time.sleep(0.2)
                
                print(f'Antwoord: {vraag["antwoord"]}')
                stop_audio(thread)
                input("")

            if invoer == "2":
                print(f'Vraag {vraag["categorie"]}: {vraag["vraag"]}')
                input("")
                print(f'Antwoord: {vraag["antwoord"]}')
                input("")

            schrijf_afgevinkt(vraag)
    
        print("\nAlle openstaande vragen zijn behandeld.")

    except KeyboardInterrupt:
        print("\nProgramma afgesloten met Ctrl-C.")

if __name__ == "__main__":
    if not os.path.exists(BESTAND):
        print("CSV-bestand ontbreekt.")
    else:
        main()

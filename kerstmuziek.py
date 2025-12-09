#!/usr/bin/env python3
import winsound
import time
import os
import threading

AUDIOBESTAND = "test.wav"
_stop_flag = False


def audio_afspelen():
    global _stop_flag
    winsound.PlaySound(AUDIOBESTAND, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
    while not _stop_flag:
        time.sleep(0.1)
    winsound.PlaySound(None, winsound.SND_FILENAME)

def main():
    global _stop_flag

    if not os.path.exists(AUDIOBESTAND):
        print("WAV-bestand ontbreekt.")
        return

    print("Start audio...")

    thread = threading.Thread(target=audio_afspelen, daemon=True)
    thread.start()

    input("ENTER stopt audio...")

    _stop_flag = True
    time.sleep(0.2)
    print("Audio gestopt.")


if __name__ == "__main__":
    main()

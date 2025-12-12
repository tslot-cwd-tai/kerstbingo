import winsound
import time
import threading
from pathlib import Path

def audio_afspelen(AUDIOBESTAND: Path) -> None:
    global _stop_flag
    winsound.PlaySound(AUDIOBESTAND.name, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
    while not _stop_flag:
        time.sleep(0.1)
    # Stop audio expliciet
    winsound.PlaySound(None, winsound.SND_FILENAME)

def start_audio(AUDIOBESTAND: Path) -> threading.Thread:
    global _stop_flag
    _stop_flag = False
    thread = threading.Thread(target=audio_afspelen, args=(AUDIOBESTAND,), daemon=True)
    thread.start()
    
    return thread

def stop_audio(thread) -> None:
    global _stop_flag
    _stop_flag = True
    thread.join() 
import shutil
import os
import time
import sys

OS_USERNAME = os.getlogin()
KOBO_PATH = f"/run/media/{OS_USERNAME}/KOBOeReader/.kobo/KoboReader.sqlite"
LOCAL_COPY_PATH = "tmp/KoboReader.sqlite"

KOBO_UNOFFICIAL_ANNOTATIONS = "/run/media/{OS_USERNAME}/KOBOeReader/Digital Editions/Annotations"

COMPATIBLE_WITH = ("Kobo") # TODO: Kindle

def wait_for_device():
    while True:
        if not device_available():
            chars = ['|', '/', '-', '\\']  # Los caracteres que se usarán para el efecto de carga
            for _ in range(5):  # El número de ciclos de carga
                for char in chars:
                    sys.stdout.write(f'\r[] Escaneando {char}')  # \r vuelve al inicio de la línea
                    sys.stdout.flush()  # Asegura que el texto se imprima de inmediato
                    time.sleep(0.1) 
        else:
            print(f"\nDevice detected: {'device_name'}")
            break

# TODO: Add more check. Posix, /media, /Volumes.
def device_available():
    """Check if Kobo is connected"""
    if os.path.exists(KOBO_PATH):
        return True
    else:
        return False
        


def copy_db_file():
    if device_available():
        try:
            shutil.copy(KOBO_PATH, LOCAL_COPY_PATH)
            print(f"[x] File copied to {LOCAL_COPY_PATH}.")
            return True
        except Exception as e:
            print(f"Error while copying file: {e}")
            return False
   
def clear_tmp():
    os.remove(LOCAL_COPY_PATH)


import shutil
import os

OS_USERNAME = os.getlogin()
KOBO_PATH = f"/run/media/{OS_USERNAME}/KOBOeReader/.kobo/KoboReader.sqlite"
LOCAL_COPY_PATH = "tmp/KoboReader.sqlite"


# TODO: Add more check. Posix, /media, /Volumes.
def device_available():
    """Check if Kobo is connected"""
    if os.path.exists(KOBO_PATH):
        return True
    else:
        print("Device not found.") 
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


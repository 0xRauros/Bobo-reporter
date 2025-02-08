import shutil
import os
import time
import sys
import win32api

OS_USERNAME = os.getlogin()
KOBO_PATH = f"/run/media/{OS_USERNAME}/KOBOeReader/.kobo/KoboReader.sqlite"
LOCAL_COPY_PATH = "tmp/KoboReader.sqlite"

KOBO_UNOFFICIAL_ANNOTATIONS = "/run/media/{OS_USERNAME}/KOBOeReader/Digital Editions/Annotations"

COMPATIBLE_WITH = ("Kobo") # TODO: Kindle

def wait_for_device():
    """Continuously check for Kobo and Kindle, alternating between them, until one is found."""
    
    chars = ['|', '/', '-', '\\']  # Loading animation characters
    print("[] Escaneando...", end='', flush=True)

    while True:
        for char in chars:
            sys.stdout.write(f'\r[] Escaneando {char}')  # Overwrites line with animation
            sys.stdout.flush()
            time.sleep(0.1)

            # Alternate checking Kobo and Kindle
            device = device_available()
            if device:
                print(f"\nDevice detected: {device}")
                return device
            
            # Check for Kindle
            result = find_kindle_documents_path()
            if result:
                device, path = result  # Extract "Kindle" and path
                print(f"\nDevice detected: {device} at {path}")
                return device, path  # Returns ("Kindle", clippings_path)

# TODO: Add more check. Posix, /media, /Volumes.
def device_available():
    """Check if Kobo is connected"""
    if os.path.exists(KOBO_PATH):
        return "Kobo"
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

def find_kindle_documents_path():
    # Retrieve all drive letters
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # Split the string and remove the last empty element

    for drive in drives:
        try:
            # Get the volume information of the drive
            volume_info = win32api.GetVolumeInformation(drive)
            volume_name = volume_info[0]
            if volume_name == "Kindle":
                documents_path = os.path.join(drive, "documents")
                if os.path.exists(documents_path):
                    print(f"Kindle 'documents' folder found at: {documents_path}")
                    clippings_path = os.path.join(documents_path,"My Clippings.txt")
                    return "Kindle", clippings_path
                else:
                    print(f"'documents' folder not found on Kindle drive: {drive}")
                    return None
        except win32api.error:
            # Skip drives that cannot be accessed
            continue

    print("No Kindle device found.")
    return None
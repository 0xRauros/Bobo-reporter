import os


def winapi_loader():
    try:
        import win32api
    except:
        print("[TODO]: Remove platform specific dependencies.")


def find_kindle_documents_path():

    winapi_loader()

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
                    return clippings_path
                else:
                    print(f"'documents' folder not found on Kindle drive: {drive}")
                    return None
        except win32api.error:
            # Skip drives that cannot be accessed
            continue

    print("No Kindle device found.")
    return None


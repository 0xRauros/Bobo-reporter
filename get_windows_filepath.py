import os

try:
    import win32api
except ImportError:
    win32api = None


def winapi_loader():
    global win32api
    if win32api is None:
        try:
            import win32api
        except ImportError:
            raise ImportError("pywin32 is required for Windows Kindle support. Install it with: pip install pywin32")


def find_kindle_documents_path():
    winapi_loader()
    
    if win32api is None:
        raise ImportError("pywin32 is required for Windows Kindle support")

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


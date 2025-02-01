import os
from bobo_reader import copy_db_file, clear_tmp, wait_for_device
from bobo_db import get_official_bookmarks
from reports import generate_report_pdf, generate_report_html
from clippings_parser import parse_clippings
import platform
from kindle_reports import kindle_report

# Retrieve the name of the operating system


def print_logo():
    os_name = platform.system()
    logo = """
______       _                                       _            
| ___ \     | |                                     | |           
| |_/ / ___ | |__   ___    _ __ ___ _ __   ___  _ __| |_ ___ _ __ 
| ___ \/ _ \| '_ \ / _ \  | '__/ _ | '_ \ / _ \| '__| __/ _ | '__|
| |_/ | (_) | |_) | (_) | | | |  __| |_) | (_) | |  | ||  __| |   
\____/ \___/|_.__/ \___/  |_|  \___| .__/ \___/|_|   \__\___|_|   
                                   | |                            
                                   |_|                            
    
    Making access to your eReader highlights easy and pretty ;)
    by 0xRauros
    """
    print(logo)
    print(f"You are using: {os_name}")

def set_up_env():
    copy_db_file()
    # check connection
    # bla bla bla TODO


def main():
    

# Inform the user about the operating system
    print_logo()

    device = wait_for_device()

    if device == "Kobo":
        print("Kobo detected! Proceeding with Kobo-specific actions...")
        set_up_env()
        #generate_report_pdf(get_official_bookmarks(), "bookmark_reports.pdf")
        generate_report_html(get_official_bookmarks())

        clear_tmp()
        # Call Kobo-related function here

    elif isinstance(device, tuple) and device[0] == "Kindle":
        _, clippings_path = device
        print(f"Kindle detected! Clippings path: {clippings_path}")
        df = parse_clippings(clippings_path)
        kindle_report(df)



if __name__ == "__main__":
    main()

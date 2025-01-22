import os
from bobo_reader import copy_db_file, clear_tmp, wait_for_device
from bobo_db import get_official_bookmarks
from reports import generate_report_pdf, generate_report_html

from clippings_parser import parse_clippings
from get_windows_filepath import find_kindle_documents_path
from kindle_reports import kindle_report


def print_logo():
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

def set_up_env():
    copy_db_file()
    # check connection
    # bla bla bla TODO


def main():
    print_logo()

    device_type = input("Please enter your eBook device (Kobo/Kindle): ").strip().lower()

    if device_type == "kobo":
        wait_for_device()
        set_up_env()
        #generate_report_pdf(get_official_bookmarks(), "bookmark_reports.pdf")
        generate_report_html(get_official_bookmarks())
        clear_tmp()

    elif device_type == "kindle":
        print("You have selected Kindle. Proceeding with parsing clippings.")
        filepath=find_kindle_documents_path()
        print(filepath)
        df = parse_clippings(filepath)
        kindle_report(df)
    
    else:
        print("Sorry, we only support Kobo Clara and Kindle ?")


if __name__ == "__main__":
    main()

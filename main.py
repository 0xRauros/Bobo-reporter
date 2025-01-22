import os
from bobo_reader import copy_db_file, clear_tmp
from bobo_db import get_official_bookmarks
from reports import generate_report_pdf, generate_report_html
from clippings_parser import parse_clippings
import platform
from get_windows_filepath import find_kindle_documents_path
from kindle_reports import kindle_report

# Retrieve the name of the operating system


def print_logo():
    os_name = platform.system()
    logo = """

    BOBO reporter  
    
    Making Kobo bookmark acess easy and smooth ;)
    
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
    
    device_type = input("Please enter your eBook device (Kobo/Kindle): ").strip().lower()

    if device_type == 'kobo':
        print("You have selected Kobo. Proceeding with copying the database file.")
        set_up_env()
        #generate_report_pdf(get_official_bookmarks(), "bookmark_reports.pdf")
        generate_report_html(get_official_bookmarks())
        clear_tmp()
    elif device_type == 'kindle':
        print("You have selected Kindle. Proceeding with parsing clippings.")
        filepath=find_kindle_documents_path()
        print(filepath)
        df = parse_clippings(filepath)
        kindle_report(df)

    else:
        print("Invalid input. Please enter 'Kobo' or 'Kindle'.")
    

if __name__ == "__main__":
    main()

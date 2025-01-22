import os
from bobo_reader import copy_db_file, clear_tmp, wait_for_device
from bobo_db import get_official_bookmarks
from reports import generate_report_pdf, generate_report_html


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

    wait_for_device()

    set_up_env()

    #generate_report_pdf(get_official_bookmarks(), "bookmark_reports.pdf")
    generate_report_html(get_official_bookmarks())

    clear_tmp()

if __name__ == "__main__":
    main()

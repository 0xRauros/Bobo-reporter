import os
from bobo_reader import copy_db_file, clear_tmp
from bobo_db import get_official_bookmarks
from reports import generate_report_pdf, generate_report_html


def print_logo():
    logo = """

    BOBO reporter  
    
    Making Kobo bookmark acess easy and smooth ;)
    
    by 0xRauros
    """
    print(logo)

def set_up_env():
    copy_db_file()
    # check connection
    # bla bla bla TODO


def main():
    print_logo()

    set_up_env()

    #generate_report_pdf(get_official_bookmarks(), "bookmark_reports.pdf")
    generate_report_html(get_official_bookmarks())

    clear_tmp()

if __name__ == "__main__":
    main()

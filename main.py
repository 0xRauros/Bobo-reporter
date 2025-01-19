import os
from bobo_reader import copy_db_file, clear_tmp
from bobo_db import get_paid_bookmarks
from reports import generate_bookmarks_output_pdf


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

    generate_bookmarks_output_pdf(get_paid_bookmarks(), "bookmark_reports.pdf")

    clear_tmp()

if __name__ == "__main__":
    main()

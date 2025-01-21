import sqlite3
from contextlib import closing
from bobo_reader import LOCAL_COPY_PATH


bookmarks_query = """
    SELECT DISTINCT Content.BookTitle as BookTitle, Bookmark.Text as BookmarkText, Bookmark.ContentID as ContentID
    FROM Content
    JOIN Bookmark ON SUBSTR(Content.ContentID, 1, INSTR(Content.ContentID, '!OEBPS!') - 1) = SUBSTR(Bookmark.ContentID, 1, INSTR(Bookmark.ContentID, '!OEBPS!') - 1)
    WHERE Bookmark.Text IS NOT NULL AND Bookmark.Text != '';
    """

def open_connection(db_path=LOCAL_COPY_PATH):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the db: {e}")
        raise


def get_official_bookmarks():
    """The ones stored inside sqlite db"""
    with closing(open_connection()) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(bookmarks_query)
            bookmarks = cursor.fetchall()
            return bookmarks
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                print(f"Error. Did you remember to press the 'Connect' option of the pop up when you plug your Kobo to the computer?")


def get_unofficial_bookmarks():
    """Other bookmarks from non-purchased books"""
    pass


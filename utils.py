from models import Book
from collections import defaultdict

def query_result_to_book_list(query_result):
    books = defaultdict(Book)
    for title, bookmark, content_id in query_result:
        if title not in books:
            books[title] = Book(title)
        books[title].add_bookmark(bookmark)
    return books
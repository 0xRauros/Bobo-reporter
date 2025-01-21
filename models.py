class Book:
    def __init__(self, title):
        self.title = title
        self.bookmarks = []

    def add_bookmark(self, bookmark):
        self.bookmarks.append(bookmark)

    def __repr__(self):
        return f"Book(title={self.title},\nbookmarks={self.bookmarks})"

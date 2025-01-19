import subprocess
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas



def generate_output_html(bookmarks, html_filename="bookmarks.html", theme=None):
    pass


def split_pdf_text(text, max_length=80):
    lines = []
    while len(text) > max_length:
        split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:  
            split_point = max_length
        lines.append(text[:split_point])
        text = text[split_point:].lstrip() 
    lines.append(text) 
    return lines


def generate_bookmarks_output_pdf(bookmarks, pdf_filename="bookmarks.pdf", theme=None):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    x = 72  
    y = 750  
    c.setFont("Helvetica-Bold", 18)
    
    for BookTitle, BookmarkText, ContentID in bookmarks:
        
        
        c.setFillColorRGB(31/255, 164/255, 171/255)  
        
        current_book_title = BookTitle
        c.drawString(x, y, BookTitle)  
        y -= 40  

        if y < 100:
            c.showPage()  
            y = 750

        c.setFont("Helvetica", 10)  

        c.setFillColorRGB(0, 0, 0)  

        bookmark_lines = split_pdf_text(BookmarkText, max_length=70)

        for line in bookmark_lines:
            c.drawString(x, y, line)
            y -= 12  

        y -= 12  

        if y < 100:
            c.showPage()  
            y = 750

    c.save()  
    subprocess.Popen(["xdg-open", f"{os.getcwd()}/{pdf_filename}"])
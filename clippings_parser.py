import re
import pandas as pd

def parse_clippings(file_path):
    """
    Parses a Kindle clippings file and returns the data as a pandas DataFrame.
    Args:
        file_path (str): The path to the Kindle clippings file.
    Returns:
        pandas.DataFrame: A DataFrame containing the parsed clippings with columns:
            - "Book Title": The title of the book.
            - "Metadata": The metadata associated with the clipping.
            - "Added On": The date and time when the clipping was added.
            - "Text": The content of the clipping.
            - "Category": The category of the clipping (extracted from metadata).
            - "Page": The page number of the clipping (extracted from metadata).
            - "Position": The position of the clipping (extracted from metadata).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Regular expression to capture the clippings
    pattern = r"""^(.*?)\n   # Título del libro
                  -\s(.*?)\s\|\sAñadido\s(el\s.*?)\n  # Metadatos
                  (.*?)\n=+$"""  # Contenido y separador
    
    # Compile the expression to allow comments and spaces
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
    matches = regex.findall(content)

    # Process matches into a structured list
    clippings = []
    for match in matches:
        book_title = match[0].strip()
        metadata = match[1].strip()
        added_on = match[2].strip()
        text = match[3].strip()
        
        clippings.append({
            "Book Title": book_title,
            "Metadata": metadata,
            "Added On": added_on,
            "Text": text
        })

    # Convert the list to a DataFrame
    df = pd.DataFrame(clippings)

    # Extract categories, pages, and positions
    if not df.empty:
        df["Category"] = df["Metadata"].apply(extract_category)
        df["Page"] = df["Metadata"].apply(extract_page)
        df["Position"] = df["Metadata"].apply(extract_position)
    # df.to_csv("kindle_bookmarks.csv")

    return df

def extract_category(metadata):
    """Extracts the category: Note, Bookmark, or Highlight"""
    if "nota" in metadata.lower():
        return "Note"
    elif "marcador" in metadata.lower():
        return "Bookmark"
    elif "subrayado" in metadata.lower():
        return "Highlight"
    return None

def extract_page(metadata):
    """Extracts the page from the metadata if available"""
    match = re.search(r"página (\d+)", metadata, re.IGNORECASE)
    return match.group(1) if match else None

def extract_position(metadata):
    """Extracts the position from the metadata"""
    match = re.search(r"posición ([\d\-]+)", metadata, re.IGNORECASE)
    return match.group(1) if match else None

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

def kindle_report(dataframe):

    df = dataframe

    # Step 1: Extract author and group data by book title
    parsed_data = {}
    for book, group in df.groupby("Book Title"):
        # Extract the author from the Metadata column (first row for the group)
        author = group["Metadata"].iloc[0].replace("Author: ", "")

        # Process notes for the book
        notes = group.apply(
        lambda row: {
            "category": row["Category"].capitalize(),
            "text": row["Text"],
            "page": row["Page"] if pd.notna(row["Page"]) else "N/A",
            "position": row["Position"],
            "added_on": row["Added On"]
        },
            axis=1
        ).tolist()

        parsed_data[book] = {
            "author": author,
            "notes": notes
        }

    # Step 2: Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))  # Use the templates folder

    # Step 3: Load the `default.html` template
    template = env.get_template("kindle_default.html")

    # Step 4: Render the template with parsed data
    html_content = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        books=parsed_data
    )
    filename = datetime.now().strftime("tmp/kindle_report_%Y-%m-%d_%H-%M-%S.html")
    # Step 5: Save the HTML report
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Report has been generated: report.html")
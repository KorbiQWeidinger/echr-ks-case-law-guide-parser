import json
import sqlite3


def find_paragraph(docs: list[dict], paragraph: int):
    def search_paragraph(doc, paragraph):
        if doc["content"].startswith(f"{paragraph}."):
            return doc["content"]
        for e in doc["elements"]:
            res = search_paragraph(e, paragraph)
            if res:
                return res
        return None

    for doc in docs:
        res = search_paragraph(doc, paragraph)
        if res:
            return res
    raise ValueError(f"Paragraph {paragraph} not found.")


def get_citation(
    db_path,
    docname: str,
    paragraph: int,
    year: str = None,
):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    try:
        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # Prepare SQL query to retrieve entries that are similar to the given docname
        query = 'SELECT * FROM "case" WHERE docname LIKE ?'
        fuzzy_docname = f"%{docname}%"
        params = (fuzzy_docname,)

        if year:
            query += " AND judgementdate LIKE ?"
            fuzzy_year = f"%{year}%"
            params = params + (fuzzy_year,)

        # Executing the SQL command
        cursor.execute(query, params)

        columns = [description[0] for description in cursor.description]

        # Fetch all rows from the last executed statement
        results = cursor.fetchall()

        if not results:
            raise ValueError("No results found")

        if len(results) > 1:
            raise ValueError("Multiple entries found for the given docname, year")

        row = results[0]
        for col, val in zip(columns, row):
            if col == "judgment":
                val = json.loads(val)
                paragraph = find_paragraph(val, paragraph)
                return paragraph

        raise ValueError("Paragraph not found.")

    except sqlite3.Error as error:
        raise error
    finally:
        # Closing the connection
        if conn:
            conn.close()


def attempt_to_get_citation(case_name: str, paragraph: int, year: str = None):
    db_path = "data/echr_2_0_0.db"
    docname = "CASE OF " + case_name.upper()
    return get_citation(db_path, docname, paragraph, year)


# Jeronovičs v. Latvia, § 109, 2016
print(attempt_to_get_citation("Jeronovičs v. Latvia", 109, "2016"))

# Georgia v. Russia (II), 2021, §§ 161-175
print(attempt_to_get_citation("Georgia v. Russia (II)", 161, "2021"))

# Ireland v. the United Kingdom, § 154, 18 January 1978
print(attempt_to_get_citation("Ireland v. the United Kingdom", 154, "1978"))

# Ukraine and the Netherlands v. Russia [GC] (dec.), 2022, § 571
# Quick query: SELECT * FROM "case" WHERE docname LIKE "%CASE OF UKRAINE AND THE NETHERLANDS v. RUSSIA%"
# Quick query: SELECT * FROM "case" WHERE judgementdate LIKE "%2023%"
print(
    attempt_to_get_citation("Ukraine and the Netherlands v. Russia", 571, "2022")
)  # Not found

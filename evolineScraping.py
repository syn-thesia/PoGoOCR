import requests
from bs4 import BeautifulSoup
import sqlite3

# Define the URL
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_evolutionary_line_in_Pok%C3%A9mon_GO"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables with class "roundy"
    tables = soup.find_all('table', class_='roundy')

    # List to store extracted data
    data = []

    # Loop through each table
    for table in tables:
        # Find all rows in each table
        rows = table.find_all('tr')

        for row in rows:
            # Find all spans within td > a > span
            span_texts = [span.get_text() for span in row.select('td > a > span')]

            # Only add rows that contain span elements
            if span_texts:
                # If there are fewer than 3 elements, pad with None to maintain structure
                while len(span_texts) < 3:
                    span_texts.append(None)

                # familyline is the same as the basic stage (first element in span_texts)
                familyline = span_texts[0]
                basic = span_texts[0]
                stage2 = span_texts[1] if len(span_texts) > 1 else None
                stage3 = span_texts[2] if len(span_texts) > 2 else None

                # Append the row data as a tuple
                data.append((familyline, basic, stage2, stage3))

    # Connect to the SQLite database
    conn = sqlite3.connect('pokemon.db')
    cursor = conn.cursor()

    # Drop the table if it already exists, then create it with the specified schema
    cursor.execute('DROP TABLE IF EXISTS pokemon_evoline')
    cursor.execute('''
        CREATE TABLE pokemon_evoline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            familyline TEXT,
            basic TEXT,
            stage2 TEXT,
            stage3 TEXT
        )
    ''')

    # Insert each row as a new record in the table
    cursor.executemany('''
        INSERT INTO pokemon_evoline (familyline, basic, stage2, stage3)
        VALUES (?, ?, ?, ?)
    ''', data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data has been saved to the pokemon.db database in the pokemon_evoline table.")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

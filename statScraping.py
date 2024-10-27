from bs4 import BeautifulSoup
import requests
import sqlite3

# Fetch the web page with error handling
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_in_Pok%C3%A9mon_GO"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    data = response.text
except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve data: {e}")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')

# Connect to SQLite database (or create it) with a context manager
with sqlite3.connect('pokemon.db') as conn:
    cursor = conn.cursor()

    # Drop the table if it already exists, then create it with the specified schema
    cursor.execute('DROP TABLE IF EXISTS pokemon_stats')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon_stats (
        pokemon_id INTEGER PRIMARY KEY,
        pokemon_name TEXT,
        stat_attack INTEGER,
        stat_defense INTEGER,
        stat_stamina INTEGER
    )
    ''')

    # Find all rows in the table
    rows = soup.select('tr.c')

    # Prepare a list for bulk inserts
    pokemon_data = []

    # Extract relevant data from each row
    for row in rows:
        try:
            pokemon_id = row.find('td', class_='r').text.strip()
            pokemon_name = row.find('td', class_='l').find('a').text.strip()
            stat_stamina = row.find('td', style='background:#9EE865').text.strip()
            stat_attack = row.find('td', style='background:#F5DE69').text.strip()
            stat_defense = row.find('td', style='background:#F09A65').text.strip()


            # Add data to the list for bulk insert
            pokemon_data.append((pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina))

        except AttributeError:
            # Handle cases where the row is not well-formed
            print(f"Skipping a malformed row: {row}")

    # Bulk insert data into the database
    cursor.executemany('''
        INSERT OR REPLACE INTO pokemon_stats (pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina)
        VALUES (?, ?, ?, ?, ?)
    ''', pokemon_data)

    # Commit the transaction (done automatically by the context manager)
    print("Data has been successfully saved to the pokemon.db database.")

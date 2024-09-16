from bs4 import BeautifulSoup
import requests
import sqlite3

# Fetch the web page
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_in_Pok%C3%A9mon_GO"
response = requests.get(url)
data = response.text

# Parse the HTML content
soup = BeautifulSoup(data, 'html.parser')

# Connect to SQLite database (or create it)
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Create the table PokeBaseStats if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS PokeBaseStats (
    pokemon_id INTEGER PRIMARY KEY,
    pokemon_name TEXT,
    stat_attack INTEGER,
    stat_defense INTEGER,
    stat_stamina INTEGER
)
''')

# Find all rows in the table
rows = soup.find_all('tr', class_='c')

# Extract relevant data
for row in rows:
    pokemon_id = row.find('td', class_='r').text.strip()
    pokemon_name = row.find('td', class_='l').find('a').text.strip()
    stat_stamina = row.find('td', style='background:#9EE865').text.strip()
    stat_attack = row.find('td', style='background:#F5DE69').text.strip()
    stat_defense = row.find('td', style='background:#F09A65').text.strip()

    # Output extracted data
    # print(f"Pokémon Number: {pokemon_id}")
    # print(f"Pokémon Name: {pokemon_name}")
    # print(f"Attack: {stat_attack}")
    # print(f"Defense: {stat_defense}")
    # print(f"HP: {stat_stamina}")

    # Insert the data into the SQLite table
    cursor.execute('''
        INSERT OR REPLACE INTO PokeBaseStats (pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina)
        VALUES (?, ?, ?, ?, ?)
        ''', (pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data has been successfully saved to the pokemon.db database.")
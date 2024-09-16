import sqlite3

# Create a new SQLite database and establish a connection
db_path = "pokemon.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the pokemon_stats table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pokemon_stats (
    pokemon_id INTEGER PRIMARY KEY,
    pokemon_name TEXT UNIQUE,
    attack INTEGER,
    defense INTEGER,
    hp INTEGER
)
''')

# Insert sample data into the pokemon_stats table
cursor.executemany('''
INSERT OR IGNORE INTO pokemon_stats (pokemon_name, pokemon_id, attack, defense, hp) 
VALUES (?, ?, ?, ?, ?)
''', [
    ('Azumarill', 184, 112, 152, 225)
])

# Commit the changes and close the connection
conn.commit()
conn.close()

db_path  # Return the path of the created database file.

import sqlite3


class PokeStats:
    def __init__(self, db_path):
        """
        Initializes the connection to the database.
        :param db_path: The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_stats_with_ivs(self, pokemon_name, ivs):
        """
        Retrieves the base stats (Attack, Defense, HP) for the given Pokémon from the database,
        adds the IVs to each respective stat, and returns the total stats.

        :param pokemon_name: The name of the Pokémon to retrieve stats for.
        :param ivs: A dictionary with IV values for 'Attack', 'Defense', and 'HP'.
        :return: A dictionary with final stats after adding IVs.
        """
        # Retrieve base stats from the database
        query = "SELECT attack, defense, hp FROM pokemon_stats WHERE pokemon_name = ?"
        self.cursor.execute(query, (pokemon_name,))
        result = self.cursor.fetchone()

        if result:
            base_attack, base_defense, base_hp = result
            # Add IVs to base stats
            total_attack = base_attack + ivs['Attack']
            total_defense = base_defense + ivs['Defense']
            total_hp = base_hp + ivs['HP']

            return {
                'Total Attack': total_attack,
                'Total Defense': total_defense,
                'Total HP': total_hp
            }
        else:
            raise ValueError(f"Pokémon '{pokemon_name}' not found in the database.")

    def close(self):
        """Closes the connection to the database."""
        self.connection.close()


# Usage example for Azumarill
db_path = 'pokemon.db'
stats = PokeStats(db_path)

# Example IVs for Azumarill (0 Attack, 15 Defense, 15 HP)
azumarill_ivs = {'Attack': 0, 'Defense': 15, 'HP': 15}

try:
    azumarill_stats = stats.get_stats_with_ivs('Azumarill', azumarill_ivs)
    print("Azumarill's Total Stats with IVs:", azumarill_stats)
except ValueError as e:
    print(e)

# Close the connection
stats.close()

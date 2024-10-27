import itertools
import sqlite3

# Define the range of IVs for Attack, Defense, and HP
ivs_range = range(16)  # IVs range from 0 to 15

# SQLite database path
db_path = 'pokemon.db'

# Batch size for inserting data
BATCH_SIZE = 10000  # Insert data in batches of 10,000

# Connect to the SQLite database using context manager
with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()

    # Create a table to store IV combinations if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon_ivs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        iv_attack INTEGER,
        iv_defense INTEGER,
        iv_stamina INTEGER
    )
    ''')

    # Create indexes on iv_attack, iv_defense, and iv_stamina columns to improve query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_iv_attack ON pokemon_ivs (iv_attack)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_iv_defense ON pokemon_ivs (iv_defense)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_iv_stamina ON pokemon_ivs (iv_stamina)')

    # Generate combinations lazily using itertools.product (no need to store them all in memory)
    iv_combinations = itertools.product(ivs_range, ivs_range, ivs_range)

    # Batch insert combinations
    batch = []
    for count, combination in enumerate(iv_combinations, 1):
        batch.append(combination)

        # Once we have enough items in the batch, insert them
        if count % BATCH_SIZE == 0:
            cursor.executemany('''
                INSERT INTO pokemon_ivs (iv_attack, iv_defense, iv_stamina)
                VALUES (?, ?, ?)
            ''', batch)
            connection.commit()  # Commit the current batch
            batch.clear()  # Clear the batch

    # Insert any remaining combinations that didn't fill up the last batch
    if batch:
        cursor.executemany('''
            INSERT INTO pokemon_ivs (iv_attack, iv_defense, iv_stamina)
            VALUES (?, ?, ?)
        ''', batch)
        connection.commit()

    # Total number of combinations
    print(f"Inserted {count} IV combinations into the database.")

    # Print a message indicating that indexes were created
    print("Indexes on iv_attack, iv_defense, and iv_stamina columns have been created.")

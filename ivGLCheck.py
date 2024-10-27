import sqlite3
import math

# Connect to the pokemon.db SQLite database
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Fetch all the Pokémon base stats from the pokemon_stats table
cursor.execute("SELECT pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina FROM pokemon_stats")
pokemon_stats = cursor.fetchall()

# Fetch all the IV combinations from the pokemon_ivs table
cursor.execute("SELECT iv_attack, iv_defense, iv_stamina FROM pokemon_ivs")
ivs_combinations = cursor.fetchall()

# Fetch the level and corresponding multiplier from the cp_multiplier table
cursor.execute("SELECT level, multiplier FROM cp_multiplier ORDER BY level DESC")
cp_multipliers = cursor.fetchall()

# Store the multipliers in a dictionary for quick lookup
cp_multiplier_dict = {level: multiplier for level, multiplier in cp_multipliers}


# Function to calculate CP for a given level
def calculate_cp(calc_attack, calc_defense, calc_stamina, multiplier):
    return math.floor((calc_attack * (calc_defense ** 0.5) * (calc_stamina ** 0.5) * (multiplier ** 2)) / 10)


# Function to calculate the Stat Product (SP)
def calculate_stat_product(actual_attack, actual_defense, actual_stamina):
    return (actual_attack * actual_defense * actual_stamina) // 1000


# Main loop for processing each Pokémon and its IV combinations
for pokemon in pokemon_stats:
    pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina = pokemon
    results = []

    # Process each IV combination
    for ivs in ivs_combinations:
        iv_attack, iv_defense, iv_stamina = ivs

        # Calculate base attack, defense, stamina with IVs
        calc_attack = stat_attack + iv_attack
        calc_defense = stat_defense + iv_defense
        calc_stamina = stat_stamina + iv_stamina

        # Start at Level 50 and decrement until CP <= 1500
        for level, multiplier in cp_multipliers:
            cp = calculate_cp(calc_attack, calc_defense, calc_stamina, multiplier)

            if cp <= 1500:  # We found the valid CP under or equal to 1500
                # Calculate actual stats with the correct multiplier
                actual_attack = calc_attack * multiplier
                actual_defense = calc_defense * multiplier
                actual_stamina = calc_stamina * multiplier

                # Calculate the Stat Product (SP)
                sp = calculate_stat_product(actual_attack, actual_defense, actual_stamina)

                # Store the result
                results.append({
                    'rank': None,  # To be calculated later
                    'pokemon_id': pokemon_id,
                    'pokemon_name': pokemon_name,
                    'stat_attack': stat_attack,
                    'stat_defense': stat_defense,
                    'stat_stamina': stat_stamina,
                    'iv_attack': iv_attack,
                    'iv_defense': iv_defense,
                    'iv_stamina': iv_stamina,
                    'actual_attack': actual_attack,
                    'actual_defense': actual_defense,
                    'actual_stamina': actual_stamina,
                    'sp': sp,
                    'cp': cp,
                    'level': level
                })
                break  # Move to the next IV combination after finding the valid CP

    # Sort the results by Stat Product in descending order
    results_sorted = sorted(results, key=lambda x: x['sp'], reverse=True)

    # Set rank and calculate percentage
    max_sp = results_sorted[0]['sp']  # The highest Stat Product for this Pokémon
    for i, result in enumerate(results_sorted):
        result['rank'] = i + 1
        result['percentage'] = round((result['sp'] / max_sp) * 100, 2)

    # Create a new table for the Pokémon
    table_name = f"GL_{pokemon_id}_stats"
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            rank INTEGER,
            pokemon_id INTEGER,
            pokemon_name TEXT,
            stat_attack INTEGER,
            stat_defense INTEGER,
            stat_stamina INTEGER,
            iv_attack INTEGER,
            iv_defense INTEGER,
            iv_stamina INTEGER,
            actual_attack REAL,
            actual_defense REAL,
            actual_stamina REAL,
            sp INTEGER,
            cp INTEGER,
            level REAL,
            percentage REAL
        )
    ''')

    # Insert the results into the new table
    for result in results_sorted:
        cursor.execute(f'''
            INSERT INTO {table_name} (rank, pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina, 
                                      iv_attack, iv_defense, iv_stamina, actual_attack, actual_defense, actual_stamina, 
                                      sp, cp, level, percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['rank'], result['pokemon_id'], result['pokemon_name'], result['stat_attack'],
            result['stat_defense'], result['stat_stamina'], result['iv_attack'], result['iv_defense'],
            result['iv_stamina'], result['actual_attack'], result['actual_defense'], result['actual_stamina'],
            result['sp'], result['cp'], result['level'], result['percentage']
        ))

    # Commit after each Pokémon
    conn.commit()

# Close the database connection
conn.close()

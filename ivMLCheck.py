import sqlite3
import math

# Connect to the pokemon.db SQLite database
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Fetch all Pokémon stats
cursor.execute("SELECT pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina FROM pokemon_stats")
pokemon_stats = cursor.fetchall()

# Fetch IV combinations
cursor.execute("SELECT iv_attack, iv_defense, iv_stamina FROM pokemon_ivs")
ivs_combinations = cursor.fetchall()

# Fetch multipliers for Level 50 and Level 51 (highest levels in Pokémon GO)
cursor.execute("SELECT level, multiplier FROM cp_multiplier WHERE level IN (50, 51)")
level_multipliers = {level: multiplier for level, multiplier in cursor.fetchall()}
multiplier = level_multipliers[50]  # Use Level 50 as default for Master League


# Function to calculate CP
def calculate_cp(calc_attack, calc_defense, calc_stamina, multiplier):
    return math.floor((calc_attack * (calc_defense ** 0.5) * (calc_stamina ** 0.5) * (multiplier ** 2)) / 10)


# Function to calculate Stat Product (SP)
def calculate_stat_product(actual_attack, actual_defense, actual_stamina):
    sp = (actual_attack * actual_defense * actual_stamina) / 1000
    return math.ceil(sp * 10) / 10


# Loop through each Pokémon
for pokemon in pokemon_stats:
    pokemon_id, pokemon_name, stat_attack, stat_defense, stat_stamina = pokemon
    results = []

    # Process each IV combination
    for ivs in ivs_combinations:
        iv_attack, iv_defense, iv_stamina = ivs

        # Calculate base stats with IVs
        calc_attack = stat_attack + iv_attack
        calc_defense = stat_defense + iv_defense
        calc_stamina = stat_stamina + iv_stamina

        # Calculate CP using Level 50 multiplier
        cp = calculate_cp(calc_attack, calc_defense, calc_stamina, multiplier)

        # Calculate actual stats for SP
        actual_attack = calc_attack * multiplier
        actual_defense = calc_defense * multiplier
        actual_stamina = int(calc_stamina * multiplier)

        # Calculate Stat Product (SP)
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
            'level': 50,  # Level 50 is standard for Master League
        })

    # Sort the results by Stat Product in descending order, then by CP in descending order if SP is the same
    results_sorted = sorted(results, key=lambda x: (x['sp'], x['cp']), reverse=True)

    # Calculate rank and percentage
    max_sp = results_sorted[0]['sp']
    for i, result in enumerate(results_sorted):
        result['rank'] = i + 1
        result['percentage'] = round((result['sp'] / max_sp) * 100, 2)

    # Create a new table for each Pokémon to store Master League data
    table_name = f"ML_{pokemon_id}_stats"
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

    # Insert results into the new table
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

    # Commit each Pokémon's data separately to avoid losing data in case of interruption
    conn.commit()

# Close the database connection
conn.close()

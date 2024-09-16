import itertools

# Define the range of IVs for Attack, Defence, and HP
attack_ivs_range = range(16)  # IVs range from 0 to 15
defence_ivs_range = range(16)  # IVs range from 0 to 15
stamina_ivs_range = range(16)  # IVs range from 0 to 15

# Generate all possible combinations using itertools.product
combinations = list(itertools.product(attack_ivs_range, defence_ivs_range, stamina_ivs_range))

# Print the total number of combinations and a few examples
print(f"Total number of combinations: {len(combinations)}")
print("A few combinations:")
for combo in combinations[:10]:  # Display first 10 combinations as an example
    print(combo)

import sqlite3


class PokeStats:
    def __init__(self, db_path):
        """
        Initializes the connection to the database.
        :param db_path: The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_stats(self, pokemon_name):
        """
        Retrieves Attack, Defense, and HP stats for the given Pokémon from the database.
        :param pokemon_name: The name of the Pokémon to retrieve stats for.
        :return: A dictionary with 'Attack', 'Defense', and 'HP' stats.
        """
        query = """
        SELECT attack, defense, hp FROM pokemon_stats WHERE pokemon_name = ?
        """
        self.cursor.execute(query, (pokemon_name,))
        result = self.cursor.fetchone()

        if result:
            attack, defense, hp = result
            return {
                'Attack': attack,
                'Defense': defense,
                'HP': hp
            }
        else:
            raise ValueError(f"Pokémon '{pokemon_name}' not found in the database.")

    def close(self):
        """
        Closes the connection to the database.
        """
        self.connection.close()

# Usage example (assuming you have a database file named 'pokemon.db'):
db_path = 'pokemon.db'
stats = PokeStats(db_path)
poke_stats = stats.get_stats('Azumarill')
print(poke_stats)
stats.close()


# Re-establish connection to SQLite database
conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

# Create the CP_multiplier table
cursor.execute('''
CREATE TABLE IF NOT EXISTS CP_multiplier (
    level REAL PRIMARY KEY,
    multiplier REAL
)
''')

# Insert CP multiplier data into the table
cp_multiplier_data = [
    (1, 0.094),
    (1.5, 0.135137432),
    (2, 0.16639787),
    (2.5, 0.192650919),
    (3, 0.21573247),
    (3.5, 0.236572661),
    (4, 0.25572005),
    (4.5, 0.273530381),
    (5, 0.29024988),
    (5.5, 0.306057378),
    (6, 0.3210876),
    (6.5, 0.335445036),
    (7, 0.34921268),
    (7.5, 0.362457751),
    (8, 0.3752356),
    (8.5, 0.387592416),
    (9, 0.39956728),
    (9.5, 0.411193551),
    (10, 0.4225),
    (10.5, 0.432926409),
    (11, 0.44310755),
    (11.5, 0.453059959),
    (12, 0.4627984),
    (12.5, 0.472336093),
    (13, 0.48168495),
    (13.5, 0.4908558),
    (14, 0.49985844),
    (14.5, 0.508701765),
    (15, 0.51739395),
    (15.5, 0.525942511),
    (16, 0.5343543),
    (16.5, 0.542635738),
    (17, 0.5507927),
    (17.5, 0.558830586),
    (18, 0.5667545),
    (18.5, 0.574569133),
    (19, 0.5822789),
    (19.5, 0.589887907),
    (20, 0.5974),
    (20.5, 0.604823665),
    (21, 0.6121573),
    (21.5, 0.619404122),
    (22, 0.6265671),
    (22.5, 0.633649143),
    (23, 0.64065295),
    (23.5, 0.647580967),
    (24, 0.65443563),
    (24.5, 0.661219252),
    (25, 0.667934),
    (25.5, 0.674581896),
    (26, 0.6811649),
    (26.5, 0.687684904),
    (27, 0.69414365),
    (27.5, 0.70054287),
    (28, 0.7068842),
    (28.5, 0.713169109),
    (29, 0.7193991),
    (29.5, 0.725575614),
    (30, 0.7317),
    (30.5, 0.734741009),
    (31, 0.7377695),
    (31.5, 0.740785594),
    (32, 0.74378943),
    (32.5, 0.746781211),
    (33, 0.74976104),
    (33.5, 0.752729087),
    (34, 0.7556855),
    (34.5, 0.758630368),
    (35, 0.76156384),
    (35.5, 0.764486065),
    (36, 0.76739717),
    (36.5, 0.770297266),
    (37, 0.7731865),
    (37.5, 0.776064962),
    (38, 0.77893275),
    (38.5, 0.781790055),
    (39, 0.784637),
    (39.5, 0.787473608),
    (40, 0.7903),
    (40.5, 0.792803968),
    (41, 0.79530001),
    (41.5, 0.797800015),
    (42, 0.8003),
    (42.5, 0.802799995),
    (43, 0.8053),
    (43.5, 0.8078),
    (44, 0.81029999),
    (44.5, 0.812799985),
    (45, 0.81529999),
    (45.5, 0.81779999),
    (46, 0.82029999),
    (46.5, 0.82279999),
    (47, 0.82529999),
    (47.5, 0.82779999),
    (48, 0.83029999),
    (48.5, 0.83279999),
    (49, 0.83529999),
    (49.5, 0.83779999),
    (50, 0.84029999),
    (50.5, 0.84279999),
    (51, 0.84529999)
]

# Insert data into CP_multiplier table
cursor.executemany('INSERT OR IGNORE INTO CP_multiplier (level, multiplier) VALUES (?, ?)', cp_multiplier_data)

# Commit changes and close connection
conn.commit()
conn.close()

# import sqlite3
# import math
#
#
# class PokeStats:
#     def __init__(self, db_path):
#         """
#         Initializes the connection to the database.
#         :param db_path: The path to the SQLite database file.
#         """
#         self.connection = sqlite3.connect(db_path)
#         self.cursor = self.connection.cursor()
#
#     def get_stats_with_ivs(self, pokemon_name, ivs):
#         """
#         Retrieves the base stats (Attack, Defense, HP) for the given Pokémon from the database,
#         adds the IVs to each respective stat, and returns the total stats.
#
#         :param pokemon_name: The name of the Pokémon to retrieve stats for.
#         :param ivs: A dictionary with IV values for 'Attack', 'Defense', and 'HP'.
#         :return: A dictionary with final stats after adding IVs.
#         """
#         # Retrieve base stats from the database
#         query = "SELECT attack, defense, hp FROM pokemon_stats WHERE pokemon_name = ?"
#         self.cursor.execute(query, (pokemon_name,))
#         result = self.cursor.fetchone()
#
#         if result:
#             base_attack, base_defense, base_hp = result
#             # Add IVs to base stats
#             total_attack = base_attack + ivs['Attack']
#             total_defense = base_defense + ivs['Defense']
#             total_hp = base_hp + ivs['HP']
#
#             return {
#                 'Total Attack': total_attack,
#                 'Total Defense': total_defense,
#                 'Total HP': total_hp
#             }
#         else:
#             raise ValueError(f"Pokémon '{pokemon_name}' not found in the database.")
#
#     def get_multiplier(self, level):
#         """
#         Retrieves the CP multiplier for a given level from the database.
#         :param level: The Pokémon level.
#         :return: The multiplier value.
#         """
#         query = "SELECT multiplier FROM CP_multiplier WHERE level = ?"
#         self.cursor.execute(query, (level,))
#         result = self.cursor.fetchone()
#
#         if result:
#             return result[0]
#         else:
#             raise ValueError(f"Multiplier for level {level} not found.")
#
#     def calculate_cp(self, total_attack, total_defense, total_hp, level):
#         """
#         Calculates the CP based on the total attack, defense, and HP stats and the level multiplier.
#         :param total_attack: The total attack stat after IVs.
#         :param total_defense: The total defense stat after IVs.
#         :param total_hp: The total HP stat after IVs.
#         :param level: The Pokémon's level.
#         :return: The computed CP.
#         """
#         # Get the multiplier for the given level
#         multiplier = self.get_multiplier(level)
#
#         # Apply the multiplier to the stats
#         resulting_attack = total_attack * multiplier
#         resulting_defense = total_defense * multiplier
#         resulting_hp = total_hp * multiplier
#
#         # Calculate the CP using the formula
#         cp = (total_attack * (math.sqrt(total_defense)) * (math.sqrt(total_hp)) * (multiplier * multiplier)) / 10
#         return math.floor(cp)  # Return the CP rounded down to the nearest integer
#
#     def adjust_for_league(self, pokemon_name, ivs, max_cp):
#         """
#         Adjusts the level to fit within the CP limits for a league.
#         :param pokemon_name: The Pokémon name.
#         :param ivs: IVs dictionary for Attack, Defense, and HP.
#         :param max_cp: Maximum allowed CP for the league (1500 for Great League, 2500 for Ultra League).
#         :return: The level and CP that fit within the league limit.
#         """
#         stats = self.get_stats_with_ivs(pokemon_name, ivs)
#         level = 50.0  # Start at the highest level
#
#         # Compute CP and decrease level until the CP fits the league's limit
#         while level > 1:
#             cp = self.calculate_cp(stats['Total Attack'], stats['Total Defense'], stats['Total HP'], level)
#             if cp <= max_cp:
#                 return level, cp
#             level -= 0.5  # Decrease by 0.5 level increments
#
#         raise ValueError(f"Cannot adjust CP to fit within {max_cp} CP for {pokemon_name}.")
#
#     def close(self):
#         """Closes the connection to the database."""
#         self.connection.close()
#
#
# # Usage example for Great and Ultra Leagues
# db_path = 'pokemon.db'
# stats = PokeStats(db_path)
#
# # Example IVs for a Pokémon (e.g., Azumarill with IVs of Attack: 0, Defense: 15, HP: 15)
# ivs = {'Attack': 0, 'Defense': 15, 'HP': 15}
#
# # Adjust for Great League (max CP 1500)
# try:
#     level_gl, cp_gl = stats.adjust_for_league('Azumarill', ivs, 1500)
#     print(f"Great League - Level: {level_gl}, CP: {cp_gl}")
#
#     # Adjust for Ultra League (max CP 2500)
#     level_ul, cp_ul = stats.adjust_for_league('Azumarill', ivs, 2500)
#     print(f"Ultra League - Level: {level_ul}, CP: {cp_ul}")
#
# except ValueError as e:
#     print(e)
#
# # Close the connection
# stats.close()


import sqlite3
import math


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

    def get_multiplier(self, level):
        """
        Retrieves the CP multiplier for a given level from the database.
        :param level: The Pokémon level.
        :return: The multiplier value.
        """
        query = "SELECT multiplier FROM CP_multiplier WHERE level = ?"
        self.cursor.execute(query, (level,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            raise ValueError(f"Multiplier for level {level} not found.")

    def calculate_cp(self, total_attack, total_defense, total_hp, level):
        """
        Calculates the CP based on the total attack, defense, and HP stats and the level multiplier.
        :param total_attack: The total attack stat after IVs.
        :param total_defense: The total defense stat after IVs.
        :param total_hp: The total HP stat after IVs.
        :param level: The Pokémon's level.
        :return: The computed CP.
        """
        # Get the multiplier for the given level
        multiplier = self.get_multiplier(level)

        # Calculate the CP using the formula
        cp = ((total_attack * math.sqrt(total_defense) * math.sqrt(total_hp)) * (multiplier ** 2)) / 10
        return math.floor(cp)  # Return the CP rounded down to the nearest integer

    def adjust_for_league(self, pokemon_name, ivs, max_cp):
        """
        Adjusts the level to fit within the CP limits for a league.
        :param pokemon_name: The Pokémon name.
        :param ivs: IVs dictionary for Attack, Defense, and HP.
        :param max_cp: Maximum allowed CP for the league (1500 for Great League, 2500 for Ultra League).
        :return: The level and CP that fit within the league limit.
        """
        stats = self.get_stats_with_ivs(pokemon_name, ivs)
        level = 50.0  # Start at the highest level

        # Compute CP and decrease level until the CP fits the league's limit
        while level > 1:
            cp = self.calculate_cp(stats['Total Attack'], stats['Total Defense'], stats['Total HP'], level)
            if cp <= max_cp:
                return level, cp
            level -= 0.5  # Decrease by 0.5 level increments

        raise ValueError(f"Cannot adjust CP to fit within {max_cp} CP for {pokemon_name}.")

    def calculate_stat_product(self, total_attack, total_defense, total_hp, level):
        """
        Calculates the product of the final stats after applying the level multiplier,
        and divides the result by 1000.
        :param total_attack: The total attack stat after IVs.
        :param total_defense: The total defense stat after IVs.
        :param total_hp: The total HP stat after IVs.
        :param level: The Pokémon's level.
        :return: The product of (stat_attack * stat_defense * stat_hp) / 1000.
        """
        multiplier = self.get_multiplier(level)

        # Apply the multiplier to the stats
        stat_attack = total_attack * multiplier
        stat_defense = total_defense * multiplier
        stat_hp = total_hp * multiplier

        # Calculate the product and divide by 1000
        stat_product = (stat_attack * stat_defense * stat_hp) / 1000
        return stat_product

    def league_stat_product(self, pokemon_name, ivs):
        """
        Finds the level that fits the Pokémon's CP within both Great League and Ultra League,
        and calculates the stat product for both.

        :param pokemon_name: The Pokémon name.
        :param ivs: IVs dictionary for Attack, Defense, and HP.
        :return: A tuple with stat products for Great League and Ultra League.
        """
        stats = self.get_stats_with_ivs(pokemon_name, ivs)

        # Great League adjustment (CP <= 1500)
        level_gl, _ = self.adjust_for_league(pokemon_name, ivs, 1500)
        stat_product_gl = self.calculate_stat_product(stats['Total Attack'], stats['Total Defense'], stats['Total HP'],
                                                      level_gl)

        # Ultra League adjustment (CP <= 2500)
        level_ul, _ = self.adjust_for_league(pokemon_name, ivs, 2500)
        stat_product_ul = self.calculate_stat_product(stats['Total Attack'], stats['Total Defense'], stats['Total HP'],
                                                      level_ul)

        return stat_product_gl, stat_product_ul

    def close(self):
        """Closes the connection to the database."""
        self.connection.close()


# Usage example for Great and Ultra Leagues stat product calculation
db_path = 'pokemon.db'
stats = PokeStats(db_path)

# Example IVs for a Pokémon (e.g., Azumarill with IVs of Attack: 0, Defense: 15, HP: 15)
ivs = {'Attack': 2, 'Defense': 14, 'HP': 13}

try:
    # Adjust for Great League (max CP 1500)
    stat_product_gl = stats.league_stat_product('Azumarill', ivs)
    level_gl, cp_gl = stats.adjust_for_league('Azumarill', ivs, 1500)
    print(f"Great League - Level: {level_gl}, CP: {cp_gl}")
    print(f"Great League Stat Product: {stat_product_gl}")

    # Adjust for Ultra League (max CP 2500)
    stat_product_ul = stats.league_stat_product('Azumarill', ivs)
    level_ul, cp_ul = stats.adjust_for_league('Azumarill', ivs, 2500)
    print(f"Ultra League - Level: {level_ul}, CP: {cp_ul}")
    print(f"Ultra League Stat Product: {stat_product_ul}")

except ValueError as e:
    print(e)

# Close the connection
stats.close()

import os
import sqlite3
from pkmOCR import process_image  # Import the function from pkmOCR.py

# Database path
DB_PATH = 'pokemon.db'


# Function to get pokemon_id by pokemon_name
def get_pokemon_id_by_name(pokemon_name):
    """Fetches the pokemon_id for a given pokemon_name."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT pokemon_id FROM pokemon_stats WHERE pokemon_name = ?", (pokemon_name,))
        result = cursor.fetchone()
        return result[0] if result else None


# Function to get relevant evolutions based on the Pokémon's stage
def get_relevant_evolutions(pokemon_name):
    """Fetches relevant evolutions for a given pokemon_name based on its evolution stage."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT basic, stage2, stage3 FROM pokemon_evoline
            WHERE basic = ? OR stage2 = ? OR stage3 = ?
        """, (pokemon_name, pokemon_name, pokemon_name))

        result = cursor.fetchone()

        if not result:
            return []

        # Identify the evolution stage and filter based on requirements
        basic, stage2, stage3 = result
        if pokemon_name == basic:
            # If the Pokémon is basic, return itself, stage1, and stage2
            return [basic] + [stage for stage in [stage2, stage3] if stage]
        elif pokemon_name == stage2:
            # If the Pokémon is stage1, return itself (stage1) and stage2
            return [stage2] + ([stage3] if stage3 else [])
        elif pokemon_name == stage3:
            # If the Pokémon is stage2, return only itself (stage2)
            return [stage3]
        return []


# Function to query the database for rankings in different leagues
def get_rankings(pokemon_id, iv_attack, iv_defense, iv_stamina):
    """Fetches rankings for each league."""
    rankings = {}

    # Connect to the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # League tables mapping
        league_tables = {
            "Little Cup": f"LC_{pokemon_id}_stats",
            "Great League": f"GL_{pokemon_id}_stats",
            "Ultra League": f"UL_{pokemon_id}_stats",
            "Master League": f"ML_{pokemon_id}_stats"
        }

        # Query each league table using pokemon_id
        for league, table_name in league_tables.items():
            try:
                query = f"""
                    SELECT rank, sp, cp, level, percentage
                    FROM {table_name}
                    WHERE pokemon_id = ? AND iv_attack = ? AND iv_defense = ? AND iv_stamina = ?
                    ORDER BY rank ASC
                """
                cursor.execute(query, (pokemon_id, iv_attack, iv_defense, iv_stamina))

                result = cursor.fetchone()
                if result:
                    rankings[league] = {
                        "rank": result[0],
                        "stat_product": result[1],
                        "combat_power": result[2],
                        "level": result[3],
                        "percentage": result[4]
                    }
                else:
                    rankings[league] = "No ranking data found."

            except sqlite3.Error as e:
                print(f"[DEBUG] Error querying {league}: {e}")
                rankings[league] = "Error querying league data."

    return rankings


# Main function to process all images in a folder and save results in a text file
def process_folder(folder_path):
    # Open the text file in write mode
    with open("pokemon_rankings.txt", "w") as output_file:

        # Check each file in the folder
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)

                # Write the image filename to the file
                output_file.write(f"\nProcessing image: {filename}\n")
                output_file.write("-" * 40 + "\n")

                # Process the image to extract data
                extracted_data = process_image(image_path)

                if 'error' in extracted_data:
                    output_file.write(f"Error processing image: {extracted_data['error']}\n\n")
                    continue

                # Extract details from OCR results
                pokemon_name = extracted_data["ocr_specific"]["Name"]
                cp_value = extracted_data["ocr_specific"]["CP"]
                iv_attack = extracted_data["attack_value"]
                iv_defense = extracted_data["defense_value"]
                iv_stamina = extracted_data["hp_value"]
                is_shadow = extracted_data["is_shadow"]

                # Write extracted information
                output_file.write(f"Extracted Information for {pokemon_name}:\n")
                output_file.write(f"  CP: {cp_value}\n")
                output_file.write(f"  IVs - Attack: {iv_attack}, Defense: {iv_defense}, Stamina: {iv_stamina}\n")
                output_file.write(f"  Shadow Status: {'Shadow' if is_shadow else 'Normal'}\n\n")

                # Retrieve relevant evolutions for the Pokémon
                relevant_evolutions = get_relevant_evolutions(pokemon_name)

                if not relevant_evolutions:
                    output_file.write(f"No evolutionary data found for {pokemon_name}.\n\n")
                    continue

                # Iterate over each relevant evolution and get rankings
                for evo_name in relevant_evolutions:
                    pokemon_id = get_pokemon_id_by_name(evo_name)

                    if pokemon_id is None:
                        output_file.write(f"Skipping {evo_name} as it was not found in the database.\n\n")
                        continue

                    # Get rankings in each league using pokemon_id and IVs
                    rankings = get_rankings(pokemon_id, iv_attack, iv_defense, iv_stamina)

                    # Write the results for each league to the file
                    output_file.write(f"\n--- Rankings for {evo_name} ---\n")
                    for league, result in rankings.items():
                        output_file.write(f"--- {league} ---\n")
                        if isinstance(result, dict):
                            output_file.write(f"  Rank: {result['rank']}\n")
                            output_file.write(f"  Stat Product (SP): {result['stat_product']}\n")
                            output_file.write(f"  Combat Power (CP): {result['combat_power']}\n")
                            output_file.write(f"  Level: {result['level']}\n")
                            output_file.write(f"  Percentage: {result['percentage']}%\n")
                        else:
                            output_file.write(f"  {result}\n")

                # Add a separator for readability between entries
                output_file.write("\n" + "=" * 50 + "\n")


# Example usage
if __name__ == "__main__":
    # Replace with the path to your folder containing images
    folder_path = "path_to_screenshot_folder"
    process_folder(folder_path)

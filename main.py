import cv2
import numpy as np
import easyocr  # EasyOCR library for OCR
import os
import re


# Step 1: Load the base image with error handling
def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    return image


# Initialize the EasyOCR reader (load with English language support)
reader = easyocr.Reader(['en'])  # You can add more languages if needed


# OCR function using EasyOCR
def perform_ocr_on_image(image, allowlist=None):
    """
    Perform OCR on the entire image using EasyOCR with optional character allowlist.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = reader.readtext(gray_image, detail=0, allowlist=allowlist)
    extracted_text = ' '.join(result)
    return extracted_text.strip()


# Step 3: Define configurable HSV ranges for color detection
HSV_RANGES = {
    "orange": ([10, 100, 100], [25, 255, 255]),
    "red1": ([0, 100, 100], [10, 255, 255]),
    "red2": ([160, 100, 100], [180, 255, 255])
}


# Function to create masks for color detection
def create_color_masks(hsv_image, hsv_ranges):
    """
    Create color masks for given HSV ranges.
    """
    masks = {}
    for color, (lower, upper) in hsv_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        masks[color] = cv2.inRange(hsv_image, lower_np, upper_np)
    # Combine red masks into one for convenience
    masks['red'] = cv2.bitwise_or(masks['red1'], masks['red2'])
    return masks


def process_rectangles(rectangles, hsv_image, original_image, color_masks):
    """
    Process a set of rectangles, divide each rectangle into 5 parts,
    check for orange and red colors, and perform OCR on each part.
    """
    orange_count = 0
    red_detected = False
    ocr_results = []

    # Process each rectangle in the set
    for (top_left, bottom_right) in rectangles:
        rect_width = bottom_right[0] - top_left[0]
        rect_height = bottom_right[1] - top_left[1]
        division_width = rect_width // 5

        for j in range(5):
            x_start = top_left[0] + j * division_width
            x_end = x_start + division_width
            y_start = top_left[1]
            y_end = bottom_right[1]

            sub_image_hsv = hsv_image[y_start:y_end, x_start:x_end]
            sub_image_bgr = original_image[y_start:y_end, x_start:x_end]

            # Efficiently check for color dominance
            mask_red = color_masks['red'][y_start:y_end, x_start:x_end]
            mask_orange = color_masks['orange'][y_start:y_end, x_start:x_end]

            if np.count_nonzero(mask_red) > 0.5 * mask_red.size:
                red_detected = True
            elif np.count_nonzero(mask_orange) > 0.5 * mask_orange.size:
                orange_count += 1

            ocr_text = perform_ocr_on_image(sub_image_bgr)
            ocr_results.append(ocr_text)

    final_value = 15 if red_detected else (orange_count if orange_count > 0 else 0)
    return final_value, ocr_results


def process_set(rectangles, hsv_image, original_image, color_masks):
    """
    General function to process a given set of rectangles.
    """
    return process_rectangles(rectangles, hsv_image, original_image, color_masks)


# Step 5: Define rectangle positions (configurable)
RECTANGLES = {
    "attack": [
        [(149, 1940), (277, 1963)],
        [(278, 1940), (408, 1963)],
        [(408, 1940), (531, 1963)]
    ],
    "defense": [
        [(149, 2050), (277, 2077)],
        [(278, 2050), (408, 2077)],
        [(408, 2050), (531, 2077)]
    ],
    "hp": [
        [(149, 2162), (277, 2190)],
        [(278, 2162), (408, 2190)],
        [(408, 2162), (531, 2190)]
    ]
}


# Modified function to perform OCR on specific areas (Name and CP)
def perform_ocr_on_specific_areas(image, areas):
    """
    Perform OCR on specific predefined areas of the image.

    Args:
    - image: The input image in BGR format.
    - areas: A dictionary defining the areas for OCR with their coordinates.

    Returns:
    - A dictionary with the OCR results for each area.
    """
    ocr_results = {}

    for area_name, (top_left, bottom_right) in areas.items():
        # Crop the region of interest (ROI)
        roi = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Perform OCR on the ROI
        ocr_text = perform_ocr_on_image(roi)

        # Remove variations of "CP" and any leading spaces for the CP area
        if area_name == "CP":
            # Remove "CP" (case-insensitive) and leading spaces from the OCR text
            ocr_text = re.sub(r'^\D*', '', ocr_text, flags=re.IGNORECASE)

        ocr_results[area_name] = ocr_text

    return ocr_results


# Define areas for OCR (Name and CP)
OCR_AREAS = {
    "Name": ((315, 950), (855, 1080)),  # Replace with the actual coordinates for Name area
    "CP": ((345, 106), (760, 260))  # Replace with the actual coordinates for CP area
}


# Function to check if a Pokémon is a shadow Pokémon based on color detection
def is_shadow_pokemon(image, roi):
    """
    Determine if a Pokémon is a shadow Pokémon by checking the presence of specific colors.
    Args:
    - image: The input image in BGR format.
    - roi: The region of interest (top-left and bottom-right coordinates) where the Pokémon is located.
    Returns:
    - True if the Pokémon is a shadow Pokémon, False otherwise.
    """
    # Convert ROI to RGB format
    (top_left, bottom_right) = roi
    region = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)

    # Step 1: Check for the specific RGB color (175, 41, 164) in the defined region ((9, 15), (800, 121))
    psy_color = (175, 41, 164)
    psy_region = region_rgb[15:121, 9:800]  # Crop the specific region for the color check
    color_mask = cv2.inRange(psy_region, np.array(psy_color) - 10, np.array(psy_color) + 10)

    # If the specific color is found, return False
    if cv2.countNonZero(color_mask) > 0:
        return False

    # Step 2: Check for the presence of purple and blue shades
    # Define the purple and blue shades in RGB format
    purple_shades = [
        (107, 66, 158), (101, 45, 174), (108, 64, 184), (100, 37, 181), (173, 133, 222),
        (120, 47, 195), (116, 44, 192), (109, 42, 194), (106, 32, 201), (82, 34, 154),
        (136, 86, 208), (108, 65, 168), (73, 39, 138)
    ]
    blue_shades = [
        (15, 10, 85), (35, 22, 129), (28, 17, 109), (17, 14, 90), (26, 19, 114), (33, 20, 115)
    ]

    # Count the number of purple and blue shades
    purple_count = 0
    blue_count = 0

    for shade in purple_shades:
        mask = cv2.inRange(region_rgb, np.array(shade) - 10, np.array(shade) + 10)
        if cv2.countNonZero(mask) > 0:
            purple_count += 1

    for shade in blue_shades:
        mask = cv2.inRange(region_rgb, np.array(shade) - 10, np.array(shade) + 10)
        if cv2.countNonZero(mask) > 0:
            blue_count += 1

    # Determine if it is a shadow Pokémon
    return purple_count >= 3 and blue_count >= 3



# Function to process images in a folder
def process_images_in_folder(fpath):
    """
    Process multiple images in a given folder, performing OCR and color detection.
    """
    # Iterate over all files in the folder
    for filename in os.listdir(fpath):
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(fpath, filename)
            print(f"Processing image: {image_path}")

            try:
                # Load the image
                image = load_image(image_path)

                # Convert to HSV and create color masks
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                color_masks = create_color_masks(hsv_image, HSV_RANGES)

                # Process each set of rectangles and perform OCR
                attack_value, attack_ocr_results = process_set(RECTANGLES["attack"], hsv_image, image, color_masks)
                defense_value, defense_ocr_results = process_set(RECTANGLES["defense"], hsv_image, image, color_masks)
                hp_value, hp_ocr_results = process_set(RECTANGLES["hp"], hsv_image, image, color_masks)

                # Perform OCR on specific areas (Name and CP)
                ocr_specific_areas_results = perform_ocr_on_specific_areas(image, OCR_AREAS)

                # Check if the Pokémon is a shadow Pokémon
                roi = ((7, 14), (1161, 958))  # Example ROI for shadow Pokémon detection
                is_shadow = is_shadow_pokemon(image, roi)

                # Print the results for the current image
                print(f"Results for {filename}:")
                print(f"  Attack Value: {attack_value}")
                print(f"  Defense Value: {defense_value}")
                print(f"  HP Value: {hp_value}")
                print(f"  OCR Results for Specific Areas:")
                for area_name, ocr_text in ocr_specific_areas_results.items():
                    print(f"    {area_name}: {ocr_text}")
                print(f"  Is Shadow Pokémon: {is_shadow}\n")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


# Example usage:
folder_path = r'C:\Users\xxxx\Documents\pogo'  # Replace with the path to your folder containing images
process_images_in_folder(folder_path)

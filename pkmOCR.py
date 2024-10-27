import cv2
import numpy as np
import easyocr
import re

# Path to database
DB_PATH = 'pokemon.db'

# Initialize the EasyOCR reader (using GPU if available)
reader = easyocr.Reader(['en'], gpu=True)  # GPU support for faster processing if available

# Define rectangle positions for IV detection (configurable)
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

# Define specific OCR areas for Name and CP
OCR_AREAS = {
    "Name": ((315, 950), (855, 1080)),  # Replace with actual coordinates
    "CP": ((345, 106), (760, 260))  # Replace with actual coordinates
}

# HSV color ranges for detecting specific colors
HSV_RANGES = {
    "orange": ([10, 100, 100], [25, 255, 255]),
    "red1": ([0, 100, 100], [10, 255, 255]),
    "red2": ([160, 100, 100], [180, 255, 255])
}


# Load image from path with error handling
def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    return image


# Perform OCR on an image with optional allowlist
def perform_ocr_on_image(image, allowlist=None):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = reader.readtext(gray_image, detail=0, allowlist=allowlist)
    return ' '.join(result).strip()


# Create color masks based on HSV ranges
def create_color_masks(hsv_image, hsv_ranges):
    masks = {}
    for color, (lower, upper) in hsv_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        masks[color] = cv2.inRange(hsv_image, lower_np, upper_np)
    masks['red'] = cv2.bitwise_or(masks['red1'], masks['red2'])  # Combine red masks
    return masks


# Process rectangles for IV detection and color checks
def process_rectangles(rectangles, hsv_image, original_image, color_masks):
    orange_count = 0
    red_detected = False
    ocr_results = []

    for (top_left, bottom_right) in rectangles:
        rect_width = bottom_right[0] - top_left[0]
        division_width = rect_width // 5

        for j in range(5):
            x_start = top_left[0] + j * division_width
            x_end = x_start + division_width
            y_start = top_left[1]
            y_end = bottom_right[1]

            sub_image_hsv = hsv_image[y_start:y_end, x_start:x_end]
            sub_image_bgr = original_image[y_start:y_end, x_start:x_end]

            mask_red = color_masks['red'][y_start:y_end, x_start:x_end]
            mask_orange = color_masks['orange'][y_start:y_end, x_start:x_end]

            # Detect color
            if np.count_nonzero(mask_red) > 0.5 * mask_red.size:
                red_detected = True
            elif np.count_nonzero(mask_orange) > 0.5 * mask_orange.size:
                orange_count += 1

            # Perform OCR on sub-image
            ocr_text = perform_ocr_on_image(sub_image_bgr)
            ocr_results.append(ocr_text)

    final_value = 15 if red_detected else (orange_count if orange_count > 0 else 0)
    return final_value, ocr_results


# Perform OCR on specific areas (Name and CP)
def perform_ocr_on_specific_areas(image, areas):
    ocr_results = {}
    for area_name, (top_left, bottom_right) in areas.items():
        roi = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        ocr_text = perform_ocr_on_image(roi)

        # Remove "CP" prefix for CP area
        if area_name == "CP":
            ocr_text = re.sub(r'^\D*', '', ocr_text, flags=re.IGNORECASE)

        ocr_results[area_name] = ocr_text
    return ocr_results


# Detect if a Pokémon is a shadow Pokémon
def is_shadow_pokemon(image, roi):
    top_left, bottom_right = roi
    region = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)

    psy_color = (175, 41, 164)
    psy_region = region_rgb[15:121, 9:800]
    color_mask = cv2.inRange(psy_region, np.array(psy_color) - 10, np.array(psy_color) + 10)
    if cv2.countNonZero(color_mask) > 0:
        return False

    purple_shades = [(107, 66, 158), (101, 45, 174), (108, 64, 184)]
    blue_shades = [(15, 10, 85), (35, 22, 129)]

    purple_count = sum(
        cv2.countNonZero(cv2.inRange(region_rgb, np.array(shade) - 10, np.array(shade) + 10)) > 0 for shade in
        purple_shades)
    blue_count = sum(
        cv2.countNonZero(cv2.inRange(region_rgb, np.array(shade) - 10, np.array(shade) + 10)) > 0 for shade in
        blue_shades)

    return purple_count >= 3 and blue_count >= 3


# Process a single image and extract required information
def process_image(image_path):
    try:
        image = load_image(image_path)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        color_masks = create_color_masks(hsv_image, HSV_RANGES)

        attack_value, _ = process_rectangles(RECTANGLES["attack"], hsv_image, image, color_masks)
        defense_value, _ = process_rectangles(RECTANGLES["defense"], hsv_image, image, color_masks)
        hp_value, _ = process_rectangles(RECTANGLES["hp"], hsv_image, image, color_masks)

        ocr_specific_areas_results = perform_ocr_on_specific_areas(image, OCR_AREAS)
        is_shadow = is_shadow_pokemon(image, ((7, 14), (1161, 958)))

        return {
            "image": image_path,
            "attack_value": attack_value,
            "defense_value": defense_value,
            "hp_value": hp_value,
            "ocr_specific": ocr_specific_areas_results,
            "is_shadow": is_shadow
        }
    except Exception as e:
        return {"image": image_path, "error": str(e)}
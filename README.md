# Pokémon GO Appraisal OCR Tool

This program is a Pokémon GO OCR tool created using Python, OpenCV, and EasyOCR, along with other Python packages. It extracts appraisal data from Pokémon screenshots, such as Combat Power (CP), Name, Attack IV, Defense IV, HP IV, and Shadow Pokémon status.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configurations](#configurations)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This program is designed to work with Pokémon GO screenshots taken on an iPhone (Width: 1170 pixels, Height: 2532 pixels). The screenshots must include the appraisal information for a Pokémon. The program processes these screenshots and extracts relevant appraisal information using Optical Character Recognition (OCR) techniques and color detection.

## Features

- Extracts CP, Name, Attack IV, Defense IV, HP IV, and Shadow Pokémon status from screenshots.
- Uses EasyOCR for character recognition.
- Detects specific colors in screenshots to determine Pokémon stats and Shadow status.
- Supports bulk processing of images in a folder.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- OpenCV
- EasyOCR
- Numpy

### Install the required packages

You can install the required Python packages using pip. Run the following command in your terminal or command prompt:

```bash
pip install opencv-python-headless numpy easyocr
```

## Usage

1. Take a Screenshot: Capture a screenshot of the Pokémon appraisal screen in Pokémon GO using your iPhone.
2. Upload the Screenshot: Save the screenshot(s) to a specific folder on your computer.
3. Specify the Folder Path: In the folder_path variable, replace the example path with the path to your folder containing the images.
4. Run the Program: Execute the script to process the images in the folder. It will extract the appraisal data from each screenshot.

### Example

```python
# Replace with the path to your folder containing images
folder_path = r'C:\Users\xxxx\Documents\pogo'
process_images_in_folder(folder_path)
```

The program will process each image in the folder and output the results, such as CP, Name, IVs, and whether the Pokémon is a shadow Pokémon.

## Configurations

The following configurations may need to be adjusted based on your device and image dimensions:

1. Image Coordinates: The coordinates for specific regions in the image (like CP, Name, Attack IV, Defense IV, HP IV) are set based on iPhone screenshots with dimensions 1170x2532 pixels. If you're using a different device or resolution, adjust the coordinates accordingly in the OCR_AREAS and RECTANGLES dictionaries.
   - Example coordinate configuration for CP area:

     ```python
     OCR_AREAS = {
      "Name": ((315, 950), (855, 1080)),  # Adjust these coordinates as needed
      "CP": ((345, 106), (760, 260))  # Adjust these coordinates as needed
     }
     ```

2. Color Ranges for Shadow Pokémon Detection: The HSV ranges for color detection and the RGB values for detecting shadow Pokémon are predefined. Adjust these ranges based on your needs or device settings.

## Limitations

- The program is specifically configured for screenshots with dimensions of 1170x2532 pixels. For other devices and/or screenshot sizes, the coordinates need to be changed.
- Accuracy of OCR may vary depending on the quality of screenshots and lighting conditions.
- The program does not support images in non-standard formats.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### License (MIT License)

```text

MIT License

Copyright (c) [2024] [syn-thesia]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**DISCLAIMER:**

This software is provided for educational and informational purposes only.
The author is not responsible for any misuse, loss of data, or damage resulting from the use of this software.
Users are solely responsible for their actions while using this software.

This project is not affiliated with, endorsed by, or associated with The Pokémon Company, Niantic, or any of their affiliates.
Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc., and Game Freak Inc.











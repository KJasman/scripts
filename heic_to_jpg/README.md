# HEIC to JPEG Converter

This Python script is used to convert HEIC image files to JPEG format. It uses the Wand library to read HEIC files and write them as JPEG files.

## Dependencies

- Wand
- shutil (built-in)
- os (built-in)

Before running the script, you need to install Wand and its dependencies:

\`\`\`bash
pip install wand
brew install freetype imagemagick
\`\`\`

## How it works

The script defines a function `convert_heic_to_jpg` that takes a HEIC file path and a JPEG file path, reads the HEIC file using Wand, converts it to JPEG format, and saves it to the specified JPEG file path.

The script then sets a source folder (`to_print`) and a destination folder (`old_heic`) for processed HEIC files. If the destination folder does not exist, it creates it.

The script then iterates over all files in the source folder. If a file ends with the `.HEIC` extension, it converts the file to JPEG format and moves the original HEIC file to the destination folder.

## Usage

To use this script, simply run it in a Python environment where Wand is installed. Make sure your HEIC files are in the source folder.

\`\`\`python
python3 heic_to_jpeg_converter.py
\`\`\`

## Output

The output JPEG files will be saved in the source folder, and the original HEIC files will be moved to the destination folder.

## Note

This script assumes that the source folder exists in the same directory as the script. If it does not exist, you will need to create it before running the script. The destination folder will be created by the script if it does not exist.
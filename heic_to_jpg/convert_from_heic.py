from wand.image import Image
import shutil # default
import os #default

# Note: install wand and its dependancies 
# pip install wand && brew install freetype imagemagick 

def convert_heic_to_jpg(heic_path, jpg_path):
    with Image(filename=heic_path) as img:
        img.format = 'jpeg'
        img.save(filename=jpg_path)

folder_path = "to_print" # Modify this line to set the source folder
done_folder_path = "old_heic" # Destination folder for processed .heic files

if not os.path.exists(done_folder_path):
    os.makedirs(done_folder_path)

for filename in os.listdir(folder_path):
    if filename.endswith(".HEIC"):
        heic_path = os.path.join(folder_path, filename)
        jpg_path = os.path.splitext(heic_path)[0] + ".jpg"
        convert_heic_to_jpg(heic_path, jpg_path)
        shutil.move(heic_path, os.path.join(done_folder_path, filename))  # Move the .heic file to the "done" directory
import os
import shutil
from sklearn.model_selection import train_test_split

# Define the directory where your images are located
image_dir = '/dataset'

# Define the directories where the train and validation images will be stored
train_dir = '/dataset/train'
val_dir = '/dataset/validate'

# Get a list of all image file names
image_files = os.listdir(image_dir)

# Split the file names into train and validation sets
train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

# Create the train and validation directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Move the files into the train and validation directories
for file_name in train_files:
    shutil.move(os.path.join(image_dir, file_name), os.path.join(train_dir, file_name))

for file_name in val_files:
    shutil.move(os.path.join(image_dir, file_name), os.path.join(val_dir, file_name))
# Split_Images_CV

This Python script is used to split an image dataset into training and validation sets. The split ratio is 80% for training and 20% for validation.

## Requirements

The script requires the following Python libraries:

- os
- shutil
- sklearn

## How to Use

1. Place your image dataset in a directory. By default, the script looks for images in the `/dataset` directory.

2. Run the script. It will automatically create two directories, `/dataset/train` and `/dataset/validate`, for the training and validation sets, respectively.

3. The script will then move the images from the original directory to the training and validation directories. The split is done randomly but in a deterministic way (random state is set to 42), so running the script multiple times with the same dataset will produce the same split.

## Customization

You can customize the script by changing the following variables:

- `image_dir`: The directory where your images are located.
- `train_dir`: The directory where the training images will be stored.
- `val_dir`: The directory where the validation images will be stored.
- `test_size`: The proportion of the dataset to include in the validation split (0.2 means 20% of images will be used for validation).
- `random_state`: The seed used by the random number generator for shuffling the data before applying the split.

## Note

This script moves the images from the original directory to the train and validation directories. If you want to keep the original images in place and make copies instead, you can modify the script by replacing `shutil.move` with `shutil.copy`.
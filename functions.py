# functions to handle change_images512.py

from PIL import ImageStat
import glob
import numpy as np
import colorsys
import os
from PIL import Image
from tqdm import tqdm


dark_threshold = 128
dark_percentage = 30

white_threshold = 200
white_percentage = 50

color_threshold = 128
color_percentage = 30


default_color = '#000000'
default_color_rgb = (0, 0, 0)
default_height = 512
default_width = 512
default_color_specs = None
# checking for tracking
chk_black = False
chk_white = False
chk_color = False




def count_images_in_folder(folder_path):
    # List all files in the directory
    files = os.listdir(folder_path)

    # Filter out non-image files
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Print the count
    print(f"There are {len(image_files)} image(s) in the folder.")
    return len(image_files)




# Function to calculate the percentage of dark pixels in a row
def get_dark_space_percentage(image):
    # Calculate the percentage of dark pixels in each row of the image
    width, height = image.size

    for y in range(height):
        row = [image.getpixel((x, y)) for x in range(width)]
        total_pixels = len(row)
        dark_pixels = 0

        for pixel in row:
            if isinstance(pixel, int):
                # Grayscale image
                if pixel < dark_threshold:
                    dark_pixels += 1
            else:
                # RGB image
                if sum(pixel) < dark_threshold:
                    dark_pixels += 1

        if (dark_pixels / total_pixels) * 100 > dark_percentage:
            return True

    return False



# Function to calculate the percentage of white pixels in a row
def get_white_space_percentage(image):
    # Calculate the percentage of white pixels in each row of the image
    width, height = image.size

    for y in range(height):
        row = [image.getpixel((x, y)) for x in range(width)]
        total_pixels = len(row)
        white_pixels = 0

        for pixel in row:
            if isinstance(pixel, int):
                # Grayscale image
                if pixel > white_threshold:
                    white_pixels += 1
            else:
                # RGB image
                if sum(pixel) > white_threshold * 3:
                    white_pixels += 1

        # Calculate the percentage of white pixels in the row
        white_pixels_percentage = (white_pixels / total_pixels) * 100

        if white_pixels_percentage > white_percentage:
            return True

    # If no row has a percentage of white pixels greater than the specified percentage, return False
    return False

# Function to delete images with a large amount of dark space in a row
def delete_images(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        # Check if the file exists before trying to open it
        if os.path.exists(filepath):
            # Open the image file
            img = Image.open(filepath)
            
            # Check if the image has a row with a large amount of dark space
            if get_dark_space_percentage(img):
                os.remove(filepath)
                print(f'Deleted {filename} due to high dark space in a row.')
            # Check if the image has a row with a large amount of white space
            if get_white_space_percentage(img):
                os.remove(filepath)
                print(f'Deleted {filename} due to high white space in a row.')
        else:
            print(f"File {filepath} not found")

    print("Finished deleting images with high dark space.")




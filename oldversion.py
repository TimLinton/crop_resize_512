# Description: This script takes a large image file and crops it into 512x512 images and then
# deletes the images that have a large amount of dark space in a row.
# and then saves the cropped images in a new folder.

import os
import argparse
from PIL import Image
import colorsys
from tqdm import tqdm

# Create the parser
parser = argparse.ArgumentParser(description='This script processes a large image, crops it into smaller images, and deletes images with a high percentage of a specified color.')

# Add the arguments
parser.add_argument('large_img_path', type=str,
                    help='The path to the large image file. Example: "/home/user/Pictures/image.png"')
parser.add_argument('new_folder', type=str,
                    help='The new folder to save the cropped images. Example: "/home/user/Pictures/CroppedImages"')
parser.add_argument('--color', type=str, nargs='*', default=['#000000'],
                    help='The colors to check for in hexadecimal or RGB format. Default is black (#000000). Example: "#FFFFFF" "#FF0000" or "255,255,255" "255,0,0"')
parser.add_argument('--color_threshold', type=int, default=70,
                    help='The color threshold. If a pixel\'s color is above this threshold, it is considered as a color pixel. Default is 70. Example: 80')
parser.add_argument('--color_percentage', type=int, default=10,
                    help='The percentage of color pixels in a row for an image to be considered having too much of that color. Default is 10. Example: 20')
parser.add_argument('--color_specs', type=str, nargs='*', default=None,
                    help='The color specifications in the format "color,threshold,percentage". Example: "#FFFFFF,80,20" "#FF0000,70,10"')

# Parse the arguments
args = parser.parse_args()

# Define the dark threshold
dark_threshold = 60
white_threshold = 700

# Define the percentage of dark pixels in a row for an image to be considered dark
dark_percentage = 10
white_percentage = 10

# Parse the arguments
args = parser.parse_args()

# Calculate the total number of images to process
total_images = len(os.listdir(args.new_folder))

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)

# Open the large image file
large_img = Image.open(args.large_img_path)


colors = []
for color in args.color:
    if color.startswith('#'):
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        r, g, b = map(int, color.split(','))
    # Convert the RGB color to a format that can be compared with the pixel values
    colors.append(colorsys.rgb_to_yiq(r, g, b))

# Convert the RGB color to a format that can be compared with the pixel values
color = colorsys.rgb_to_yiq(r, g, b)

# Define the color threshold and percentage
color_threshold = args.color_threshold
color_percentage = args.color_percentage

# Define the path to the large image file and the new folder
large_img_path = args.large_img_path
new_folder = args.new_folder
args = parser.parse_args()

# Convert single color string to list if necessary
if isinstance(args.color, str):
    args.color = [args.color]


# Parse the color specifications
color_specs = []
if args.color_specs:
    for spec in args.color_specs:
        color, threshold, percentage = spec.split(',')
        color_specs.append((color, int(threshold), int(percentage)))
else:
    # Default values
    color_specs.append(('#000000', 70, 10))  # Black
    color_specs.append(('#FFFFFF', 80, 20))  # White

def get_color_space_percentage(image, color, threshold, percentage):
    # Calculate the percentage of color pixels in each row of the image
    width, height = image.size

    for y in range(height):
        row = [image.getpixel((x, y)) for x in range(width)]
        total_pixels = len(row)
        color_pixels = 0

        for pixel in row:
            if isinstance(pixel, int):
                # Grayscale image
                if pixel > threshold:
                    color_pixels += 1
            else:
                # RGB image
                if colorsys.rgb_to_yiq(*pixel) > color:
                    color_pixels += 1

        if (color_pixels / total_pixels) * 100 > percentage:
            return True

    return False
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
                if sum(pixel) > white_threshold:
                    white_pixels += 1

        if (white_pixels / total_pixels) * 100 > white_percentage:
            return True

    return False

# Function to delete images with a large amount of white space in a row

# Parse the arguments
args = parser.parse_args()

# Calculate the total number of images to process
total_images = len(os.listdir(args.new_folder))

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)

# Function to delete images with a large amount of white space in a row
def delete_white_images(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        img = Image.open(filepath)

        # Check if the image has a row with a large amount of white space
        if get_white_space_percentage(img):
            os.remove(filepath)
            print(f'Deleted {filename} due to high white space in a row.')
        
        # Update the progress bar
        progress_bar.update(1)

    print("Finished deleting images with high white space.")

# Function to delete images with a large amount of dark space in a row
def delete_dark_images(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        img = Image.open(filepath)

        # Check if the image has a row with a large amount of dark space
        if get_dark_space_percentage(img):
            os.remove(filepath)
            print(f'Deleted {filename} due to high dark space in a row.')
        
        # Update the progress bar
        progress_bar.update(1)

    print("Finished deleting images with high dark space.")


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
def delete_color_images(folder, color_specs):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        img = Image.open(filepath)

        # Check if the image has a large amount of the chosen color
        for color, threshold, percentage in color_specs:
            if get_color_space_percentage(img, color, threshold, percentage):
                os.remove(filepath)
                print(f'Deleted {filename} due to high {color} space.')
                break  # break the loop if the image is deleted

        # Update the progress bar
        progress_bar.update(1)

    print("Finished deleting images with high color space.")

def get_color_space_percentage(image, color):
    # Calculate the percentage of color pixels in each row of the image
    width, height = image.size

    for y in range(height):
        row = [image.getpixel((x, y)) for x in range(width)]
        total_pixels = len(row)
        color_pixels = 0

        for pixel in row:
            if isinstance(pixel, int):
                # Grayscale image
                if pixel > color_threshold:
                    color_pixels += 1
            else:
                # RGB image
                if colorsys.rgb_to_yiq(*pixel) > color:
                    color_pixels += 1

        if (color_pixels / total_pixels) * 100 > color_percentage:
            return True

    return False




# Create a new folder to save the cropped images
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# Loop through rows and columns
height = large_img.height
width = large_img.width
for r in range((height // 512) + 1):
    for c in range((width // 512) + 1):
        # Calculate the left, upper, right, lower pixel coordinate
        left = c * 512
        upper = r * 512
        right = (c + 1) * 512
        lower = (r + 1) * 512

        # Crop the image
        cropped_img = large_img.crop((left, upper, right, lower))

        # Save the cropped image
        filename = f'cropped_{r+1}_{c+1}.jpg'
        filepath = os.path.join(new_folder, filename)
        cropped_img.save(filepath)

        # Check if there's dark black space and delete it
        delete_dark_images(new_folder)
        delete_white_images(new_folder)
progress_bar.close()

print(f'{(height // 512) * (width // 512)} images have been created.')
print("Script finished executing.")
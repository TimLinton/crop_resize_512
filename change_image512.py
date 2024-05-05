# Description: This script takes a large image file and crops it into 512x512 images and then
# deletes the images that have a large amount of dark space in a row.
# and then saves the cropped images in a new folder.

import os
import argparse
from PIL import Image
from PIL import ImageStat
import numpy as np
import colorsys
from tqdm import tqdm
import time
Image.MAX_IMAGE_PIXELS = None

# Create the parser
parser = argparse.ArgumentParser(description='This script processes a large image, crops it into smaller images, and deletes images with a high percentage of a specified color.')

# Add the arguments
parser.add_argument('-i', '--image', type=str, required=True, help='The path to the large image file. Example: "/home/user/Pictures/image.png"')
parser.add_argument('-id', '--input-dir', type=str, help='The path to the directory containing image files. Example: "/home/user/Pictures/Images"')

parser.add_argument('-d', '--dest', type=str, required=True, help='The new folder to save the cropped images. Example: "/home/user/Pictures/CroppedImages"')
parser.add_argument('--color', type=str, nargs='*', default=['#000000'],
                    help='The colors to check for in hexadecimal or RGB format. Default is black (#000000). Example: "#FFFFFF" "#FF0000" or "255,255,255" "255,0,0"')
parser.add_argument('--color_threshold', type=int, default=60,
                    help='The color threshold. If a pixel\'s color is above this threshold, it is considered as a color pixel. Default is 70. Example: 80')
parser.add_argument('--color_percentage', type=int, default=10,
                    help='The percentage of color pixels in a row for an image to be considered having too much of that color. Default is 10. Example: 20')
parser.add_argument('--color_specs', type=str, nargs='*', default=None,
                    help='The color specifications in the format "color,threshold,percentage". Example: "#FFFFFF,80,20" "#FF0000,70,10"')
parser.add_argument('-bw', '--black_white', action='store_true', help='Check for both black and white colors.')
parser.add_argument('-b', '--black', action='store_true', help='Check for black color. This is the default behavior.')
parser.add_argument('-w', '--white', action='store_true', help='Check for white color.')

# Parse the arguments
args = parser.parse_args()


if args.input_dir:
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(args.input_dir) if os.path.isfile(os.path.join(args.input_dir, f))]

    # Process each image file
    for image_file in image_files:
        # Open the image file
        large_img = Image.open(os.path.join(args.input_dir, image_file))
else:
    # Open the large image file
    large_img = Image.open(args.image)


# Define the path to the large image file and the new folder
large_img_path = args.image
new_folder = args.dest
num_rows = (large_img.height // 512) + 1
num_cols = (large_img.width // 512) + 1

# Calculate the total number of images that will be generated
total_images = num_rows * num_cols

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)

# Define the dark threshold
dark_threshold = 60
white_threshold = None if not args.white and not args.black_white else 700

# Define the percentage of dark pixels in a row for an image to be considered dark
dark_percentage = 10
white_percentage = None if not args.white and not args.black_white else 30

# Parse the color specifications

color_specs = []
# if args.black or args.black_white:
#     color_specs.append(('#000000', 70, 10))  # Black
# if args.white or args.black_white:
#     color_specs.append(('#FFFFFF', 80, 20))  # White

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)

print(f"Image: {args.image}")
print(f"Destination: {args.dest}")
print(f"Color: {args.color}")
print(f"Color Threshold: {args.color_threshold}")
print(f"Color Percentage: {args.color_percentage}")
print(f"Color Specs: {args.color_specs}")
print(f"Black White: {args.black_white}")

# Calculate the number of rows and columns
num_rows = (large_img.height // 512) + 1
num_cols = (large_img.width // 512) + 1

# Calculate the total number of images that will be generated
total_images = num_rows * num_cols

print(f'Total images to be generated before deletion: {total_images}')

# Initialize a list to store the processing times of the first two images
processing_times = []

# Convert single color string to list if necessary
if isinstance(args.color, str):
    args.color = [args.color]

colors = []
for color in args.color:
    if color.startswith('#'):
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        r, g, b = map(int, color.split(','))
    # Convert the RGB color to a format that can be compared with the pixel values
    colors.append(colorsys.rgb_to_yiq(r, g, b))  # Store the tuple, not the string

# Define the color threshold and percentage
color_threshold = args.color_threshold
color_percentage = args.color_percentage

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

# Calculate the total number of images to process
total_images = len(os.listdir(new_folder))

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)


def get_color_space_percentage(image, color_threshold, percentage):
    # Calculate the percentage of pixels in each row of the image that meet the color threshold
    width, height = image.size

    for y in range(height):
        row = [image.getpixel((x, y)) for x in range(width)]
        total_pixels = len(row)
        matching_pixels = 0

        for pixel in row:
            if isinstance(pixel, int):
                # Grayscale image
                if pixel > color_threshold:
                    matching_pixels += 1
            else:
                # RGB image
                if sum(pixel) > color_threshold:
                    matching_pixels += 1

        matching_percentage = (matching_pixels / total_pixels) * 100
        if matching_percentage > percentage:
            print(f"Image has {matching_percentage}% matching pixels.")
            return True

    return False

# Function to calculate image statistics
def calculate_image_stats(img):
    stat = ImageStat.Stat(img)
    return stat.mean[0]


# Create a new folder to save the cropped images
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# Dictionary to store image statistics
image_stats = {}
# Delete images based on color
def delete_images(image_stats, new_folder, color='dark', threshold=50, percentage=10):
    for filename, mean in image_stats.items():
        filepath = os.path.join(new_folder, filename)
        if not os.path.exists(filepath):
            print(f"File {filepath} does exist. Skipping...")
            continue
        else:
            print(f"File {filepath} does not exist.")
        img = Image.open(os.path.join(new_folder, filename))
        if color == 'dark' and mean < threshold:
            os.remove(os.path.join(new_folder, filename))
            print(f'Deleted {filename} due to high darkness.')
        elif color == 'white' and mean > threshold:
            os.remove(os.path.join(new_folder, filename))
            print(f'Deleted {filename} due to high whiteness.')
        elif color.startswith('#'):
            r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            color_rgb = np.array([r, g, b])
            img_rgb = np.array(img)
            diff = np.sqrt(np.sum((img_rgb - color_rgb)**2, axis=2))
            color_percentage = np.sum(diff < threshold) / diff.size * 100
            if color_percentage > percentage:
                os.remove(os.path.join(new_folder, filename))
                print(f'Deleted {filename} due to high {color} color.')


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

        # Calculate image statistics and store them
        image_stats[filename] = calculate_image_stats(cropped_img)

# Call delete_images() function after all images have been processed
for color_spec in color_specs:
    color, threshold, percentage = color_spec
    delete_images(image_stats, new_folder, color=color, threshold=threshold, percentage=percentage)

progress_bar.close()

print(f'{(height // 512) * (width // 512)} images have been created.')
print("Script finished executing.")
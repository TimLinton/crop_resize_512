# Description: This script takes a large image file and crops it into a chosen size of images and then
# deletes the images that have a large amount of dark space in a row using a chosen color or no color by default (black) .
# and then saves the cropped images in a new folder.
import os
import argparse
from PIL import Image

from tqdm import tqdm
import time
from pathlib import Path
import ast
from functions import default_color, default_color_rgb, default_height, default_width, default_color_specs, chk_black, chk_white, chk_color
from functions import  delete_images, count_images_in_folder


Image.MAX_IMAGE_PIXELS = None




# Create the parser
parser = argparse.ArgumentParser(description='This script processes a large image, crops it into smaller images, and deletes images with a high percentage of a specified color.')
# Add the arguments
parser.add_argument('-i', '--image', type=str, help='The path to the large image file. Example: "/home/user/Pictures/image.png"')
parser.add_argument('-id', '--input-dir', type=str, help='The path to the directory containing image files. Example: "/home/user/Pictures/Images"')

parser.add_argument('-d', '--dest', type=str, required=True, help='The new folder to save the cropped images. Example: "/home/user/Pictures/CroppedImages"')
parser.add_argument('--color', type=str, default='#000000',
                    help='The colors to check for in hexadecimal or RGB format. Default is black (#000000). Example: "#FFFFFF" "#FF0000" or "255,255,255" "255,0,0"')
parser.add_argument('--color_threshold', type=int, default=70,
                    help='The color threshold. If a pixel\'s color is above this threshold, it is considered as a color pixel. Default is 70. Example: 80')
parser.add_argument('--color_percentage', type=int, default=10,
                    help='The percentage of color pixels in a row for an image to be considered having too much of that color. Default is 10. Example: 20')
parser.add_argument('--color_specs', type=ast.literal_eval, nargs='*', default=None,
                    help='The color specifications in the format "color,threshold,percentage". Example: "#FFFFFF,80,20" "#FF0000,70,10"')
parser.add_argument('-bw', '--black_white', action='store_true', help='Check for both black and white colors.')
parser.add_argument('-b', '--black', action='store_true', help='Check for black color. This is the default behavior.')
parser.add_argument('-w', '--white', action='store_true', help='Check for white color.')
parser.add_argument('--height', type=int, default=512, help='The desired height of the cropped images. Default is 512.')
parser.add_argument('--width', type=int, default=512, help='The desired width of the cropped images. Default is 512.')


# Use the desired dimensions
# load in all args


# Parse the arguments
args = parser.parse_args()
if args.black or args.black_white:
    chk_black = True
    chk_white = False
    chk_color = False
if args.white:
    chk_black = False
    chk_white = True
    chk_color = False
if args.color:
    chk_black = False
    chk_white = False
    chk_color = True

color_specs = []

color_threshold = args.color_threshold

# Parse the color specifications
if args.height:
    desired_height = args.height
if args.width:
    desired_width = args.width
if args.color_specs:
    for spec in args.color_specs:
        color, threshold, percentage = spec.split(',')
        color_specs.append((color, int(threshold), int(percentage)))

# Create a new folder to save the cropped images
if not os.path.exists(args.dest):
    os.makedirs(args.dest)

# Dictionary to store image statistics


if args.input_dir:
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(args.input_dir) if Path(f).suffix in ['.jpg', '.jpeg', '.png'] and os.path.isfile(os.path.join(args.input_dir, f))]

    # Define the path to the new folder
    new_folder = args.dest

    # Process each image file
    for image_file in image_files:
        # check how many files are in the folder only 1 time, do not check again
        if image_files.index(image_file) == 0:
            images_in_folder = count_images_in_folder(args.input_dir)
            
        original_filename = os.path.splitext(os.path.basename(image_file))[0]
        large_img = Image.open(os.path.join(args.input_dir, image_file))
        large_img_path = os.path.join(args.input_dir, image_file)
        directory_path = os.path.dirname(large_img_path)


        num_rows = (large_img.height // desired_height) + 1
        num_cols = (large_img.width // desired_width) + 1

        # Calculate the total number of images that will be generated
        total_images = num_rows * num_cols




else:
    large_img = Image.open(args.image)

if args.black_white:
    color_specs.append(('#000000', 70, 10))  # Black
    color_specs.append(('#FFFFFF', 80, 20))  # White
if args.black:
    color_specs.append(('#000000', 70, 10))  # Black
if args.white:
    color_specs.append(('#FFFFFF', 80, 20))  # White

if args.color and args.color_threshold and args.color_percentage:
    color_specs.append((args.color, args.color_threshold, args.color_percentage))

# Define the dark threshold
# dark_threshold = 60
# white_threshold = None if not args.white and not args.black_white else 700

# # Define the percentage of dark pixels in a row for an image to be considered dark
# dark_percentage = 10
# white_percentage = None if not args.white and not args.black_white else 30




# Loop through rows and columns based on the desired dimensions
for r in range((large_img.height // desired_height) + 1):
    for c in range((large_img.width // desired_width) + 1):
        # Calculate the left, upper, right, lower pixel coordinate based on the desired dimensions
        left = c * desired_width
        upper = r * desired_height
        right = (c + 1) * desired_width
        lower = (r + 1) * desired_height

        # Crop the image based on the desired dimensions
        cropped_img = large_img.crop((left, upper, right, lower))

        # Save the cropped image
        filename = f'cropped_{r+1}_{c+1}.jpg'
        filepath = os.path.join(new_folder, filename)
        cropped_img.save(filepath)

        # Delete images with a large amount of black or white space


        # delete_images(new_folder)  # White
print(f'{(large_img.height // desired_height) * (large_img.width // desired_width)} images have been created.')

# Create a progress bar
progress_bar = tqdm(total=total_images, desc="Processing images", ncols=100)

print(f"Image: {args.image}")
print(f"Destination: {args.dest}")
print(f"Color: {args.color}")
print(f"Color Threshold: {args.color_threshold}")
print(f"Color Percentage: {args.color_percentage}")
print(f"Color Specs: {args.color_specs}")
print(f"Black White: {args.black_white}")

# Calculate the number of rows and columns based on the desired dimensions.

num_rows = (large_img.height // desired_height) + 1
num_cols = (large_img.width // desired_width) + 1

# Calculate the total number of images that will be generated based on the desired dimensions
total_images = num_rows * num_cols

# Calculate the total number of images that will be generated
total_images = num_rows * num_cols * images_in_folder

print(f'Estimated total images to be generated before deletion: {total_images}')

# Initialize a list to store the processing times of the first two images
processing_times = []

# Convert single color string to list if necessary
if isinstance(args.color, str):
    args.color = [args.color]


# Define the color threshold and percentage
color_threshold = args.color_threshold
color_percentage = args.color_percentage





# Create a new folder to save the cropped images
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# Dictionary to store image statistics


# Parse the color specifications
if args.color_specs:
    for spec in args.color_specs.split(','):
        color, threshold, percentage = spec.split(':')
        color_specs.append((color, int(threshold), float(percentage)))

if args.input_dir:
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(args.input_dir) if os.path.splitext(f)[1] in ['.jpg', '.jpeg', '.png']]

    # Process each image file
for image_file in image_files:
        # check how many files are in the folder only 1 time, do not check again
        if image_files.index(image_file) == 0:
            images_in_folder = count_images_in_folder(args.input_dir)
            
        original_filename = os.path.splitext(os.path.basename(image_file))[0]
        large_img = Image.open(os.path.join(args.input_dir, image_file))
        large_img_path = os.path.join(args.input_dir, image_file)
        directory_path = os.path.dirname(large_img_path)

        # Print the image_file variable for debugging
        print(f"Processing image file: {image_file}")

        # Open the image file
        large_img = Image.open(os.path.join(args.input_dir, image_file))

        # Extract the base name of the image file
        base_name = os.path.basename(image_file)
        print(f"Base name: {base_name}")

        # Split the base name into name and extension
        name, extension = os.path.splitext(base_name)
        print(f"Name: {name}, Extension: {extension}")

        # Loop through rows and columns
        height = large_img.height
        width = large_img.width
        for r in range((height // desired_height) + 1):
            for c in range((width // desired_width) + 1):
                # Calculate the left, upper, right, lower pixel coordinate
                left = c * desired_width
                upper = r * desired_height
                right = (c + 1) * desired_width
                lower = (r + 1) * desired_height

                # Crop the image
                cropped_img = large_img.crop((left, upper, right, lower))

                # Save the cropped image
            filename = f'{original_filename}_cropped_{r+1}_{c+1}.jpg'
            filepath = os.path.join(args.dest, filename)
            cropped_img.save(filepath)
            # progress_bar.update(1)


# Calculate the total number of images to process
total_images = len(os.listdir(args.input_dir))

delete_images(new_folder)  # Black


progress_bar.close()

print(f'{(height // large_img.height) * (width //  large_img.width)} images have been created.')
print("Script finished executing.")
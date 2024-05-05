# Image Cropper and Cleaner

This Python script takes a large image file, crops it into 512x512 images, and then deletes the images that have a large amount of specified color space in a row. The cropped images are saved in a new folder. The idea is to remove images that have large blocks of color. When creating a style LORA, these can cause issues if you have black space or white space in your image scans.

## Usage

The script can be run from the command line with the following arguments:

- `-i`, `--image`: The path to the large image file. Example: "/home/user/Pictures/image.png"
- `-id`, `--input-dir`: The path to the directory containing image files. Example: "/home/user/Pictures/Images"
- `-d`, `--dest`: The new folder to save the cropped images. Example: "/home/user/Pictures/CroppedImages"
- `--color`: The colors to check for in hexadecimal or RGB format. Default is black (#000000). Example: "#FFFFFF" "#FF0000" or "255,255,255" "255,0,0"
- `--color_threshold`: The color threshold. If a pixel's color is above this threshold, it is considered as a color pixel. Default is 70. Example: 80
- `--color_percentage`: The percentage of color pixels in a row for an image to be considered having too much of that color. Default is 10. Example: 20
- `--color_specs`: The color specifications in the format "color,threshold,percentage". Example: "#FFFFFF,80,20" "#FF0000,70,10"
- `-bw`, `--black_white`: Check for both black and white colors.
- `-b`, `--black`: Check for black color. This is the default behavior.
- `-w`, `--white`: Check for white color.

## Example

Here is an example of how to run the script:

Quick Run:

```bash
python change_image512.py -i "./image_path.png" -d "./output/"
```

This will check do the default behavior which is black threshold of 60, blackk percentage of 10. No white check, no color check.

Advanced:

```bash
python change_image512.py -id "/home/user/Pictures/Images" -d "/home/user/Pictures/CroppedImages" --color "#FFFFFF" "#FF0000" --color_threshold 80 --color_percentage 20 --color_specs "#FFFFFF,80,20" "#FF0000,70,10" -bw
```

This will take the image at /home/user/Pictures/large_image.png, crop it into 512x512 images, save the cropped images in /home/user/Pictures/CroppedImages, and delete any images that have more than 20% of their pixels above a color threshold of 80 for the colors white and red.

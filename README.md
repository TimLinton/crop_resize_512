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
- `--height`: The desired height of the cropped images. Default is 512. Example: 768
- `--width`: The desired width of the cropped images. Default is 512. Example: 720

## Example

Here is an example of how to run the script:

Quick Run:

```bash
python change_image512.py -id "./Images" -d "./output/"
```

This will check do the default behavior which is black threshold of 60, black percentage of 10. No white check, no color check.

Advanced:

```bash
python change_image512.py -id "/home/user/Pictures/Images" -d "/home/user/Pictures/CroppedImages" --color "#FFFFFF" "#FF0000" --color_threshold 80 --color_percentage 20 --color_specs "#FFFFFF,80,20" "#FF0000,70,10" -bw --height 768 --width 720
```

This will crop the images to 768x720, check for both black and white colors, and check for the colors "#FFFFFF" and "#FF0000" with the specified thresholds and percentages. ```

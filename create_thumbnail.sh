#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
	echo "ImageMagick is required but not installed. Aborting."
	exit 1
fi

# Check if at least one image file is provided as an argument
if [ $# -eq 0 ]; then
	echo "Usage: $0 <image1> [<image2> ...]"
	exit 1
fi

# Loop through each provided image file
mogrify -auto-orient "$@"
for img_file in "$@"; do
	if [ -f "$img_file" ]; then
		# Apply auto-orientation to the image
		convert "$img_file" -resize 144x144 -density 72 -units PixelsPerInch "${img_file%.*}-th.jpg"
		echo "Processed: ${img_file}"
	else
		echo "File not found: ${img_file}"
	fi
done

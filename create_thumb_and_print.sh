#!/bin/bash

# Function to check if a command is available
command_exists() {
	command -v "$1" &> /dev/null
}

# Function to resize images and rename them
resize_and_rename() {
	local output_dir="$1"
	local size="$2"
	local density="$3"
	local suffix="$4"
	local input_file="$5"

	# Check if the output directory exists, create if not
	mkdir -p "$output_dir"

	# Resize while converting to JPG
	input_file_basename=$(basename "$input_file")
	output_file="${input_file_basename%.*}-$suffix.jpg"
	magick "$input_file" -resize "$size" -density "$density" -units PixelsPerInch -format jpg "$output_file"

	# Move the converted JPG file
	if [ -f "$output_file" ]; then
		mv "$output_file" "$output_dir"
	fi
}

# Check if ImageMagick is installed
if ! command_exists mogrify; then
	echo "ImageMagick is required but not installed. Aborting."
	exit 1
fi

# Check if at least one image file is provided as an argument
if [ $# -eq 0 ]; then
	echo "Usage: $0 <image1> [<image2> ...]"
	exit 1
fi

# Loop through each image file and resize for thumbs and print
for img_file in "$@"; do
	resize_and_rename "thumbs" "144x144" "72" "th" "$img_file"
	resize_and_rename "print" "1125x1500" "150" "150" "$img_file"
	echo "Processed: $img_file"
done

#!/bin/bash
# Applies lzw compression to an uncompressed tiff.

# just do this:
# mogrify -auto-orient -compress lzw *.tif

command_exists() {
	command -v "$1" &> /dev/null
}

if ! command_exists exiftool; then
	echo "Exiftool is required but not installed. Aborting."
	exit 1
fi

if ! command_exists convert; then
	echo "ImageMagick is required but not installed. Aborting."
	exit 1
fi

for FILE in "$@"; do
	echo $FILE
	if [ ! -f "${FILE}" ]; then 
		echo "	it not file"
		continue
	fi
	echo "	it file"
	if [[ ! $(exiftool "${FILE}" -filetype) == "File Type                       : TIFF" ]]; then
		echo "	but it not tif"
		continue
	fi
	echo "	it tif"
	if [[ ! $(exiftool "${FILE}" -compression) == "Compression                     : Uncompressed" ]]; then
		echo "	but it not uncompresed"
		continue
	fi
	echo "	it uncompresed"
	convert -auto-orient -compress lzw "${FILE}" "${FILE}"
	echo "	but it compresed nao lol"
done



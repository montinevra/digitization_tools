import argparse
import os
import re
from bs4 import BeautifulSoup

def resize_hocr(hocr_file, scaling_factor):
	with open(hocr_file, 'r', encoding='utf-8') as f:
		hocr_content = f.read()

	soup = BeautifulSoup(hocr_content, 'html.parser')

	# Find all bounding boxes
	bbox_elems = soup.find_all(class_=['ocr_page', 'ocr_carea', 'ocr_par', 'ocr_line', 'ocrx_word'])

	# Update bounding box coordinates
	for bbox_elem in bbox_elems:
		title_attr = bbox_elem['title']
		bbox_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', title_attr)
		if bbox_match:
			bbox_coords = [int(coord) for coord in bbox_match.groups()]
			updated_coords = [int(coord * scaling_factor) for coord in bbox_coords]
			updated_bbox = f'bbox {" ".join(map(str, updated_coords))}'
			updated_title = re.sub(r'bbox (\d+) (\d+) (\d+) (\d+)', updated_bbox, title_attr)
			bbox_elem['title'] = updated_title

	# Output directory for resized hOCR files
	output_dir = 'resized_hocr_files'
	os.makedirs(output_dir, exist_ok=True)

	# Extract filename from the provided path
	filename = os.path.basename(hocr_file)

	# Construct output file path
	output_file = os.path.join(output_dir, f'{filename}')

	# Write updated hOCR content to file
	with open(output_file, 'w', encoding='utf-8') as f:
		f.write(str(soup))
	
	print(f"Resized hOCR file saved to '{output_file}'.")

def main():
	parser = argparse.ArgumentParser(description='Resize bounding boxes in an hOCR file.')
	parser.add_argument('scaling_factor', type=float, help='Scaling factor for resizing the bounding boxes')
	parser.add_argument('hocr_files', metavar='hocr_file', nargs='+', help='Path to the hOCR file')
	args = parser.parse_args()

	for file in args.hocr_files:
		resize_hocr(file, args.scaling_factor)

if __name__ == '__main__':
	main()

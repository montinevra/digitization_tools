#!/usr/bin/env python3
import argparse
import os

# import re

# def extract_image_paths_from_pto(pto_file):
#     image_paths = []
#     pto_dir = os.path.dirname(pto_file)
#     with open(pto_file, 'r') as f:
#         for line in f:
#             match = re.match(r'tile-design-*.tif', line)
#             if match:
#                 filename = match.group(1)
#                 full_path = os.path.join(pto_dir, filename)
#                 image_paths.append(full_path)
#     return image_paths

# # Replace 'your_project.pto' with the path to your .pto file
# pto_file_path = 'your_project.pto'
# image_paths = extract_image_paths_from_pto(pto_file_path)

# # Print the extracted image paths
# for path in image_paths:
#     print(path)



def parse_args():
	parser = argparse.ArgumentParser(description='Script to generate a project file and perform control point detection')
	parser.add_argument('-o', dest='prefix', metavar='prefix', default='',
						help='Specify the output file prefix')
	parser.add_argument('input_files', metavar='input_file', nargs='+',
						help='Input files')

	# Checking if input files are provided
	if len(parser.parse_args().input_files) == 0:
		parser.error("No input files specified.")

	return parser.parse_args()


def main():
	args = parse_args()
	prefix = args.prefix
	input_files = tuple(args.input_files)

	# If output file is not specified, use the first input file's name without extension
	if not prefix:
		first_input_file = os.path.basename(input_files[0])
		prefix = os.path.splitext(first_input_file)[0]

	project_file = prefix + ".pto"

	commands = (
			('nona', '-m', 'TIFF_m', '-o', prefix, project_file),
			('enblend', '--save-masks', '-o', f'{prefix}-300.tif', f'{prefix}*.tif'),
	)
	for command in commands:
		os.system(' '.join(command))

	# image_paths = extract_image_paths_from_pto(project_file)
	# print(image_paths)
	# os.system(f'rm {" ".join(input_files)}')


if __name__ == "__main__":
	main()

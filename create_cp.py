#!/usr/bin/env python3
import argparse
import os
import subprocess


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

	# If output file is not specified, use the first and last input file's name
	if not prefix:
		first_input_file = os.path.basename(input_files[0])
		last_input_file = os.path.basename(input_files[-1])
		prefix = os.path.splitext(first_input_file)[0] + '-' + os.path.splitext(last_input_file)[0]
	project_file = prefix + ".pto"

	commands = (
			("pto_gen", "-o", project_file) + input_files,
			("cpfind", "--linearmatch", "-o", project_file, project_file),
	)
	for command in commands:
		sub_ret = subprocess.run(command, capture_output=True, text=True)
		# print(sub_ret.stdout)
		# print(sub_ret.stdout.split('/')[-1].strip())
		
	with open(project_file, 'r') as file:
		file_content = file.read()
	modified_content = file_content.replace('#hugin_optimizerMasterSwitch 1', '#hugin_optimizerMasterSwitch 0')
	modified_content = modified_content.replace('v p1\nv y1', 'v TrX1\nv TrY1\nv TrZ1')
	modified_content = modified_content.replace('p f2 w3000 h1500 v360', 'p f0 w3000 h3500 v60') # Rectilinear projection
	with open(project_file, 'w') as file:
		file.write(modified_content)

	print((
			f'\nNow open {project_file} in Hugin.\n'
			f'Fine-tune all points.\n'
			f'Optimize.\n'
			f'Adjust cropping.\n'
			f'Then run:\n'
			f'python3 stitch.py -o {prefix} {project_file}\n'					
	))


if __name__ == "__main__":
	main()

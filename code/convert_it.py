#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# THIS FILE IS JUST A WRAPPER FOR THE OTHERS

SUPPORTED_FORMATS=['png','jpeg','gif','tiff']

def parseargs():
	"""parse the arguments"""
	import argparse
	parser = argparse.ArgumentParser(description='Converts image files to other formats, while striving to be lossless if able', epilog="Usually via imageMagik convert")
	parser.add_argument('-o', '--out', dest='output_file', required=True, help='The output file to save.')
	parser.add_argument('-i', '--in', dest='input_file', required=True, help='The file to operate on.')
	parser.add_argument('-f', '--format', dest='output_format', required=True, choices=['png','jpeg','gif','tiff'], help='The format to use.')
	return parser.parse_args()

def convertToNewFile(theFilePath, theFilePathOut, out_format="png"):
	"""Convert the given file to the given format"""
	# map the inputs to the function blocks
	format_options = {"png" : convertToPNGFile,
        "PNG" : convertToPNGFile,
        "JPEG" : convertToJPGFile,
        "JPG" : convertToJPGFile,
        "jpeg" : convertToJPGFile,
	"jpg" : convertToJPGFile,
	"tif" : convertToTIFFFile,
	"tiff" : convertToTIFFFile,
	"gif" : convertToGIFFile }
	return format_options[out_format](theFilePath, theFilePathOut)

def convertToPNGFile(theFilePath, theFilePathOut):
	"""convert the given file to PNG"""
	try:
        	from . import convert_png
	except Exception:
        	import convert_png
	return convert_png.convertToPNGFile(theFilePath, theFilePathOut)

def convertToJPGFile(theFilePath, theFilePathOut):
	"""convert the given file to JPEG"""
	try:
        	from . import convert_jpeg
	except Exception:
        	import convert_jpeg
	return convert_jpeg.convertToJPGFile(theFilePath, theFilePathOut)

def convertToGIFFile(theFilePath, theFilePathOut):
	"""convert the given file to GIF"""
	try:
        	from . import convert_gif
	except Exception:
        	import convert_gif
	return convert_gif.convertToGIFFile(theFilePath, theFilePathOut)

def convertToTIFFFile(theFilePath, theFilePathOut):
	"""convert the given file to TIFF"""
	try:
        	from . import convert_tiff
	except Exception:
        	import convert_tiff
	return convert_tiff.convertToTIFFFile(theFilePath, theFilePathOut)

if __name__ == '__main__':
	args = parseargs()
	try:
		output_file = args.output_file
		output_format = args.output_format
		input_file = args.input_file
		if (input_file is None):
			print(str("convert_it: grumble....grumble: INPUT_FILE is set to None! Nothing to read. Nothing to do."))
			exit(3)
		if (output_file is None):
			print(str("convert_it: grumble....grumble: OUTPUT_FILE is set to None! Nothing to save. Nothing to do."))
			exit(3)
		else:
			if input_file is not None:
				convertToNewFile(input_file, output_file, str(output_format))
	except Exception:
		print(str("convert_it: REALLY BAD ERROR: ACTION will not be compleated! ABORT!"))
		exit(5)
	exit(0)

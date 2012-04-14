#! /usr/bin/env python

# RNAmazing:  CS51 Final Project


# Format for input from text file is Strand name, material, then sequence 
# each separated by a new line character


# Imports necessary python libraries
import sys
import fnmatch
import re
import string


# Checks validity of command line arguments and file to be imported
if (len(sys.argv) != 2):
	print "Usage: python master.py filename.txt"
else:
	file = sys.argv[1]
	if not(fnmatch.fnmatch(file, '*.txt')):
		print "File should be of type '.txt'"
	else:
		try:
			file = open(sys.argv[1])
		except IOError:
			print "This file could not be opened"
			sys.exit()

# imports strand name from file
strand_name = string.rstrip(string.upper(file.readline()))
print "Strand Name:  " + strand_name

# imports and checks material from text file
material = string.rstrip(string.upper(file.readline()))
if (material != "DNA") & (material != "RNA"):
	print "ERROR:  Material must be of type DNA or RNA"
	sys.exit()
else:
	print "Material:  " + material

# imports and checks sequence from text file
sequence = string.rstrip(string.upper(file.readline()))
if material == "DNA":
	for c in sequence:
		if (c != 'A') & (c != 'T') & (c != 'C') & (c != 'G'):
			print "ERROR:  DNA sequences can only consist of A, T, C, & G"
			sys.exit()
if material == "RNA":
	for c in sequence:
		if (c != 'A') & (c != 'U') & (c != 'C') & (c != 'G'):
			print "ERROR:  RNA sequences can only consist of A, U, C, & G"
			sys.exit()
print "Sequence:  " + sequence

file.close()
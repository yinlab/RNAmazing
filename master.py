#! /usr/bin/env python

# RNAmazing:  CS51 Final Project

# Format for input from text file is {strand name;material;sequence} 
# with each strand separated by a new line character


# imports necessary python libraries
import sys
import fnmatch
import re
import string

# imports .py files we have created
import classes
import prediction
import visualization

# checks validity of command line arguments and file to be imported
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

# initializes a list for strand objects
strands_list = []

# iterates over all strands in file
# strands are of type {name;material;sequence} separated by new lines
for line in file:

	# re-formats and checks the input
	strand = string.rstrip(string.upper(line))
	strand_length = len(strand)
	if (strand[0] != '{') | (strand[strand_length-1] != '}'):
		print "ERROR:  Format for strands is {name;material;sequence}"
		sys.exit()
	strand = string.rstrip(string.lstrip(string.rstrip(string.upper(line)),'{'),'}')
	
	# initializes variables to read in the strand
	strand_name = ""
	string_counter = 0
	# accounts for the fact that we just removed two elements from strand
	strand_length = strand_length-2
	
	# isolates strand name
	for i in range(0, strand_length):
		if (strand[i] != ';'):
			strand_name += strand[i]
			string_counter += 1
		else:
			string_counter += 1
			break
	print "Strand name:  " + strand_name

	# catches if there is an error in formatting
	if string_counter == strand_length:
		print "ERROR:  Format for strands is {name;material;sequence}"
		sys.exit()
	
	# isolates and validates material
	material = ""
	for i in range(string_counter, strand_length):
		if (strand[i] != ';'):
			material += strand[i]
			string_counter += 1
		else:
			string_counter += 1
			break
	material = string.upper(material)
	if (material != "DNA") & (material != "RNA"):
		print "ERROR:  Material must be of type DNA or RNA"
		sys.exit()
	else:
		print "Material:  " + material

	# catches if there is an error in formatting
	if string_counter == strand_length:
		print "ERROR:  Format for strands is {name;material;sequence}"
		sys.exit()

	# isolates and validates sequence
	sequence = ""
	if material == "DNA":
		for i in range(string_counter, strand_length):
			c = strand[i]
			if (c == '}'):
				print "ERROR:  Format for strands is {name;material;sequence}"
				sys.exit()
			if (c != 'A') & (c != 'T') & (c != 'C') & (c != 'G'):
				print "ERROR:  DNA sequences can only consist of A, T, C, & G"
				sys.exit()
			# catches the case when someone didn't put a new line between successive strands

			sequence += c
	if material == "RNA":
		for i in range(string_counter, strand_length):
			c = strand[i]
			if (c != 'A') & (c != 'U') & (c != 'C') & (c != 'G'):
				print "ERROR:  RNA sequences can only consist of A, U, C, & G"
				sys.exit()
			else:
				sequence += c
	sequence = string.upper(sequence)
	print "Sequence:  " + sequence 
	
	# generates a strand object of the input and adds it to strand list
	strand_obj = classes.Strand(material, strand_name, sequence)
	strands_list.append(strand_obj)	
file.close()

# test of creating single permutation
print "Testing single permutation..."
first_permutation = classes.Permutation(strands_list)
print first_permutation.get_concatamer("")

# test of creating permutation list
print "Testing multiple permutations..."
multiple_permutations = classes.Permutations(strands_list)

# testing Nussinov prediction
print "Testing Nussinov prediction algorithm..."

# creates a list of all possible nussinov structures
list_of_nussinov_structures = []

# iterates over all possible permutations, printing tests along the way
for element in multiple_permutations.permutations():
	print "Permutation: "+element.get_name()
	print element.get_concatamer("")
	nussinov = prediction.NussinovPredictor(element,None)
	nussinov.predict_structure()
	list_of_nussinov_structures.append(nussinov.to_structure())
	print (nussinov.to_structure()).get_pairs()

# determining best case scenario of the multiple permutations
def len_fun(x):
	return len(x.get_pairs())
list_of_nussinov_scores = map(len_fun, list_of_nussinov_structures)
index_of_best = list_of_nussinov_scores.index(max(list_of_nussinov_scores))
best_nussinov = list_of_nussinov_structures.pop(index_of_best)

# generates variables to represent the secondary structure and sequence of output
sstr = best_nussinov.get_pairs()
seq = best_nussinov.get_sequence()

print "Best structure..."
print "Pair list: "
print sstr
print "Sequence: " + seq

for i in range (1,5):
	print i


# pass output to visualization module
vis = visualization.Visualize()
print "In dot-paren notation: " 
print vis.viz_bracket(sstr, seq)
vis.viz_circle(sstr, seq)







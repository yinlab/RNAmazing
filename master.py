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
#import visualization

# checks validity of command line arguments and file to be imported
if (len(sys.argv) != 3):
	print "Usage: python master.py filename.txt visualization"
	sys.exit()
else:
	file = sys.argv[1]
	third_arg = string.upper(sys.argv[2])
	if (third_arg != "CIRCLE") & (third_arg != "DOTPAREN") & (third_arg != "ARC"):
		print "Usage: possible visualization types include DOTPAREN CIRCLE ARC"
		sys.exit()
	if not(fnmatch.fnmatch(file, '*.txt')):
		print "File should be of type '.txt'"
		sys.exit()
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

# creates a list of all possible nussinov structures and score matrices
list_of_nussinov_structures = []
list_of_nussinov_matrices = []

# iterates over all possible permutations, printing tests along the way
for element in multiple_permutations.permutations():
	print "Permutation: "+element.get_name()
	print element.get_concatamer("")
	nussinov = prediction.NussinovPredictor(element,None)
	nussinov.predict_structure()
	list_of_nussinov_structures.append(nussinov.to_structure())
	list_of_nussinov_matrices.append(nussinov.to_score_matrix())
	print (nussinov.to_structure()).get_pairs()

# determining best case scenario of the multiple permutations
def len_fun(x):
	return len(x.get_pairs())
list_of_nussinov_scores = map(len_fun, list_of_nussinov_structures)
index_of_best = list_of_nussinov_scores.index(max(list_of_nussinov_scores))
best_nussinov = list_of_nussinov_structures.pop(index_of_best)

best_nussinov_score_matrix = list_of_nussinov_matrices[index_of_best]

# generates variables to represent the secondary structure and sequence of output
sstr = best_nussinov.get_pairs()
seq = best_nussinov.get_sequence()

print "Best structure..."
print "Pair list: "
print sstr
print "Sequence: " + seq


# Testing simple substitutions for real-time recalculations
print "Testing simple substitutions..."
print "Original sequence:  " + seq


# gets permutation object from structure object and overall index of the change
#best_perm = best_nussinov.get_permutation()
#(sub_perm, index) = best_perm.simple_transformation("strand1", 2, 'a')
#new_seq = sub_perm.get_concatamer()
#print "New sequence:  " + new_seq
#print "Overall index: " 
#print index

best_perm = best_nussinov.get_permutation()
new_struct = prediction.Recalculation(best_nussinov_score_matrix, best_perm, "strand1", 2, 'a')
new_struct.predict_structure()
print (new_struct.to_structure()).get_pairs()


# pass output to visualization module
##visualization_type = string.upper(sys.argv[2])
##vis = visualization.Visualize()
##if visualization_type == "DOTPAREN":
##	print "In dot-paren notation: " 
##	print vis.viz_bracket(sstr, seq)
##elif visualization_type == "CIRCLE":
##	vis.viz_circle(sstr, seq)
##elif visualization_type == "ARC":
##	vis.viz_arc(sstr, seq)


#./master.py fsdfas
##def main():
	
##if __name__ == '__main__':
##	main()



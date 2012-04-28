#! /usr/bin/env python

# RNAmazing:  CS51 Final Project

# imports necessary python libraries
import sys
import fnmatch
import re
import string

# imports .py files we have created
import classes
import prediction
import visualization


# checks validity of command line arguments
def cmdline_validation():
	if (len(sys.argv) != 4):
		print "Usage: python master.py filename.txt visualization algorithm"
		sys.exit()
	else:
		file = sys.argv[1]
		third_arg = string.upper(sys.argv[2])
		fourth_arg = string.upper(sys.argv[3])
		if (third_arg != "CIRCLE") & (third_arg != "DOTPAREN") & (third_arg != "ARC"):
			print "Usage: possible visualization types include DOTPAREN CIRCLE ARC"
			sys.exit()
		if (fourth_arg != "NUSSINOV") & (fourth_arg != "ZUKER"):
			print "Usage: possible algorithm types include NUSSINOV ZUKER"
			sys.exit()
		if not(fnmatch.fnmatch(file, '*.txt')):
			print "File should be of type '.txt'"
			sys.exit()

# checks validity of input file format, and returns a Permutations object
def import_from_file():
	
	# tries to open file
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

		# catches if two strings have the same name
		def name_check(x): return (x.name == strand_name)
		if filter(name_check, strands_list) != []:
			print "ERROR:  No two strands can have the same name"
			sys.exit()
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
	
		# generates a strand object of the input and adds it to strand list, and generates
		# Permutations object
		strand_obj = classes.Strand(material, strand_name, sequence)
		strands_list.append(strand_obj)	
		multiple_permutations = classes.Permutations(strands_list)
		return multiple_permutations
	file.close()


def nussinov_algorithm(multiple_permutations):
	# prints all possible permutations
	print "Testing multiple permutations with Nussinov Algorithm..."

	# creates a list of all possible nussinov structures and score matrices
	list_of_nussinov_structures = []
	list_of_nussinov_matrices = []
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

	# pass output to visualization module
	visualization_type = string.upper(sys.argv[2])
	vis = visualization.Visualize()
	if visualization_type == "DOTPAREN":
		print "In dot-paren notation: " 
		print vis.viz_bracket(sstr, seq)
	elif visualization_type == "CIRCLE":
		vis.viz_circle(sstr, seq)
	elif visualization_type == "ARC":
		vis.viz_arc(sstr, seq)


	while True:

		# gets user input for any updates
		option = "q"
		while (option != "y") & (option != "n"):
			option = raw_input("Would you like to make an update to your structure? [y/n]: ")
		else:
			if option == "y":
				strand_name = raw_input("Which strand would you like to update?  ")
				strand_index = (raw_input("Which zero-indexed base on this strand would you like to modify?  "))
				new_base = raw_input("What base would you like to modify " + strand_name + "[" + strand_index + "] to?  " )
				strand_index = int(strand_index)
			elif option == "n":
				sys.exit()

		# re-initializes empty lists
		list_of_nussinov_structures = []
		list_of_nussinov_matrices = []

		for element in multiple_permutations.permutations():
			# sets up environment for real-time recalculation
			#best_perm = best_nussinov.get_permutation()
			new_struct = prediction.Recalculation(best_nussinov_score_matrix, element, strand_name, strand_index, new_base)
			new_struct.predict_structure()
			list_of_nussinov_structures.append(new_struct.to_structure())
			list_of_nussinov_matrices.append(new_struct.to_score_matrix())
			print "Permutation: "+ element.get_name()
			print element.get_concatamer("")
			print (new_struct.to_structure()).get_pairs()
			print len((new_struct.to_structure()).get_pairs())

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

		# pass output to visualization module
		visualization_type = string.upper(sys.argv[2])
		vis = visualization.Visualize()
		if visualization_type == "DOTPAREN":
			print "In dot-paren notation: " 
			print vis.viz_bracket(sstr, seq)
		elif visualization_type == "CIRCLE":
			vis.viz_circle(sstr, seq)
		elif visualization_type == "ARC":
			vis.viz_arc(sstr, seq)

	else:
		sys.exit()

def zuker_algorithm():
	print "coming soon.."
	



#./master.py filename.txt visualization algorithm
def main():
	cmdline_validation()
	if (string.upper(sys.argv[3]) == "NUSSINOV"):
		nussinov_algorithm(	import_from_file() )
	elif (string.upper(sys.argv[3]) == "ZUKER"):
		zuker_algorithm( import_from_file() )
	
if __name__ == '__main__':
	main()



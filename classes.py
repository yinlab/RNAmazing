import itertools
import sys
import classes

class Strand:

	def __init__ (self, material, name, sequence):
		"""
		specifies whether DNA or RNA, gives name, and gives sequence
		and checks self.correct_type(sequence)
		"""
		self.material = material
		self.name = name
		self.sequence = sequence
		pass
	
	
	def correct_type (self, sequence):
		"""
		iteratively check if all letters in list are a, t (or u), c, or g, making sure to check materia
		"""
		pass	
	
	

class StrandDict:
	"""implements StrandDict using built in dict type where keys are names of strands and members are lists of characters (A,T,C,G) if DNA or (A,U,C,G) if RNA"""
	
	def __init__ (self):
		"""
		initializes an empty dict 
		strand_dict = dict([])
		"""
		pass

	def add (self, strand):
		""" 
		add sequence as a named strand to the dict, given that name not already used
		if !(self.does_exist(name)) then 
		self.dict.add .....
		"""
		pass 

	def remove (self, strand):
		"""
		search through list of strands and remove instance of strand
		self.dict 
		"""
		pass
		
	def does_exist (self, name):
		"""
		checks if a strand with this name already exist before implementing it as a dict
		self.dict.(name in strand_dict)
		"""
		pass

	def num_strands(self):
		""" 
		outputs number of strands in dict, using built in dict implementation 
		self.dict.len(strand_dict)
		"""
		pass
		
	def sequence (self, strand):
		"""
		iteratively check for instance of name and print its sequence
		"""
		pass
	
	def members (self):
		"""
		print names of all strands in dict using dict implementation
		"""
		pass


class Permutations:
	""" can be implemented as another dict or set """

	# so there is some redundancy in this, but it will have to do for now
	def __init__(self, list):
		self.permutation_list = itertools.permutations(list)
		self.actual_permutation_list = []
		for element in self.permutation_list:
			self.actual_permutation_list.append(classes.Permutation(element))
	
	def permutations (self):
		"""
		calculate all permutation of list
		"""
		return self.actual_permutation_list

class ScoreMatrix:
	"""2D triangular matrix containing scores of optimal substructures"""
	
	def __init__(self, i, j):
		"""
		Initializes triangular matrix with height i and width j, with zeroes 
		across the main diagonal
		"""
		# a little too clever I think
		# self.matrix = [[None] * i] * j
		self.matrix = [[None for n in range(i)] for m in range(j)]
		self.width = i
		self.height = j
	
	def get(self, i, j):
		"""Gets the element at i,j"""
		return self.matrix[i][j]
	
	def set(self, i, j, value):
		"""Updates the element at i,j with value"""
		self.matrix[i][j] = value
	
	def has(self, i, j):
		"""True if there is a value in the matrix at i,j; false otherwise"""
		return self.matrix[i][j] != None
	
	def get_width(self):
		"""Returns the j-dimension (width) of the matrix"""
		return self.width
		
	def get_height(self):
		"""Returns the i-dimension (height) of the matrix"""
		return self.height
		
	def insert(self, k):
		"""Inserts both a row and a column at k"""
		pass
	
	def remove(self, k):
		"""Removes both a row and a column at k"""
		pass

class Permutation:
	"""Represents a single circular permutation of named strands"""
	
	def __init__(self, strands):
		"""Accepts an ordered list of Strands"""
		#if(isinstance(strands, list)):
		self.strands = strands
		self.namelist = []
		self.nameconcatenation = ""
		self.seqconcatenation = ""
		#else:
		#	print "You fail"
		
	def get_names(self):
		"""Returns a list of names of the strands, in order"""
		for element in self.strands:
			self.namelist.append(element.name)
		return self.namelist
		
	# what was the purpose of this guy again?
	def get_strands(self):
		"""Returns a list of Strands, in order"""
		pass
		
	def get_concatamer(self, separator=""):
		"""
		Returns a string containing the sequences concatenated together,
		separated by an optional separator
		"""
		#return separator.join(map(lambda strand: strand.sequence, self.strands))
		for i in range(0, len(self.strands)):
			self.seqconcatenation = self.seqconcatenation + separator + (self.strands[i]).sequence
		return self.seqconcatenation
			
	def get_name(self):
		"""
		Returns the names of the strands, concatenated together; can be used 
		as a unique identifier for this Permutation within the ensemble.
		"""
		for i in range(0, len(self.strands)):
			self.nameconcatenation = self.nameconcatenation + (self.strands[i]).name
		return self.nameconcatenation
		
class Structure:
	"""Represents the secondary structure of a given strand"""
	
	def __init__(self, pairs):
		"""Builds an initial structure from a list of (int,int) tuples"""
		self.pairs = pairs
		
	def __str__(self):
		"""Prints an informal string-based representation of the structure"""
		return str(self.pairs)
		
	def get_pairs(self):
		"""Returns the structure as a list of (int,int) tuples"""
	
	def __iter__(self):
		for pair in self.pairs:
			yield pair
		pass

		
class State:
	"""
	Represents a state of the predictor which can be more quickly mutated by single-base
	substitution (and insertion and deletion)
	"""
	
	def __init__(self, pairs):
		"""Initialized the state from a list of (Permutation,ScoreMatrix) tuples"""
		pass
		
	def add(self, permutation, score_matrix):
		"""Adds an additional ScoreMatrix for a given permutation"""
		pass
	
	def remove(self, permutation):
		"""Removes the given permutation from the ensemble"""
		pass
		
	def get_permutations(self):
		"""Returns the permutations in the state"""
		pass
		
	def get_score_matrix(self, permutation):
		"""Returns the score matrix corresponding to a particular permutation"""
		pass
		
	def set_score_matrix(self, permutation):
		"""Updates the score matrix corresponding to a particular permutation"""
		pass
	
	def get_as_tuples(self):
		"""Returns list of (Permutation, ScoreMatrix) tuples, as passed to the initiator"""
		pass
		

class Transformation:
	"""
	Performs a single base transformation on an Strand
	"""
	
	def transform(self, old):
		"""
		Accepts the old Strand and returns a new one, with the transformation
		applied.
		"""

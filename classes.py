class Strand:

    def __init__ (self, material, name, sequence):
    	"""
    	specifies whether DNA or RNA, gives name, and gives sequence
    	and checks self.correct_type(sequence)
    	"""
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

	def __init__(self):
		"""
        self.perm_list = []
        """
        pass
    
	def permutations (self,list):
		"""
        calculate all permutation of list
        """
        pass

class ScoreMatrix:
	"""2D triangular matrix containing scores of optimal substructures"""
	
	def __init__(self,i,j):
		"""
		Initializes triangular matrix with height i and width j, with zeroes 
		across the main diagonal
		"""
		pass
	
	def get(self,i,j):
		"""Gets the element at i,j"""
		pass
	
	def set(self,i,j,value):
		"""Updates the element at i,j with value"""
		pass
	
	def get_width(self):
		"""Returns the j-dimension (width) of the matrix"""
		pass
		
	def get_height(self):
		"""Returns the i-dimension (height) of the matrix"""
		pass
		
	def insert(self,k):
		"""Inserts both a row and a column at k"""
		pass
	
	def remove(self,k):
		"""Removes both a row and a column at k"""
		pass

class Permutation:
	"""Represents a single circular permutation of named strands"""
	
	def __init__(self,strands):
		"""Accepts an ordered list of Strands"""
		self.strands = strands;
		pass
		
	def get_names(self):
		"""Returns a list of names of the strands, in order"""
		pass
		
	def get_strands(self):
		"""Returns a list of Strands, in order"""
		pass
		
	def get_concatamer(self,separator=""):
		"""
		Returns a string containing the sequences concatenated together,
		separated by an optinal separator
		"""
		pass
		
	def get_name(self):
		"""
		Returns the names of the strands, concatenated together; can be used 
		as a unique identifier for this Permutation within the ensemble.
		"""
		pass
	
class Structure:
	"""Represents the secondary structure of a given strand"""
	
	def __init__(self,pairs):
		"""Builds an initial structure from a list of (int,int) tuples"""
		pass
	
	def get_pairs(self):
		"""Returns the structure as a list of (int,int) tuples"""
	
	def __iter__(self):
		pass
		
	def next(self):
		pass
		
class State:
	"""
	Represents a state of the predictor which can be more quickly mutated by single-base
	substitution (and insertion and deletion)
	"""
	
	def __init__(self, pairs):
		"""Initialized the state from a list of (Permutation,ScoreMatrix) tuples"""
		pass
		
	def add(self,permutation,score_matrix):
		"""Adds an additional ScoreMatrix for a given permutation"""
		pass
	
	def remove(self,permutation):
		"""Removes the given permutation from the ensemble"""
		pass
		
	def get_permutations(self):
		"""Returns the permutations in the state"""
		pass
		
	def get_score_matrix(self,permutation):
		"""Returns the score matrix corresponding to a particular permutation"""
		pass
		
	def set_score_matrix(self,permutation):
		"""Updates the score matrix corresponding to a particular permutation"""
		pass
	
	def get_as_tuples(self):
		"""Returns list of (Permutation, ScoreMatrix) tuples, as passed to the initiator"""
		pass
		

class Transformation:
	"""
	Performs a single base transformation on an Strand
	"""
	
	def transform(self,old):
		"""
		Accepts the old Strand and returns a new one, with the transformation
		applied.
		"""

class Visualize:
	"""
	Takes structure and outputs it as visualize
	"""

	def viz_circle(self,structure):
		"""Returns bmp of circular secondary structure graph"""
		pass

	def viz_planar(self,structure):
		"""Return bmp of planar secondary structure graph"""
		pass
		
	def viz_arc(self,structure):
		"""Return bmp of arc graph"""


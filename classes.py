
class StrandDict:
    
	def __init__ (self):
        """
		self.length = 0
		self.list = []
        """
        pass
        
    def does_exist (name):
        """
        checks if a strand with this name already exist
        """
        pass
    
    def correct_type (self, sequence):
        """
        iteratively check if all letters in list are a, t, c, or g
        """
        pass        
    
    def add (self, name, sequence):
        """ 
        add sequence as a named strand to the dict, given that name not already used

        if (correct_type (sequence)) && !(self.does_exist(name)) then 
        self.list.append((name,sequence))
        self.length += 1	
        """
        pass    
        
	def remove (self, name):
		"""
        search through list of strands and remove instance of strand

        if self.length != 0 then self.length += 1 else 0
        """
        pass

	def num_strands(self):
		""" 
        outputs number of strands in dict 
        """
        pass

    def members (self):
        """
        print names of all strands in dict
        """
        pass

    def sequence (self, name):
        """
        iteratively check for instance of name and print its sequence
        """
        pass


class PermutationSet:
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
	
	def __init__(self,names,strands):
		pass
		
	def get_names(self):
		"""Returns a list of names of the strands, in order"""
		pass
		
	def get_strands(self):
		"""Returns a list of sequences, in order"""
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
		

		
		
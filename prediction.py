class AbstractSingleStrandPredictor:
	"""
	Performs a dynamic programming algorithm to predict secondary structure of 
	a single strand or concatamer
	"""
	
	def __init__(self,permutation,score_matrix):
	"""
	Initializes from a Permutation and a (possibly empty) ScoreMatrix
	"""
		pass
		
	def generate_score_matrix(self):
	"""
	Populates the score matrix
	"""
		pass
		
	def traceback(self):
	"""
	Performs the traceback function
	"""
		pass
		
	def predict_structure(self):
	"""
	Predicts the secondary structure by calling generate_score_matrix and traceback
	"""
		pass
		
class MultiStrandPredictor:
	
	@staticmethod
	def from_strands(ss_predictor_class,strand_dict):
		"""
		Generates a new MultiStrandPredictor from the StrandDict strand_dict which uses the passed 
		class ss_predictor_class as its single-stranded predictor
		"""
		# self.ss_predictor = new ss_predictor_class()
		# self.
		pass

	@staticmethod
	def from_state(ss_predictor_class,state):
		"""
		Generates a new MultiStrandPredictor from the State state which uses the passed 
		class ss_predictor_class as its single-stranded predictor
		"""
		pass
	
	def generate_permutations(self,strand_dict):
		"""
		Generates and returns a Permutations of all distinct circular permutations 
		of the Strands in strand_dict
		"""
		pass
	
	def predict_structure(self):
		"""
		Predicts the most favorable secondary structure of the ensemble of strands. Works by
		running self.ss_predictor across all permutations in self.permutations. Saves structure in
		self.prediction, and state in self.state.
		"""		
		pass
	
	def to_structure(self):
		"""
		Returns a Structure representing the optimal secondary structure calculated by 
		predict_structure
		"""
		pass
	
	def to_state(self):
		"""
		Returns a State object mapping the generated permutations to their computed score matricies
		Used for real-time recalculation.
		"""
		pass


	
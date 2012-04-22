from classes import * 

class AbstractSingleStrandPredictor:
	"""
	Performs a dynamic programming algorithm to predict secondary structure of 
	a single strand or concatamer
	"""
	
	def __init__(self,permutation,score_matrix):
		"""
		Initializes from a Permutation and a (possibly empty) ScoreMatrix
		"""
		self.permutation = permutation
		self.score_matrix = score_matrix
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
		
	def to_structure(self):
		"""
		Returns the predicted secondary structure calculated by #predict_structure
		"""
		pass
		
	def to_score_matrix(self):
		"""
		Returns the score matrix g enerated by #predict_structure
		"""
		pass
		
		
class NussinovPredictor(AbstractSingleStrandPredictor):
	"""
	Implements Nussinov's dynamic programming algorithm for predicting 
	secondary structure by maximizing the number of paired bases.
	"""
	
	def __init__(self,permutation,score_matrix=None):
		"""
		Initializes from a Permutation and a (possibly empty) ScoreMatrix
		"""
		self.permutation = permutation
		if(score_matrix == None):
			(seq,l) = self.get_sequence()
			score_matrix = ScoreMatrix(l,l)
		
		self.score_matrix = score_matrix
		pass
		
	def get_sequence(self):
		self.seq = self.permutation.get_concatamer()
		return (self.seq, len(self.seq))
	
	def delta(self,ni, nj):
		pair = set([ni,nj])
		if pair == set(['A','T']): return 1
		elif pair == set(['C','G']): return 1
		elif pair == set(['G','T']): return 0.5
		else: return 0
	
	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		(seq, l) = self.get_sequence()
		
		# populate main diagonal of score matrix with zeroes
		self.score_matrix.set(0,0,0)
		for i in range(1,l):
			self.score_matrix.set(i,i,0)
			self.score_matrix.set(i,i-1,0)
		
		
		def delta(i, j):
			return self.delta(seq[i], seq[j])
			
		
		
		# I don't really know how self-binding happens in python...
		#score_matrix = self.score_matrix
		
		def gamma(i,j):
			if(self.score_matrix.has(i,j)): return self.score_matrix.get(i,j) 
			return max(gamma(i+1,j),
				gamma(i,j-1),
				gamma(i+1,j-1)+delta(i,j),
				max(map(lambda k: gamma(i,k) + gamma(k+1, j), range(i,j))))
		
		for n in range(1,l):
			for j in range(n,l):
				#i = j - n + 1
				i = j - n
				self.score_matrix.set(i,j,gamma(i,j))
		
	def traceback(self):
		"""
		Performs the traceback function
		"""
		(seq, l) = self.get_sequence()
		
		def gamma(i,j):
			return self.score_matrix.get(i,j)
			
		def delta(i, j):
			return self.delta(seq[i], seq[j])

			
		pairs = []
		
		def trace(i,j):
			if i<j:
				if gamma(i,j) == gamma(i+1, j):
					trace(i+1,j)
				elif gamma(i,j) == gamma(i,j-1):
					trace(i,j-1)
				elif gamma(i,j) == gamma(i+1, j-1) + delta(i,j):
					pairs.append((i,j))
					trace(i+1,j-1)
				else:
					for k in range(i+1, j-1):
						if gamma(i,j) == gamma(i,k)+gamma(k+1,j):
							trace(i,k)
							trace(k+1,j)
		
		trace(0,self.score_matrix.get_width()-1)
		self.pairs = Structure(pairs, self.seq)
		return self.pairs
		
	def predict_structure(self):
		"""
		Predicts the secondary structure by calling generate_score_matrix and traceback
		"""
		self.generate_score_matrix()
		self.traceback()
		
	def to_structure(self):
		"""
		Returns the predicted secondary structure calculated by #predict_structure
		"""
		return self.pairs
		
	def to_score_matrix(self):
		"""
		Returns the score matrix g enerated by #predict_structure
		"""
		return self.score_matrix
		
		
		
class MultiStrandPredictor:
	
	def __init__(self):
		pass
	
	@staticmethod
	def from_strands(ss_predictor_class,strand_dict):
		"""
		Generates a new MultiStrandPredictor from the StrandDict strand_dict which uses the passed 
		class ss_predictor_class as its single-stranded predictor
		"""
		self = MultiStrandPredictor()
		permutations = self.generate_permutations(strand_dict)
		self.ss_predictor = ss_predictor_class()
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


	
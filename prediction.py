from classes import * 
import string

class AbstractSingleStrandPredictor:
	"""
	Performs a dynamic programming algorithm to predict secondary structure of 
	a single strand or concatamer
	"""
	
	def __init__(self, permutation, score_matrix):
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
	
	def __init__(self, permutation, score_matrix=None):
		"""
		Initializes from a Permutation and a (possibly empty) ScoreMatrix
		"""
		self.permutation = permutation
		if(score_matrix == None):
			(seq, l) = self.get_sequence()
			score_matrix = ScoreMatrix(l, l)
		
		self.score_matrix = score_matrix
		pass
		
	def get_sequence(self):
		self.seq = self.permutation.get_concatamer()
		return (self.seq, len(self.seq))
	
	def delta(self, ni, nj):
		pair = set([ni, nj])
		if (pair == set(['A', 'T'])) | (pair == set(['A', 'U'])): return 1
		elif pair == set(['C', 'G']): return 1
		elif (pair == set(['G', 'T'])) | (pair == set(['G', 'U'])): return 1
		else: return 0
	
	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		(seq, l) = self.get_sequence()
		
		# populate main diagonal of score matrix with zeroes
		self.score_matrix.set(0, 0, 0)
		for i in range(1, l):
			self.score_matrix.set(i, i, 0)
			self.score_matrix.set(i, i - 1, 0)
		
		
		def delta(i, j):
			if self.delta(seq[i], seq[j]) != 0:
				return self.delta(seq[i], seq[j])
			else:
				return 0
			
		
		def gamma(i, j):
			if(self.score_matrix.has(i, j)): return self.score_matrix.get(i, j) 
			return max(gamma(i + 1, j),
				gamma(i, j - 1),
				gamma(i + 1, j - 1) + delta(i, j),
#				max([gamma(i, k) + gamma(k + 1, j) for k in range(i+1, j)] if (i+1!=j)  else [0])
				max([gamma(i, k) + gamma(k + 1, j) for k in range(i, j)])

			)
		
		for n in range(1, l):
			for j in range(n, l):
				#i = j - n + 1
				i = j - n
				self.score_matrix.set(i, j, gamma(i, j))

		
	def traceback(self):
		"""
		Performs the traceback function
		"""
		(seq, l) = self.get_sequence()
		
		def gamma(i, j):
			return self.score_matrix.get(i, j)
			
		def delta(i, j):
			return self.delta(seq[i], seq[j])

			
		pairs = []
		
		def trace(i, j):
			if i < j:
				if gamma(i, j) == gamma(i + 1, j):
					trace(i + 1, j)
				elif gamma(i, j) == gamma(i, j - 1):
					trace(i, j - 1)
				elif gamma(i, j) == gamma(i + 1, j - 1) + delta(i, j):
					pairs.append((i, j))
					trace(i + 1, j - 1)
				else:
					for k in range(i + 1, j - 1):
						if gamma(i, j) == gamma(i, k) + gamma(k + 1, j):
							trace(i, k)
							trace(k + 1, j)
							break

		trace(0, self.score_matrix.get_width() - 1)
		
		#self.pairs = Structure(pairs, self.seq)
		self.pairs = pairs
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
		self.structure_obj = Structure(self.pairs, self.permutation)
		return self.structure_obj
		
	def to_score_matrix(self):
		"""
		Returns the score matrix g enerated by #predict_structure
		"""
		return self.score_matrix


class Recalculation:
	def __init__(self, scorematrix, base, permutation):
		"""
		Implements real-time recalculation of Nussinov predictor for simple substitutions, taking
		in the original scorematrix, the number of the base being updated, and the permutation
		to which we are performing the update
		"""
		self.score_matrix = scorematrix
		self.change_index = base
		
	
	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		# need to make this get new sequence
		(seq, l) = self.get_sequence()
		
		def delta(i, j):
			if self.delta(seq[i], seq[j]) != 0:
				return self.delta(seq[i], seq[j])
			else:
				return 0

		def gamma(i, j):
			#if(self.score_matrix.has(i, j)): return self.score_matrix.get(i, j) 
			return max(gamma(i + 1, j),
				gamma(i, j - 1),
				gamma(i + 1, j - 1) + delta(i, j),
#				max([gamma(i, k) + gamma(k + 1, j) for k in range(i+1, j)] if (i+1!=j)  else [0])
				max([gamma(i, k) + gamma(k + 1, j) for k in range(i, j)])
			)

		for n in range(self.change_index + 1, l):
			for j in range(n, l):
				i = j - n
				self.score_matrix.set(i, j, gamma(i, j))

	def traceback(self):
		"""
		Performs the traceback function
		"""
		(seq, l) = self.get_sequence()
		
		def gamma(i, j):
			return self.score_matrix.get(i, j)
			
		def delta(i, j):
			return self.delta(seq[i], seq[j])

			
		pairs = []
		
		def trace(i, j):
			if i < j:
				if gamma(i, j) == gamma(i + 1, j):
					trace(i + 1, j)
				elif gamma(i, j) == gamma(i, j - 1):
					trace(i, j - 1)
				elif gamma(i, j) == gamma(i + 1, j - 1) + delta(i, j):
					pairs.append((i, j))
					trace(i + 1, j - 1)
				else:
					for k in range(i + 1, j - 1):
						if gamma(i, j) == gamma(i, k) + gamma(k + 1, j):
							trace(i, k)
							trace(k + 1, j)
							break

		trace(0, self.score_matrix.get_width() - 1)
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




class ZukerPredictor(AbstractSingleStrandPredictor):
	"""
	Implements Nussinov's dynamic programming algorithm for predicting 
	secondary structure by maximizing the number of paired bases.
	"""
	
	def __init__(self, permutation, score_matrix=None):
		"""
		Initializes from a Permutation and a (possibly empty) ScoreMatrix
		"""
		self.permutation = permutation
		(seq, l) = self.get_sequence()

		if(score_matrix == None):
			score_matrix = ScoreMatrix(l, l)
		
		
		self.score_matrix_v = ScoreMatrix(l,l)
		self.score_matrix = score_matrix
		pass
		
	def get_sequence(self):
		seq = self.permutation.get_concatamer()
		return (seq, len(seq))
	
	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		(seq, l) = self.get_sequence()
		
		loop_energies = [None, 						# 0
						[None,	3.9,	None],	# 1
						[4.1,	3.1,	None],	# 2
						[5.1,	3.5,	4.1],	# 3
						[4.9,	4.2,	4.9],	# 4
						[5.3,	4.8,	4.4],	# 5
						[6.3,	5.5,	5.3],	# 10
						[6.7,	6.0,	5.8],	# 15
						[7.0,	6.3,	6.1],	# 20
						[7.2,	6.5,	6.3],	# 25
						[7.4,	6.7,	6.5],	# 30
					]
		
		stack_energies = {
						"AU": {
							"AU": -0.9, "CG": -1.8, "GC": -2.3, "UA": -1.1, "GU": -1.1, "UG": -0.8,
						}, "CG": {
							"AU": -1.7, "CG": -2.9, "GC": -3.4, "UA": -2.3, "GU": -2.1, "UG": -1.4,
						}, "GC": {
							"AU": -2.1, "CG": -2.0, "GC": -2.9, "UA": -1.8, "GU": -1.9, "UG": -1.2,
						}, "UA": {
							"AU": -0.9, "CG": -1.7, "GC": -2.1, "UA": -0.9, "GU": -1.0, "UG": -0.5,
						}, "GU": {
							"AU": -0.5, "CG": -1.2, "GC": -1.4, "UA": -0.8, "GU": -0.4, "UG": -0.2,
						}, "UG": {
							"AU": -1.0, "CG": -1.9, "GC": -2.1, "UA": -1.1, "GU": -1.5, "UG": -0.4,
						}
		}
		
		# k = 1 -> hairpin
		# k = 2 -> bulge
		# k = 3 -> internal loop
		def loop_energy(k,size):
			if size > 5: size = round(size/5)*5
			return loop_energies[size,3-k]
		
		def stack_energy(i,j,ip,jp):
			return stack_energies[base(i)+base(j)][base(ip)+base(jp)]
			
		def base(k):
			return seq[k]
		
		def loop_size(i,j,ip,jp):
			# TODO: add absolute value?
			max(ip-i,j-jp)
		
		def V(i, j):
			if(self.v_score_matrix.has(i, j)):
				return self.v_score_matrix.get(i, j)
			else:
				return min(eh(i, j),
						es(i, j) + V(i + 1, j - 1),
						VBI(i, j),
						VM(i, j))
		
		def W(i, j):
			if(self.score_matrix.has(i, j)):
				self.score_matrix.get(i, j)
			else:
				return min(W(i + 1, j),
						W(i, j - 1),
						V(i, j),
						min([W(i, k) + W(k + 1, j) for k in range(i, j)]))

		def VBI(i, j):
			min([ebi(i, j, ip, jp) + V(ip, jp) for ip in range(i, j) for jp in range(ip, j) if ip - i + j - jp > 2])
			
		def VM(i, j):
			min(W(i + 1, k) + W(k + 1, j - 1) for k in range(i, j - 1)) + a
			
		a = 5
		
		def eh(i, j):
			return loop_energy(1,abs(i-j))
		
		def es(i, j):
			return stack_energy(i,j,i+1,j-1)
		
		def ebi(i, j, ip, jp):
			[min_ij, max_ij] = [ip-i,j-jp].sort()
			
			# if on one side the closing and the accessible bases are adjacent, it's
			# a bulge loop (2), else it's an internal loop (3)
			loop_type = 2 if min_ij == 1 else 3 
			loop_size = max_ij
			return loop_energy(loop_type, loop_size)
		

				
		# populate main diagonal of score matrix with zeroes
		self.score_matrix.set(0, 0, 0)
		for j in range(4, l):
			for i in range(j - 4, j):
				self.score_matrix.set(i, j, float("inf"))
				self.score_matrix_v.set(i, j, float("inf")) 		
		
		for i in range(1, l):
			for j in range(i, l):
				self.score_matrix.set(i, j, W(i, j))
				self.score_matrix_v.set(i, j, V(i, j))
		
	def traceback(self):
		"""
		Performs the traceback function
		"""
		(seq, l) = self.get_sequence()
		
		def gamma(i, j):
			return self.score_matrix.get(i, j)
			
		def delta(i, j):
			return self.delta(seq[i], seq[j])

			
		pairs = []
		
		def trace(i, j):
			if i < j:
				if gamma(i, j) == gamma(i + 1, j):
					trace(i + 1, j)
				elif gamma(i, j) == gamma(i, j - 1):
					trace(i, j - 1)
				elif gamma(i, j) == gamma(i + 1, j - 1) + delta(i, j):
					pairs.append((i, j))
					trace(i + 1, j - 1)
				else:
					for k in range(i + 1, j - 1):
						if gamma(i, j) == gamma(i, k) + gamma(k + 1, j):
							trace(i, k)
							trace(k + 1, j)
		
		trace(0, self.score_matrix.get_width() - 1)
		self.pairs = Structure(pairs)
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
	def from_strands(ss_predictor_class, strand_dict):
		"""
		Generates a new MultiStrandPredictor from the StrandDict strand_dict which uses the passed 
		class ss_predictor_class as its single-stranded predictor
		"""
		self = MultiStrandPredictor()
		permutations = self.generate_permutations(strand_dict)
		self.ss_predictor = ss_predictor_class()
		pass

	@staticmethod
	def from_state(ss_predictor_class, state):
		"""
		Generates a new MultiStrandPredictor from the State state which uses the passed 
		class ss_predictor_class as its single-stranded predictor
		"""
		pass
	
	def generate_permutations(self, strand_dict):
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


	

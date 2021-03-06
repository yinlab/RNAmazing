from classes import *
import string
import csv
import sys

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

	def get_sequence(self):
		self.seq = self.permutation.get_concatamer()
		return (self.seq, len(self.seq))	

	def update(self,strand_name,index,base,old_score_matrix=None):
		"""
		Updates the predictor to allow generate_score_matrix to be called 
		again, partially recalculating the matrix
		"""
		if(old_score_matrix != None): 
			self.old_score_matrix = old_score_matrix
		else:
			self.old_score_matrix = self.score_matrix
		
		l = len(self.permutation.get_concatamer())
		self.score_matrix = ScoreMatrix(l,l)
		(self.permutation, self.change_index) = self.permutation.substitution(strand_name,index,base)
		self.update_score_matrix(l)
		
	def update_score_matrix(self,width):
		"""
		Updates the score matrix to reflect recalculation; called by #update
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
		Returns the score matrix generated by #predict_structure
		"""
		return self.score_matrix

	def print_matrix(self,matrix=None):
		if(matrix == None):
			matrix = self.score_matrix
		self.score_matrix.print_matrix()
		
		
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
		
	def get_sequence(self):
		self.seq = self.permutation.get_concatamer()
		return (self.seq, len(self.seq))
	
	def delta(self, ni, nj):
		pair = set([ni, nj])
		if (pair == set(['A', 'T'])) | (pair == set(['A', 'U'])): return 1
		elif pair == set(['C', 'G']): return 1
		elif (pair == set(['G', 'T'])) | (pair == set(['G', 'U'])): return 1
		else: return 0
		
	def update_score_matrix(self,l):
		for i in range(0, self.change_index):
			for j in range(i, self.change_index):
				if j < l:
					self.score_matrix.set(i, j, self.old_score_matrix.get(i,j))		

	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		(seq, l) = self.get_sequence()
		
		# populate score matrix with old values
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
				max([gamma(i, k) + gamma(k + 1, j) for k in range(i, j)])
			)

		
		for n in range(1, l):
			for j in range(n, l):
				#i = j - n + 1
				i = j - n
				self.score_matrix.set(i, j, gamma(i, j))
				

#		for n in range(self.change_index + 1, l):
#			for j in range(n, l):
#				i = j - n
#				self.score_matrix.set(i, j, gamma(i, j))

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
		self.pairs = pairs
		return self.pairs
	


class Recalculation(NussinovPredictor):
	def __init__(self, scorematrix, original_permutation, strand_name, index, base):
		"""
		Implements real-time recalculation of Nussinov predictor for simple substitutions, taking
		in the original scorematrix, the number of the base being updated, and the permutation
		to which we are performing the update
		"""
		self.permutation = original_permutation
		self.update(strand_name, index, base, scorematrix)
	
	def as_permutations(self):
		return 
		

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
		
		
	def update(self):
		raise "Unimplemented for Zuker model"
	
	def generate_score_matrix(self):
		"""
		Populates the score matrix
		"""
		(seq, l) = self.get_sequence()
		
		# Energies of various types of loop
		# loop_energies[n][0] -> Energy of internal loop of size n
		# loop_energies[n][1] -> Energy of bulge loop of size n
		# loop_energies[n][2] -> Energy of hairpin loop of size n
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
		
		# Energies for coaxial stacks between each type of base pair
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
		
		# Constant multiloop penalty
		a = 5
		
		# Returns the loop energy of a k-loop with the given size
		# k = 1 -> hairpin
		# k = 2 -> bulge
		# k = 3 -> internal loop
		def loop_energy(k,size):
			if size > 5: 
				size = int(round(size/5))
				if size > 10: 
					size = 10
			energy = loop_energies[size][3-k]
			if energy == None:
				return 0
			else:
				return energy
		
		# Returns the stacking energy for base between i,j and ip, jp 
		def stack_energy(i,j,ip,jp):
			key = "".join([base(i),base(j)])
			keyp = "".join([base(ip),base(jp)])
			if (key in stack_energies) and (keyp in stack_energies[key]):
				return stack_energies[key][keyp]
			else:
				return 0
			
		def base(k):
			return seq[k] if seq[k]!='T' else 'U'
		
		# Returns the size of a loop enclosed by i,j with ip, jp accessible
		def loop_size(i,j,ip,jp):
			return max(abs(ip-i),abs(j-jp))
			
		# Hairpin energy
		def eh(i, j):
			return loop_energy(1,abs(i-j))
		
		# Stacking energy
		def es(i, j):
			return stack_energy(i,j,i+1,j-1)
		
		# Bulge/internal loop energy
		def ebi(i, j, ip, jp):
			[min_ij, max_ij] = sorted([ip-i,j-jp])
			
			# if on one side the closing and the accessible bases are adjacent, it's
			# a bulge loop (2), else it's an internal loop (3)
			loop_type = 2 if min_ij == 1 else 3 
			loop_size = max_ij
			return loop_energy(loop_type, loop_size)
		
		# V values for bulge/internal loop(s)
		def VBI(i, j):
			return min([ebi(i, j, ip, jp) + V(ip, jp) for ip in range(i, j) for jp in range(ip, j) if ip - i + j - jp > 2])
					
		# V values for multiloops
		def VM(i, j):
			return min(W(i + 1, k) + W(k + 1, j - 1) for k in range(i, j - 1)) + a
		
		# V matrix represents the optimal substructure scores if i,j are paired to one another
		def V(i, j):
			if(self.score_matrix_v.has(i, j)):
				return self.score_matrix_v.get(i, j)
			else:
				return min(eh(i, j),
						es(i, j) + V(i + 1, j - 1),
						VBI(i, j),
						VM(i, j))
				
		# W represents the scores of optimal substructures (analogous to gamma in Nussinov)
		def W(i, j):
			if(self.score_matrix.has(i, j)):
				return self.score_matrix.get(i, j)
			else:
				w1 = W(i + 1, j)
				w2 = W(i, j - 1)
				w3 = V(i, j)
				w4 = min([W(i, k) + W(k + 1, j) for k in range(i, j)] if (i!=j)  else [float("inf")])
				
				return min(w1, w2, w3, w4)

				
		# populate main diagonal of score matrix with zeroes
		if l < 4:
			# populate score matrix entirely with infinity
			
			for i in range(0,l):
				for j in range(0,l):
					self.score_matrix.set(i,j,float("inf"))
					self.score_matrix_v.set(i,j,float("inf"))
			pass
		
		# We want this, ultimately:
		
		# j,i->	0	1	2	3	4	5	6	7
		# 0:	oo	oo	oo	oo	
		# 1:	oo	oo	oo	oo	oo
		# 2:	oo	oo	oo	oo	oo	oo
		# 3:	oo	oo	oo	oo	oo	oo	oo	
		# 4:		oo	oo	oo	oo	oo	oo	oo
		# 5:			oo	oo	oo	oo_	oo_	oo_
		# 6:				oo	oo	oo_	oo_	oo_
		# 7:					oo	oo_	oo_	oo_
		
		# where oo = infinity
		# we'll generate all but the bottom right (the oo_) cells first...
		else:
			for n in range(l-3):
				j = n
				for i in range(n,n+4):
					self.score_matrix.set(i, j, float("inf"))
					self.score_matrix_v.set(i, j, float("inf")) 		
		
				i = n
				for j in range(n,n+4):
					self.score_matrix.set(i, j, float("inf"))
					self.score_matrix_v.set(i, j, float("inf")) 		
					
			# ...then do the bottom nine
			for i in range(l-3,l):
				for j in range(l-3,l):
					self.score_matrix.set(i, j, float("inf"))
					self.score_matrix_v.set(i, j, float("inf")) 		
		
		# Do the main thing
		for n in range(1, l):
			for j in range(n, l):
				#i = j - n + 1
				i = j - n
				self.score_matrix_v.set(i, j, V(i, j))
				self.score_matrix.set(i, j, W(i, j))
		
	def traceback(self):
		"""
		Performs the traceback function
		"""
		(seq, l) = self.get_sequence()
		
		def W(i,j):
			return self.score_matrix.get(i,j)

		def V(i,j):
			return self.score_matrix_v.get(i, j)
			
		pairs = []
		
		def trace(i, j):
			if i < j:
				if W(i, j) == W(i + 1, j):
					trace(i + 1, j)
				elif W(i, j) == W(i, j - 1):
					trace(i, j - 1)
				elif W(i, j) == V(i, j): # W(i + 1, j - 1) + V(i, j):
					pairs.append((i, j))
					trace(i + 1, j - 1)
				else:
					for k in range(i + 1, j - 1):
						if W(i, j) == W(i, k) + W(k + 1, j):
							trace(i, k)
							trace(k + 1, j)
							break
		
		trace(0, self.score_matrix.get_width() - 1)
		self.pairs = pairs
		return self.pairs

class Visualize:
	"""
	Takes structure and outputs it as visualize
	"""
	def viz_bracket(self, sstr, seq):
		"""Returns string of secondary structure in dot-bracket notation"""
		output = ""
		#fill dots
		for i in seq:
			output += "."

		#fill brackets
		for i in sstr:
			x,y = i
			output = output[:x] + "(" + output[x+1:]
			output = output[:y] + ")" + output[y+1:]
		return output

	def viz_circle(self,structure):
		"""Returns bmp of circular secondary structure graph"""
		pass

	def viz_planar(self,structure):
		"""Return bmp of planar secondary structure graph"""
		pass
		
	def viz_arc(self,structure):
		"""Return bmp of arc graph"""

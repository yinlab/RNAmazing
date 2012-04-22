class Visualize:
	"""
	Takes structure and outputs it as visualization
	"""
	def viz_bracket(self, sstr, seq):
		"""
		Returns string of secondary structure in dot-bracket notation
		"""
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

	def viz_circle(self, sstr, seq):
		"""
		Returns bmp of chord secondary structure graph
		"""
		import math
		from Tkinter import *

		# Create a Tk instance
		master = Tk()
		master.title("Chord Diagram")
		master.resizable(width = 0, height = 0)

		# Create canvas
		canvaswidth = 600
		canvasheight = 600
		w = Canvas(master, width = canvaswidth, height = canvasheight)
		w.pack()

		# Draw circle and tick marks
		w.create_oval(50, 50, 550, 550)
		angle = (2 * math.pi) / len(seq)
		r = 250
		for i in range(len(seq)):
			theta = i * angle
			x = r * math.cos(theta) + (canvaswidth / 2)
			y = r * math.sin(theta) + (canvasheight / 2)
			w.create_oval(x - 2, y - 2, x + 2, y + 2, fill = "black")

		# Draw bases
		coords = []
		for i, base in enumerate(seq):
			theta = i * angle
			r = 275
			x = r * math.cos(theta) + (canvaswidth / 2)
			y = r * math.sin(theta) + (canvasheight / 2)
			w.create_text(x, y, text = base)
			r = 250
			x2 = r * math.cos(theta) + (canvaswidth / 2)
			y2 = r * math.sin(theta) + (canvasheight / 2)
			coords.append({"x": x2, "y": y2})
			
		# Draw segments between bases
		for base1, base2 in sstr:
			w.create_line(coords[base1]["x"], coords[base1]["y"], coords[base2]["x"], coords[base2]["y"])

		# Enter main event loop
		mainloop()	
		
	def viz_planar(self,structure):
		"""Return bmp of planar secondary structure graph"""
		pass
		
	





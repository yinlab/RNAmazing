class Visualize:
	"""
	Takes structure and outputs it as visualization
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

	def viz_circle(self, sstr, seq):
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
		w.configure(background = "white")

		# Draw circle
		w.create_oval(50, 50, 550, 550)
		angle = (2 * math.pi) / len(seq)

		# Draw bases and tick marks
		coords = []
		for i, base in enumerate(seq):
			theta = i * angle
			# Draw bases
			r = 275
			x = r * math.cos(theta) + (canvaswidth / 2)
			y = r * math.sin(theta) + (canvasheight / 2)
			w.create_text(x, y, text = base)
			# Create tick marks
			r = 250
			x2 = r * math.cos(theta) + (canvaswidth / 2)
			y2 = r * math.sin(theta) + (canvasheight / 2)
			w.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill = "black", activewidth = 4)
			# Save base location
			coords.append({"x": x2, "y": y2})
			
		# Draw segments between bases
		for b1, b2 in sstr:
			w.create_line(coords[b1]["x"], coords[b1]["y"], coords[b2]["x"], coords[b2]["y"], activewidth = 3)

		# Enter main event loop
		mainloop()

	def viz_planar(self,structure):
		"""Return bmp of planar secondary structure graph"""
		pass
		
	def viz_arc(self,structure):
		"""Return bmp of arc graph"""

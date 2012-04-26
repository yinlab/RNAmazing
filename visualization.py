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


	def viz_arc(self,sstr,seq):
		"""
		Returns bmp of arc secondary structure graph
		"""
		import math
		from Tkinter import * 

		# Create Tk instance
		master = Tk()
		master.title("Arc Diagram")
		master.resizable(width=0, height=0)

		# Create canvas
		canvasw = min((len(seq)*8),1024)
		canvash = min((len(seq)*2.25),768)
		w = Canvas(master, width = canvasw, height = canvash)
		w.pack()

		# Toggle base name display
		display_bases = True
		if len(seq) > 100:
			display_bases = False

		# Draw line and tick marks
		w.create_line(50,canvash-50,canvasw-50,canvash-50)
		l = len(seq)
		spacer = (canvasw-100)/(l-1)
		coords = []

		for i,base in enumerate(seq):
			x = (spacer * i) + 50
			y = canvash-50
			w.create_line(x, y+4, x, y-4)
			if display_bases:
				w.create_text(x, y+16 , text = base)
			coords.append({"x":x, "y": y})

		# Draw segments between bases
		for base1, base2 in sstr:
			w.create_arc(coords[base1]["x"], coords[base1]["y"] - (base2-base1)*2.5,
				     coords[base2]["x"], coords[base2]["y"] + (base2-base1)*2.5,
				      start = 0, extent = 180, style = "arc")


		# Enter main event loop
		mainloop()	


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
		w.configure(background = "white")

		# Toggle base name display
		display_bases = True
		if len(seq) > 100:
			display_bases = False

		# Draw circle and tick marks
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

			if display_bases:
				w.create_text(x, y, text = base)
			r = 250
			x2 = r * math.cos(theta) + (canvaswidth / 2)
			y2 = r * math.sin(theta) + (canvasheight / 2)
			w.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill = "black", activewidth = 4)
			# Save base location
			coords.append({"x": x2, "y": y2})
			
		# Draw segments between bases

		for base1, base2 in sstr:
			w.create_line(coords[base1]["x"], coords[base1]["y"], 
				      coords[base2]["x"], coords[base2]["y"])

		# Enter main event loop
		mainloop()	
		
	def viz_planar(self,seq,sstr):
		"""Return bmp of planar secondary structure graph"""

		import math
		from Tkinter import * 
		
		# Create Tk instance
		master = Tk()
		master.title("Arc Diagram")
		master.resizable(width=0, height=0)

		# Create canvas
		canvasw = 600
		canvash = 200
		w = Canvas(master, width = canvasw, height = canvash)
		w.pack()
		w.configure(background = "white")		
		
		class RNA:
			def __init__ (self, seq, sstr):
				"""
				Construct initial base + pair list
				"""
				seq_list = []
				for i in seq:
					seq_list.append({"base": i, "pair": -1, "mark" = False})
					for b1, b2 in sstr:
						seq_list[b1]["pair"] = b2
						
			def regions (self):
				"""
				Define stem regions
				"""
				regions = []
				for index,entry in enumerate(seq_list):
					if entry["pair"] != -1 and entry["mark"] = False:
						regions.append({"start1": entry["base"], 
								"end2": entry["pair"]})
						entry["mark"] = True
						n = entry["pair"]
						seq_list[n]["mark"] = True
						for j in seq_list[index::n]:
							if j["pair"] == n-1:
								j["mark"] = True
								n = j["pair"]
								seq_list[n]["mark"] = True
							else:
								break
						

			def loops (self): 
				"""
				Define loop regions
				"""
				pass

			def connection (self):
				"""
				Connects loops to stems and other loops
				"""

			def plot (self):
				"""
				Assign x, y coordinate values to all bases
				"""
				# Return array of {base: char, x: int, y: int, pair: int}
				pass

			def draw (self):
				"""
				Output to canvas
				"""				
				# Draw all bases and base pairs
				for base in self.plot:
					colors = {"G": "green", "C": "blue", "A": "red", "U": "yellow"}
					w.create_text(base["x"], base["y"], text = base["base"], fill = colors[base["base"]])
					if base["pair"] != -1:
						mate = self.plot["pair"]
						w.create_line(mate["x"], mate["y"], base["x"], base["y"], fill = "gray")
				
				# Enter main event loop
				mainloop()
				
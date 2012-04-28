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
		Returns svg of arc secondary structure graph
		"""
		import math
		import canvasvg
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


		# Output to file
		canvasvg.saveall("arc.svg", w)	


	def viz_circle(self, sstr, seq):
		"""
		Returns svg of chord secondary structure graph
		"""
		import math
		import canvasvg
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

		# Output to file
		canvasvg.saveall("circle.svg", w)
	
	def viz_mountain(self, seq, sstr):
		"""Returns svg of secondary structure mountain plot"""
		
		import math
		import canvasvg
		from Tkinter import *

		# Create a Tk instance
		master = Tk()
		master.title("Mountain Plot")
		master.resizable(width = 0, height = 0)

		# Create canvas
		canvaswidth = 800
		canvasheight = 600
		w = Canvas(master, width = canvaswidth, height = canvasheight)
		w.pack()
		w.configure(background = "white")	

		def find_enclosures(seq, sstr):
			enclosures = []
			max_enclosures = 0
			for i in seq:
				enclosures.append({"base": i, "enclosures": 0})
			for b1, b2 in sstr:
				for j in enclosures[(b1 + 1):b2]:
					j["enclosures"] += 1
					if max_enclosures < j["enclosures"]:
						max_enclosures += 1
			return (enclosures, max_enclosures)

		enclosures, max_enclosures = find_enclosures(seq, sstr)

		# Define bounding box of plot and other plot variables
		plot_x1 = 100
		plot_x2 = canvaswidth - 150
		plot_y1 = 50
		plot_y2 = canvasheight - 50
		xinc = (plot_x2 - plot_x1) / len(seq)
		yinc = (plot_y2 - plot_y1) / max_enclosures

		# Draw axes and labels
		w.create_line(plot_x1, plot_y1, plot_x1, plot_y2)
		w.create_line(plot_x1, plot_y2, plot_x2, plot_y2)
		w.create_text((plot_x2 - plot_x1) / 2 + plot_x1, plot_y2 + 30, text = "Sequence Position")
		w.create_text(plot_x1, plot_y1 - 15, text = "Enclosing Base Pairs")

		# Draw tick marks
		for i in range(10):
			w.create_line

		# Draw legend
		if 'U' in seq:
			colors = {'G': "green", 'C': "blue", 'A': "red", 'U': "yellow"}	
		else:
			colors = {'G': "green", 'C': "blue", 'A': "red", 'T': "yellow"}	
		legendx = plot_x2 + 20
		legendy = plot_y1 + 70
		w.create_rectangle(legendx - 20, legendy - 20, legendx + 50, legendy + 100)
		w.create_text(legendx - 10, legendy - 10, anchor = NW, text="LEGEND:")
		for index, (key, value) in enumerate(colors.iteritems()):
			w.create_oval(legendx - 2, legendy + 20 + 20*index, legendx + 2, legendy + 24 + 20*index, outline = value, fill = value)
			w.create_text(legendx + 20, legendy + 22 + 20*index, text=key)

		# Draw bases
		points = []
		for index, entry in enumerate(enclosures):
			base, height = entry["base"], entry["enclosures"]
			xcoord = index * xinc + plot_x1
			ycoord = plot_y2 - height * yinc
			points.append({"x": xcoord, "y": ycoord})
			w.create_oval(xcoord - 4, ycoord - 4, xcoord + 4, ycoord + 4, outline = colors[base], fill = colors[base])

		# Connect the dots
		for index, point in enumerate(points[1:]):
			w.create_line(point["x"], point["y"], points[index]["x"], points[index]["y"], fill = "black")

		canvasvg.saveall("mountainplot.svg", w)
	
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
				for index, entry in enumerate(seq_list):
					if entry["pair"] != -1 and entry["mark"] = False:
						regions.append({"start1": entry["base"], 
								"end2": entry["pair"]})
						
						region_index = len(regions) - 1
						entry["mark"] = True
						entry["region"] = region_index
						
						n = entry["pair"]
						ending = entry["pair"]
						seq_list[n]["mark"] = True
						seq_list[n]["region"] = region_index

						for i,j in enumerate(seq_list[index::ending]):
							if j["pair"] == n-1:
								j["mark"] = True
								j["region"] = region_index
								
								n = j["pair"]
								seq_list[n]["mark"] = True
								seq_list[n]["region"] = region_index
							else:
								regions[region_index]["start2"] = 
								seq_list[i-1]["base"]
								seq_list[i-1]["region"] = 
								region_index
								
								pair_loc = seq_list[i-1]["pair"]
								
								regions[region_index]["end2"] = 
								pair_loc
								
								seq_list[pair_loc]["region"] = 
								region_index


			def loops (self): 
				"""
				Define loop regions
				"""
				pass

			def connection (self):
				"""
				Connects loops to stems and other loops
				"""
				pass

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
			
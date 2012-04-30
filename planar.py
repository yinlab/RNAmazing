# Initialize modules
import math
from Tkinter import * 

# Create Tk instance
master = Tk()
master.title("RNA Planar Graph")
master.resizable(width=0, height=0)

# Create canvas
canvasw = 600
canvash = 200
w = Canvas(master, width = canvasw, height = canvash)
w.pack()

class RNA:
    def __init__ (self, seq, sstr):
        """
        Construct initial base + pair list
        """
        self.seq_list = []
        self.seq = seq
        self.loop = []
        for i in seq:
            self.seq_list.append({"base": i, "pair": -1, "mark": False})
        for b1, b2 in sstr:
            self.seq_list[b1]["pair"] = b2
            self.seq_list[b2]["pair"] = b1

    def region (self):
        """
        Define stem regions
        """
        self.regions = []
        
        print self.seq_list

        for index,entry in enumerate(self.seq_list):
            if entry["pair"] != -1 and entry["mark"] == False:
                self.regions.append({"start1": index, 
                                "end2": entry["pair"]})
                
                region_index = len(self.regions) - 1
                entry["mark"] = True
                entry["region"] = region_index
                
                n = entry["pair"]
                ending = entry["pair"]
                self.seq_list[n]["mark"] = True
                self.seq_list[n]["region"] = region_index
                
                for i,j in enumerate(self.seq_list):
                    print j["pair"]
                    print n-1
                    print ""
                    if i <= index:
                        continue
                    elif i >= ending:
                        break
                    elif j["pair"] == n-1:

                        j["mark"] = True
                        j["region"] = region_index
                        
                        
                        n = j["pair"]
                        self.seq_list[n]["mark"] = True
                        self.seq_list[n]["region"] = region_index
                    else:
                        self.regions[region_index]["start2"] = i-1
                        self.seq_list[i-1]["region"] = region_index
                        
                        pair_loc = self.seq_list[i]["pair"]
                        
                        self.regions[region_index]["end1"] = pair_loc
                        self.seq_list[pair_loc]["region"] = region_index
        
    def loops (self, i): 
        """
        Define loop regions
        """
        lp = {}
        self.cp = {}
        retloop = []

        while True:
            if (i == -1):
                break
            if (self.seq_list[i]["pair"] != -1):
                
                region_index = self.seq_list[i]["region"]
                rp = self.regions[region_index]
                print rp["start1"]
                print rp["start2"]
                if (i == rp["start1"]):
                    seq_list[i]["extracted"] = True
                    i_end1 = rp["end1"]
                    i_start2 = rp["start2"]
                    i_end2 = rp["end2"]
                    self.seq_list[i_end1]["extracted"] = True
                    self.seq_list[i_start2]["extracted"] = True
                    self.seq_list[i_end2]["extracted"] = True
                    if i_end1 < len(seq):
                        lp = self.loops(i_end1 + 1)
                    else:
                        lp = self.loops(-1)
                elif (i == rp["start2"]):
                    self.seq_list[i]["extracted"] = True
                    i_end1 = rp["end1"]
                    i_start2 = rp["start2"]
                    i_end2 = rp["end2"]
                    self.seq_list[i_end1]["extracted"] = True
                    self.seq_list[i_start2]["extracted"] = True
                    self.seq_list[i_end2]["extracted"] = True
                    if i_end2 < len(self.seq):
                        lp = self.loops(i_end2 + 1)
                    else:
                        lp = self.loops(-1)
                else:
                    print "base not found"
                self.loop.append(lp)
                lp_index = len(self.loop) - 1
                self.cp["loop"] = lp_index
                self.cp["region"] = region_index
                if (i == rp["start1"]):
                    self.cp["start"] = rp["start1"]
                    self.cp["end"] = rp["end2"]
                else:
                    self.cp["start"] = rp["start2"]
                    self.cp["end"] = rp["end1"]
                self.cp["extruded"] = False
                self.cp["broken"] = False
                self.cp["region"] = rp
                if (i == rp["start1"]):
                    self.cp["start"] = rp["start1"]
                    self.cp["end"] = rp["end2"]
                else:
                    self.cp["start"] = rp["start2"]
                    self.cp["end"] = rp["end1"]
                self.cp["extruded"] = False
                self.cp["broken"] = False
            i = self.seq_list[i]["pair"]
        if (++i > len(self.seq)):
            i = -1
        return self.cp

    def plot (self):
        """
        Assign x, y coordinate values to all bases
        """
        pass
    
    def draw (self):
        """
        Output to canvas
        """
        pass
		

# Begin another attempt
def planar2:
	# Fake input
	seq = "CGCGGGGUAGAGCAGCCUGGUAGCUCGUCGGGCUCAUA"
	sstr = [(1, 20), (2, 19), (4, 17), (5, 16), (6, 15), (7, 14), (22, 32), (23, 31), (24, 30)]

	# Initialize modules
	import math
	from Tkinter import * 

	# Create Tk instance
	master = Tk()
	master.title("RNA Planar Graph")
	master.resizable(width=0, height=0)

	# Create canvas
	canvasw = 800
	canvash = 800
	w = Canvas(master, width = canvasw, height = canvash)
	w.pack()

	# Construct initial list of bases and pairs
	bases = []
	for base in seq:
		bases.append({"base": base, "mate": -1})
	for b1, b2 in sstr:
		bases[b1]["mate"] = b2
		bases[b2]["mate"] = b1

	# Starting coordinates
	xstart = canvasw / 2
	ystart = 50
	locations = {}

	# Loop through rest of sequence
	i, j = 0, len(seq) - 1
	xcount = 0
	ycount = 0
	while (i < j):
		if bases[i]["mate"] == j:
			locations[i] = xstart - 20, ystart + ycount * 20
			locations[j] = xstart + 20, ystart + ycount * 20
			currentpair = i, j
			i += 1
			j -= 1
		else:
			# Find next base pair
			nextpair = None
			max_diff = 0
			for b1, b2 in sstr:
				if (b2 - b1) > max_diff:
					max_diff = b2 - b1
					nextpair = (b1, b2)
			if nextpair:
				sstr.pop(sstr.index(nextpair))
				k, l = nextpair
				ycount += ((k - i) + (j - l)) / 2
				locations[k] = xstart - 20, ystart + ycount * 20
				locations[l] = xstart + 20, ystart + ycount * 20
				i, j = k, l
			else: 
				i += 1
			
	print locations

	# Draw
	colors = {'G': "green", 'C': "blue", 'A': "yellow", 'U': "red", 'T': "red"}	
	for key, (x, y) in locations.iteritems():
		w.create_text(x, y, text = seq[key], fill = colors[seq[key]])
		
	mainloop()

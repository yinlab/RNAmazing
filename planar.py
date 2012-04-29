
# Initialize modules
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

class RNA:
    def __init__ (self, seq, sstr):
        """
        Construct initial base + pair list
        """
        seq_list = []
        for i in seq:
            seq_list.append({"base": i, "pair": -1, "mark": False})
            for b1, b2 in sstr:
                seq_list[b1]["pair"] = b2
                
    def regions (self):
        """
        Define stem regions
        """
        regions = []
        for index,entry in enumerate(seq_list):
            if entry["pair"] != -1 and entry["mark"] == False:
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
                        regions[region_index]["start2"] = seq_list[i-1]["base"]
                        seq_list[i-1]["region"] = region_index
                        
                        pair_loc = seq_list[i-1]["pair"]
                        
                        regions[region_index]["end2"] = pair_loc
                        
                        seq_list[pair_loc]["region"] = region_index
                        
                        
    def loops (self, i): 
        """
        Define loop regions
        """
        lp = []
        cp = []

        while True:
            if (i == ibase):
                break
            if (seq_list[i]["pair"] != -1):
                region_index = bases[i].region
                rp = regions[region_index]
                if (i == rp["start1"]):
                    seq_list[i]["extracted"] = True
                    i_end1 = rp["end1"]
                    i_start2 = rp["start2"]
                    i_end2 = rp["end2"]
                    seq_list[i_end1]["extracted"] = True
                    seq_list[i_start2]["extracted"] = True
                    seq_list[i_end2]["extracted"] = True
                    if i_end1 < len(seq):
                        lp = loops(i_end1 + 1)
                    else:
                        lp = loops(-1)
                elif (i == rp["start2"]):
                    seq_list[i]["extracted"] = True
                    i_end1 = rp["end1"]
                    i_start2 = rp["start2"]
                    i_end2 = rp["end2"]
                    seq_list[i_end1]["extracted"] = True
                    seq_list[i_start2]["extracted"] = True
                    seq_list[i_end2]["extracted"] = True
                    if i_end2 < len(seq):
                        lp = loops(i_end2 + 1)
                    else:
                        lp = loops(-1)
                else:
                    print "base not found"
                retloop["connections"] = cp
                cp["loop"] = lp 
                cp["region"] = region_index
                if (i == rp["start1"]):
                    cp["start"] = rp["start1"]
                    cp["end"] = rp["end2"]
                else:
                    cp["start"] = rp["start2"]
                    cp["end"] = rp["end1"]
                cp["extruded"] = False
                cp["broken"] = False
                cp["loop"] = retloop
                cp["region"] = rp
                if (i == rp["start1"]):
                    cp["start"] = rp["start1"]
                    cp["end"] = rp["end2"]
                else:
                    cp["start"] = rp["start2"]
                    cp["end"] = rp["end1"]
                cp["extruded"] = False
                cp["broken"] = False
            i = seq_list[i]["pair"]
        if (++i > len(seq)):
            i = -1
        return retloop


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

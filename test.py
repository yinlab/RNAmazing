from classes import *
from prediction import *
from visualization import Visualize
import sys, csv

print "Permutation:\n"
#perm = Permutation([Strand("DNA","A","ACGUGCCACGAUUCAACGUGGCACAG")])
perm = Permutation([Strand("DNA","A","GGGAAAUCC")])

print perm.get_concatamer()

print "\nNussinov:\n"
nussinov = NussinovPredictor(perm,None)

nussinov.generate_score_matrix()
print "\nCSV:\n"
writer = csv.writer(sys.stdout, delimiter="\t")
writer.writerows(nussinov.to_score_matrix().matrix)
print "\nMatrix:\n"
print "Length: "+str(len(nussinov.to_score_matrix().matrix))
#print nussinov.to_score_matrix().matrix
for row in nussinov.to_score_matrix().matrix:
    print str(len(row))+": "+ str(row)

print nussinov.traceback()


#sstr = nussinov.to_structure()
#(seq,length) = nussinov.get_sequence()
#vis = Visualize()
#vis.viz_circle(sstr, seq)

print "\nZuker:\n"
zuker = ZukerPredictor(perm,None)

zuker.generate_score_matrix()
print nussinov.to_score_matrix().matrix
print nussinov.traceback()

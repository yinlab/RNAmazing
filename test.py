from classes import *
from prediction import *
from visualization import Visualize

print "Permutation:\n"
perm = Permutation([Strand("DNA","A","GGGAAATCC")])
print perm.get_concatamer()

print "\nNussinov:\n"
nussinov = NussinovPredictor(perm,None)

nussinov.generate_score_matrix()
print nussinov.to_score_matrix().matrix
print nussinov.traceback()

sstr = nussinov.to_structure()
(seq,length) = nussinov.get_sequence()
vis = Visualize()
vis.viz_circle(sstr, seq)
#print "\nZuker:\n"
#zuker = ZukerPredictor(perm,None)
#
#zuker.generate_score_matrix()
#print nussinov.to_score_matrix().matrix
#print nussinov.traceback()

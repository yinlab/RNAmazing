from classes import *
from prediction import *

perm = Permutation([Strand("DNA","A","GGGAAATCC")])
nussinov = NussinovPredictor(perm,None)

nussinov.generate_score_matrix()
print nussinov.to_score_matrix().matrix
print nussinov.traceback()
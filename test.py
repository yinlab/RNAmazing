from classes import *
from prediction import *
from visualization import Visualize
import sys, csv

print "Permutation:\n"
perm = Permutation([Strand("DNA","A","ACGUGCCACGAUUCAACGUGGCACAG")])
#perm = Permutation([Strand("DNA","A","GGGAAAUCC")])

print perm.get_concatamer()

def print_matrix(matrix):
    print "\nCSV:\n"
    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerows(map(lambda row: map(lambda x: None if x==None else round(x,3), row), matrix) )
    print "\nMatrix:\n"
    print "Length: "+str(len(matrix))
    #print nussinov.to_score_matrix().matrix
    for row in matrix:
        print str(len(row))+": "+ str(row)


#print "\nNussinov:\n"
#nussinov = NussinovPredictor(perm,None)
#
#nussinov.generate_score_matrix()
#print "\nCSV:\n"
#writer = csv.writer(sys.stdout, delimiter="\t")
#writer.writerows(nussinov.to_score_matrix().matrix)
#print "\nMatrix:\n"
#print "Length: "+str(len(nussinov.to_score_matrix().matrix))
##print nussinov.to_score_matrix().matrix
#for row in nussinov.to_score_matrix().matrix:
#    print str(len(row))+": "+ str(row)
#
#print nussinov.traceback()


#sstr = nussinov.to_structure()
#(seq,length) = nussinov.get_sequence()


print "\nZuker:\n"
zuker = ZukerPredictor(perm,None)

zuker.generate_score_matrix()
print_matrix(zuker.to_score_matrix().matrix)
print_matrix(zuker.score_matrix_v.matrix)

print zuker.traceback()

sstr = zuker.to_structure()
(seq,l) = zuker.get_sequence()
vis = Visualize()
vis.viz_circle(sstr, seq)
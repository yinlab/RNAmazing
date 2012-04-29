from classes import *
from prediction import *
from visualization import Visualize
import sys, csv
import master


# Tests of Nussinov Algorithm:

# tests that in the case of a strand of all one nucleotide, no base pairs are formed
perm = Permutations([Strand("DNA","Strand 1","AAAAAAAAAA")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])
perm = Permutations([Strand("RNA","Strand 1","AAAAAAAAAA")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])

# tests that in the case of a strand of only one nucleotide, no base pairs are formed
perm = Permutations([Strand("DNA","Strand 1","A")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])
perm = Permutations([Strand("RNA","Strand 1","A")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])
perm = Permutations([Strand("DNA","Strand 1","T")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])
perm = Permutations([Strand("RNA","Strand 1","U")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
assert(sstr == [])

# tests that in the case of two complementary bases, only one pair is formed
perm = Permutations([Strand("DNA","Strand 1","AT")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)
perm = Permutations([Strand("DNA","Strand 1","CG")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)
perm = Permutations([Strand("RNA","Strand 1","AU")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)
perm = Permutations([Strand("RNA","Strand 1","CG")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)

# tests that in the case of three possible base pair interactions, only one pair is formed 
perm = Permutations([Strand("DNA","Strand 1","AAAT")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)
perm = Permutations([Strand("RNA","Strand 1","AAAU")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 1)

# tests the case where two base pairs are expected and formed 
perm = Permutations([Strand("DNA","Strand 1","AATT")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 2)

# tests the case where two strands that have direct complementary bind at all instances 
perm = Permutations([Strand("DNA","Strand 1","AAAA"),Strand("DNA","Strand 2","TTTT")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
length_test = len( sstr )
assert(length_test == 4)


# Tests of Real-time Recalculation:

# tests changing one base to see if generates the same score matrix as the case without using
# real-time recalculation
original_perm = Permutations([Strand("DNA","Strand 1","AAAAAA")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "nussinov")
score_matrix_one = 


# Tests of Zuker Algorithm:

# tests that in the case of a strand of one nucleotide, no base pairs are formed
perm = Permutations([Strand("DNA","Strand 1","A")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "zuker")
assert(sstr == [])
perm = Permutations([Strand("RNA","Strand 1","A")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "zuker")
assert(sstr == [])

# tests the case that for small sequences the zuker algorithm yields no base pair interactions
perm = Permutations([Strand("DNA","Strand 1","AATT")])
(sstr, seq, list_of_matrices) = master.algorithm_operator(perm, "zuker")
length_test = len( sstr )
assert(length_test == 0)


#print perm.get_concatamer()

#def print_matrix(matrix):
#    print "\nCSV:\n"
#    writer = csv.writer(sys.stdout, delimiter="\t")
#    writer.writerows(map(lambda row: map(lambda x: None if x==None else round(x,3), row), matrix) )
#    print "\nMatrix:\n"
#    print "Length: "+str(len(matrix))
    #print nussinov.to_score_matrix().matrix
#    for row in matrix:
 #       print str(len(row))+": "+ str(row)


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


#print "\nZuker:\n"
#zuker = ZukerPredictor(perm,None)

#zuker.generate_score_matrix()
#print_matrix(zuker.to_score_matrix().matrix)
#print_matrix(zuker.score_matrix_v.matrix)

#print zuker.traceback()

#sstr = zuker.to_structure()
#(seq,l) = zuker.get_sequence()
#vis = Visualize()
#vis.viz_circle(sstr, seq)
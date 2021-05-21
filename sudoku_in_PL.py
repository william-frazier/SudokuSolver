

# Will Frazier
# Adapted from Prof. Kfoury 

from z3 import * 

# The 9x9 grid, together with the 9 possible digits in each cell,
# is represented by a 9x9x9 matrix S of Boolean values :
S = [ [ [ Bool("s_%s_%s_%s" % (i+1, j+1, k+1)) for k in range(9) ]
        for j in range(9) ]
      for i in range(9) ]

# CONSTRAINT: Each cell contains a digit in {1, ..., 9} :
cell_constraint  = [ Or([ S[i][j][k] for k in range(9) ])
                     for i in range(9) for j in range(9) ]

# CONSTRAINT: Each row contains the same digit at most once :
row_constraint = [ And( Not( And( S[i][j][k], S[p][j][k] )))
                   for j in range(9) for k in range(9)
                   for i in range(8) for p in range(i+1,9) ]

# CONSTRAINT: Each column contains the same digit at most once :
column_constraint = [ And( Not( And( S[i][j][k], S[i][p][k] )))
                      for i in range(9) for k in range(9)
                      for j in range(8) for p in range(j+1,9) ]

# CONSTRAINT: Each 3x3 sub-grid contains a digit at most once :
sq_constraintA = [ And( Not( And( S[3*p+i][3*q+j][k], S[3*p+i][3*q+r][k])))
                   for k in range(9) for p in range(3) for q in range(3)
                   for i in range(3) for j in range(3) for r in range(j+1,3) ]

sq_constraintB = [ And( Not( And( S[3*p+i][3*q+j][k], S[3*p+r][3*q+n][k])))
                   for k in range(9) for p in range(3) for q in range(3)
                   for i in range(3) for j in range(3) for r in range(i+1,3)
                   for n in range(3) ]

# Combine the 5 preceding constraints into a single CONSTRAINT :
sudoku_constraint = cell_constraint + row_constraint + column_constraint \
                    + sq_constraintA + sq_constraintB

# An initial Sudoku instance is here encoded as a two-dimensional matrix.
# For other initial Sudoku instances, you need to modify the matrix 'instance'.

# An initial Sudoku instance, where '0' denotes an empty cell :
"""
#instance = ((0,0,0,0,9,4,0,3,0),
#            (0,0,0,5,1,0,0,0,7),
#            (0,8,9,0,0,0,0,4,0),
#            (0,0,0,0,0,0,2,0,8),
#            (0,6,0,2,0,1,0,5,0),
#            (1,0,2,0,0,0,0,0,0),
#            (0,7,0,0,0,0,5,2,0),
#            (9,0,0,0,6,5,0,0,0),
#            (0,4,0,9,7,0,0,0,0))


#instance = ((1,0,0,0,9,4,0,3,0),
#            (0,0,0,5,1,0,0,0,7),
#            (0,8,9,0,0,0,0,4,0),
#            (0,0,0,0,0,0,2,0,8),
#            (0,6,0,2,0,1,0,5,0),
#            (1,0,2,0,0,0,0,0,0),
#            (0,7,0,0,0,0,5,2,0),
#            (9,0,0,0,6,5,0,0,0),
#            (0,4,0,9,7,0,0,0,0))




# Another initial Sudoku instance :
instance = ((0,0,0,7,0,0,0,9,1),
            (0,3,1,0,0,8,0,0,0),
            (0,0,0,0,1,6,3,0,0),
            (0,9,0,0,0,0,0,8,4),
            (0,0,0,8,0,5,0,0,0),
            (6,4,0,0,0,0,0,7,0),
            (0,0,6,5,8,0,0,0,0),
            (0,0,0,1,0,0,7,3,0),
            (2,8,0,0,0,9,0,0,0))

# Another initial Sudoku instance :
instance = ((2,1,3,5,4,9,6,8,7),
            (0,0,0,8,0,0,0,0,0),
            (7,9,8,1,5,3,2,6,4),
            (9,5,4,7,8,6,0,0,0),
            (0,0,0,0,6,0,0,0,0),            
            (0,0,0,0,0,0,4,0,0),
            (0,0,0,3,0,1,8,5,9),
            (5,4,1,9,3,8,7,2,6),
            (8,7,6,4,9,2,5,1,3))
"""





# CONSTRAINT: Insert the clues according to their positions in the
# initial Sudoku instance :

def run(instance):
    initial_constraint = [ If(instance[i][j] == k+1, S[i][j][k], True)
                           for i in range(9) for j in range(9) for k in range(9)]
    
    # list to store all possible solutions
    results=[]
    s = Solver()
    # add our constraints
    s.add( sudoku_constraint + initial_constraint )
    while s.check() == sat:
        m = s.model()
        r = [ [ k+1 for j in range(9) for k in range(9)
                if is_true (m.evaluate(S[i][j][k])) ]
                for i in range(9) ]
        if r not in results:
            results.append (r)
        block = []
        for d in m :
            t = d()
            block.append ( t != m[d] )
        s.add (Or (block))
#    for n in range (len (results)) :
#        print_matrix(results[n])
#    if results == []:
#        print(results)
    return results
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools
from functools import reduce
import operator

def binary_ne_grid(kenken_grid):
    #  ((3),(11,12,13,6,0),(21,22,31,2,2),....)
   
    N = kenken_grid[0][0]


    dom = []
    for i in range(N):
        dom.append(i+1)
    

    vars = [["" for x in range(N)] for y in range(N)]
    for i in dom:
        for j in dom:
            vars[i-1][j-1] = Variable('KenCSP{}{}'.format(i, j), dom)
            


    cons = []
    for qi in range(len(dom)):
        for qj in range(len(dom) - 1):
            for qk in range(qj+1, len(dom)):
                con = Constraint("C(K{}{},K{}{})".format(qi+1,qj+1, qi+1,qk+1),[vars[qi][qj], vars[qj][qk]])
                
                con_col = Constraint("C(K{}{},K{}{})".format(qj+1,qi+1, qk+1,qi+1),[vars[qj][qi], vars[qk][qi]])
                
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:
                        sat_tuples.append(t)


                con.add_satisfying_tuples(sat_tuples)
                con_col.add_satisfying_tuples(sat_tuples)
                cons.append(con)
                cons.append(con_col)


 

    vars_flat = list(itertools.chain(*vars))  ## flatten 2d array
    csp = CSP("{}-KenCSP".format(N), vars_flat)
    for c in cons:
        csp.add_constraint(c)
    return csp, vars

def nary_ad_grid(kenken_grid):
   
    N = kenken_grid[0][0]


    dom = []
    for i in range(N):
        dom.append(i+1)
        

    vars = [["" for x in range(N)] for y in range(N)]
    for i in dom:
        for j in dom:
            vars[i-1][j-1] = Variable('KenCSP{}{}'.format(i, j), dom)
                
                   
     

    cons = [] 
    i = 0
    for row in vars:
        i += 1
        con = Constraint("C(Row{})".format(i),row)
        ## sat_tuples generation
        sat_tuples = []
        for t in itertools.permutations(range(N),N):
            addOne = tuple(x+1 for x in t)
            sat_tuples.append(addOne)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    
    for i in range(N):    
        col = []
        for row in vars:
            col.append(row[i])
            
        con_col = Constraint("C(Column{})".format(i+1),col)
        con_col.add_satisfying_tuples(sat_tuples)
        
        cons.append(con_col)

    vars_flat = list(itertools.chain(*vars))  ## flatten 2d array
    csp = CSP("{}-KenCSP".format(N), vars_flat)
    for c in cons:
        csp.add_constraint(c)
    return csp, vars

def kenken_csp_model(kenken_grid):   
    N = kenken_grid[0][0]
    dom = []
    grid_vars = kenken_grid[1:]
    for i in range(N):
        dom.append(i+1)

    vars = [["" for x in range(N)] for y in range(N)]
    for i in dom:
        for j in dom:
            vars[i-1][j-1] = Variable('KenCSP{}{}'.format(i, j), dom)

    ## n-ary 
    new_cons = [] 
    i = 0
    for row in vars:
        i += 1
        con = Constraint("C(Row{})".format(i),row)
        ## sat_tuples generation
        sat_tuples = []
        for t in itertools.permutations(range(N),N):
            addOne = tuple(x+1 for x in t)
            sat_tuples.append(addOne)
        con.add_satisfying_tuples(sat_tuples)
        new_cons.append(con)

    for i in range(N):    
        col = []
        for row in vars:
            col.append(row[i])
            
        con_col = Constraint("C(Column{})".format(i+1),col)
        con_col.add_satisfying_tuples(sat_tuples)
        new_cons.append(con_col)

    index = 0
    new_cons_cage = []
    denys_sat_tuples = []
    for cage in grid_vars:
        operation = cage[-1] 
        result = cage[-2] 
        cells = cage[ :len(cage) - 2]
        
        if len(cells) != 0:
            scope = []
        
            for cell in cells:
                str_cell = str(cell)
                i = int(str_cell[0])
                j = int(str_cell[1])
                scope.append(vars[i - 1][j - 1])
            sat_tuples = []
            options = list(itertools.product(list(range(1, N+1)), repeat = len(cells)))
            con = Constraint("KenKen_%i" % index, scope)
            for option in options:
                
                    if(operation == 0): 
                        func = reduce((lambda x, y: x + y), option)
                    elif(operation == 1): 
                        func = reduce((lambda x, y: x - y), option)
                    elif(operation == 2): 
                        func = reduce((lambda x, y: x / y), option)
                    elif(operation == 3): 
                        func = reduce((lambda x, y: x * y), option)

                    if func == result:
                        for perms in itertools.permutations(option):
                            if perms not in sat_tuples:
                                sat_tuples.append(perms)
            denys_sat_tuples.append(sat_tuples)
            con.add_satisfying_tuples(sat_tuples)
            # new_cons_test.append(con)
            new_cons_cage.append(con)
        

    vars_flat = list(itertools.chain(*vars))  ## flatten 2d array
    csp = CSP("{}-KenCSP".format(N), vars_flat)
    for c in new_cons:
        csp.add_constraint(c)
    for c in new_cons_cage:
        csp.add_constraint(c)
    return csp, vars

kenken_grid = [[5],[11,12,21,22,10,0],[13,14,23,24,34,18,0],[15,25,35,2,1],[31,32,33,1,1],[41,42,43,51,52,53,600,3],[44,54,55,2,2],[45,3]]
# kenken_grid = [[6],[11,12,13,2,2],[14,15,3,1],[16,26,36,11,0],[21,22,23,2,2],[24,25,34,35,40,3],[31,41,51,61,14,0],[32,33,42,43,52,53,3600,3],[44,54,64,120,3],[45,46,55,56,1,1],[62,63,5,1],[65,66,5,0]]
kenken_csp_model(kenken_grid)



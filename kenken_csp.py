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

def binary_ne_grid(kenken_grid):
    #  ((3),(11,12,13,6,0),(21,22,31,2,2),....)
   
    N = kenken_grid[0][0]


    dom = []
    for i in range(N):
        dom.append(i+1)
    
    vars = [["" for x in range(N)] for y in range(N)]
        
    grid_vars = kenken_grid[1:]
    for cage in grid_vars:
        cells = cage[ :len(cage) - 2]
        for cell in cells:
            str_cell = str(cell)
            
            i = int(str_cell[0])
            j = int(str_cell[1])
            vars[i - 1][j - 1] = Variable('KenCSP'+ str_cell, dom)
            

    # vars = []
    # for i in dom:
    #     vars.append(Variable('Q{}'.format(i), dom))


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
        
    grid_vars = kenken_grid[1:]
    for cage in grid_vars:
        cells = cage[ :len(cage) - 2]
        for cell in cells:
            str_cell = str(cell)
            
            i = int(str_cell[0])
            j = int(str_cell[1])
            vars[i - 1][j - 1] = Variable('KenCSP'+ str_cell, dom)
                
                   
     

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
    grid_vars = kenken_grid[1:]
    for cage in grid_vars:
        cells = cage[ :len(cage) - 2]
        for cell in cells:
            str_cell = str(cell)
            i = int(str_cell[0])
            j = int(str_cell[1])
            vars[i - 1][j - 1] = Variable('KenCSP'+ str_cell, dom)
    
    ## n-ary 
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



    i = 0
    for cage in grid_vars:
        operation = cage[-1] 
        result = cage[-2] 
        cells = cage[ :len(cage) - 2]
        scope = []
        for cell in cells:
            str_cell = str(cell)
            i = int(str_cell[0])
            j = int(str_cell[1])
            scope.append(vars[i - 1][j - 1])
        #  scope (an ORDERED list of variable objects)
       
        con = Constraint("KenKen_%i" % i, scope)
       
        for element in result:
            pass

            
            
        cells = cage[ :len(cage) - 2]
        for cell in cells:
            str_cell = str(cell)
            
            i = int(str_cell[0])
            j = int(str_cell[1])
            vars[i - 1][j - 1] = Variable('KenCSP'+ str_cell, dom)

        i -= 1



kenken_grid = [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]]
kenken_csp_model(kenken_grid)



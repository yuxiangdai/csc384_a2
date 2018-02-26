'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    unassigned = csp.get_all_unasgn_vars()
    max_index = -1
    max_degrees = -1

    for i in range(len(unassigned)):
        degree = 0
        var = unassigned[i]
        cons = csp.get_cons_with_var(var)
        for c in cons:
            unassignedInConstraint = var.get_n_unasgn()
            if unassignedInConstraint > 1: # our var + other unassigned
                degree += 1
        if degree > max_degrees:
            i = max_index
            max_degrees = degree 
    return unassigned[max_index]


def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!


    unassigned = csp.get_all_unasgn_vars()
    CurDomArr = []
    for i in range(len(unassigned)):
        var = unassigned[i]
        CurDom = var.cur_domain_size()
        CurDomArr.append(CurDom)

    smallestDom = min(CurDomArr)
    min_index = CurDomArr.index(smallestDom)
    return unassigned[min_index]

    
def val_lcv(csp, var):
    '''val lcv returns a list of values. The list is ordered by the
    value that rules out the fewest values in the remaining variables (i.e., the variable that gives the most
    flexibility later on) to the value that rules out the most.'''
    CurDom = var.cur_domain()
    unassigned = csp.get_all_unasgn_vars()
    cons = csp.get_cons_with_var(var)

    pruneCount = []


    for d in CurDom:
        
        prunes = 0

        for c in cons:
            vars = c.get_scope()
            vals = []
           
            
            for variable in vars:
                '''return assigned value...returns None if is unassigned'''
                vals.append(variable.get_assigned_value())
            vals[vars.index(var)] = d

            vals2 = [val for val in vals if val == None]

        ### test this vs  var.assign(x) result
            for var in vals2:
                for val in var.cur_domain():
                    if not c.has_support(var, val):
                        prunes += 1

            ## check vals2/vals3 for support

            ## store d, and # prunes
        
        pruneCount.append((d , prunes))

    sorted_by_second = sorted(pruneCount, key=lambda tup: tup[1])
    res_list = [x[0] for x in sorted_by_second]
    return res_list
                    
            
        

from myCSP.myVariable import *
from myCSP.myVarArray import *
from myCSP.myConstraint import *
from myCSP.AllDifferent import *
from board import Board
from refresher import Refresher

from queue import Queue
from collections import deque

# my_variables = [] is declared in myVariable.py
constraint_list = []
g: myConstraintGraph

def my_satisfy(*constraints: Union[myConstraint, myAllDifferent]) -> None:
    """
    Adds constraints to the constraint list and initializes the constraint graph.
    
    :param constraints: A variable number of constraint objects (either myConstraint or myAllDifferent).
    """
    for constraint in constraints:
        if isinstance(constraint, myAllDifferent):
            constraint_list.extend(constraint.get_constraints())
        else:
            constraint_list.append(constraint)

    global g
    g = myConstraintGraph(constraint_list)
    

def my_solve(do_unary_check: bool, 
             do_arc_consistency: bool, 
             do_mrv: bool, 
             do_lcv: bool, 
             refresher: Refresher) -> bool:
    """
    Solves the CSP problem using backtracking with optional heuristics.
    
    :param do_unary_check: If True, performs node consistency.
    :param do_arc_consistency: If True, applies arc consistency during backtracking.
    :param do_mrv: If True, applies Minimum Remaining Values (MRV) heuristic.
    :param do_lcv: If True, applies Least Constraining Value (LCV) heuristic.
    :param refresher: A Refresher object to update the UI during solving.
    Use `refresher.refresh_screen()` in middle of your code to update the sudoku on screen.
    :return: True if a solution is found, False otherwise.
    :raises: `StopAlgorithmException` if user clicks on 'Stop' or exit button.
    You do not need to handle this; it's handled in `main.py`.
    """

    # node consistency
    if do_unary_check:
        if not node_consistency(refresher):
            return False

    # backtrack 
    if not backtrack(do_arc_consistency, do_mrv, do_lcv, refresher):
        return False

    return True

def my_clear():
    """
    Clears variables and constraints for a fresh CSP instance.
    """
    my_variables = []
    constraint_list = []
    g = None

def node_consistency(refresher: Refresher) -> bool:
    """
    Applies node consistency by filtering values that do not satisfy unary constraints.

    Use `g.is_node_satisfied(v, d)` to check if `d` is satisfied for variable `v`
    
    :param refresher: A Refresher object to update the UI.
    :return: True if node consistency is maintained, False otherwise.
    """
    for v in my_variables:
        if v.value is not None:
            if not g.is_node_satisfied(v, v.value):
                return False
    return True


def backtrack(do_arc_consistency: bool, do_mrv: bool, do_lcv: bool, refresher: Refresher):
    """
    Implements backtracking search with optional heuristics.

    Use `g.is_assignment_complete()` to check if every variable has been assigned a value.
    Use `g.is_assignment_consistent(v)` to check if the value assigned to v satisfies all the constrains
    between v and its neighbors. It also checks the unary constraints.
    Use `extract_domains()` and  `restore_domains()` to backup and restore domains of all the variables.
    Use `set_doms_to_values()` to set remaining_domain=value for any variable that has been assigned a value. This
    can be useful before calling `inference()` since inference works with only remaining domains and not
    assigned values.
    
    :param do_arc_consistency: If True, use arc consistency forwarding algorithm inside `inference()` method.
    :param do_mrv: If True, apply Minimum Remaining Values (MRV) heuristic inside `select_unassigned_variable()` method.
    :param do_lcv: If True, apply Least Constraining Value (LCV) heuristic inside `order_domain_values()` method.
    :param refresher: A Refresher object to update the UI during solving.
    Use `refresher.refresh_screen()` in middle of your code to update the sudoku on screen.
    :return: True if a solution is found, False otherwise.
    """
    # Update UI before any work
    refresher.refresh_screen()

    # 1. Check for completion
    if g.is_assignment_complete():
        return True

    # 2. Select the next variable to assign
    var = select_unassigned_variable(do_mrv)

    # 3. Try each value in the chosen order
    for value in order_domain_values(var, do_lcv):
        # Assign value and check local consistency
        var.value = value
        set_doms_to_values()

        if g.is_assignment_consistent(var):
            # Backup domains before inference
            backup = extract_domains()

            # 4. Inference step (forward checking or AC)
            if inference(do_arc_consistency, refresher):
                # Recursive call
                if backtrack(do_arc_consistency, do_mrv, do_lcv, refresher):
                    return True

            # Restore domains if inference or deeper search failed
            restore_domains(backup)

        # Unassign variable before next trial
        var.value = None
        # Optional UI update after unassignment
        refresher.refresh_screen()

    # 5. No valid assignment found for this branch
    return False

def inference(do_arc_consistency: bool, refresher: Refresher) -> bool:
    """
    Uses forward-checking methods to eliminate variable domains that cause contradiction in the future. 
    """
    if do_arc_consistency:
        return arc_consistency(refresher)
    return True

def arc_consistency(refresher: Refresher) -> bool:
    """
    Implements the AC-3 algorithm for arc consistency.

    Use `g.get_arcs()` to get a queue containing all arcs in the graph.
    
    :param refresher: A Refresher object to update the UI.
    Use `refresher.refresh_screen()` in middle of your code to update the sudoku on screen.
    :return: True if arc consistency is maintained, False otherwise.
    """
    queue: Queue = g.get_arcs()

    while not queue.empty():
        xi, xj = queue.get()
        if revise(xi, xj):
            refresher.refresh_screen()
            if not xi.remaining_domain:
                return False
            for xk in g.neighbors(xi):
                if xk is not xj:
                    queue.put((xk, xi))
    return True

def revise(v1: myVariable, v2: myVariable):
    """
    Revises the domain of v1 by removing values that do not satisfy arc consistency with v2.

    For checking the satisfiability of any arc, use g.is_arc_satisfied(v1, v2, x1, x2) so 
    the order of values for variables remains consistent.
    
    :param v1: First variable.
    :param v2: Second variable.
    :return: True if the domain of v1 was revised, False otherwise.
    """
    revised = False

    for x1 in set(v1.remaining_domain):
        if not any(g.is_arc_satisfied(v1, v2, x1, x2) for x2 in v2.remaining_domain):
            v1.remaining_domain.remove(x1)
            revised = True

    return revised

    
def select_unassigned_variable(do_mrv: bool) -> myVariable:
    if do_mrv:
        return minimum_remaining_values()
    else:
        return select_static_order_variable()
    
def select_static_order_variable() -> myVariable:
    """
    Selects the first unassigned variable in the static (insertion) order.
    """
    for v in my_variables:
        if v.value is None:
            return v
    return None

def minimum_remaining_values() -> myVariable:
    """
    Returns a variable with the lowest remaining domain count.
    """
    best_var = None
    best_size = float('inf')
    for v in my_variables:
        if v.value is None:
            size = len(v.remaining_domain)
            if size < best_size:
                best_var, best_size = v, size
    if best_var is None:
        raise RuntimeError("No unassigned variables available for MRV")
    return best_var
        
def order_domain_values(v: myVariable, do_lcv: bool) -> List[int]:
    if do_lcv:
        return least_constraining_value(v)
    else:
        return static_order_domains(v)
    
def static_order_domains(v: myVariable) -> List[int]:
    """
    Returns the values in `v.remaining_domain` in ascending order.
    """
    # Ensure iterable and return sorted list
    return sorted(list(v.remaining_domain))

def least_constraining_value(v: myVariable) -> List[int]:
    """
    Orders the values in the domain of `v` based on how few constraints they impose on neighboring variables.  
    Values that allow the most options for neighboring variables are prioritized.
    """
    # YOUR CODE

def extract_domains() -> Dict[myVariable, List[int]]:
    """
    Backups all the remaining domains of every variable and returns them.

    :return: The becked-up domains as a dictionary {v:[d]}.
    """
    backup_domains = {}
    for v in my_variables:
        backup_domains[v] = v.remaining_domain
    return backup_domains

def restore_domains(backup_domains: Dict[myVariable, List[int]]):
    """
    Sets back the remaining domains of every variable to their becked-up domains.

    :param backup_domains: The previous remaining_domains of all variables.
    """
    for v in my_variables:
        v.remaining_domain = backup_domains[v]

def set_doms_to_values():
    """
    Sets remaining_domain of all variables with assigned value to their value.

    Use this function after a variable has been assigned a value
    and inference() needs to be called.
    """
    for v in my_variables:
        if v.value is not None:
            v.remaining_domain = set([v.value])
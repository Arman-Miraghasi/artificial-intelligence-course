# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # # just for test
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    from util import Stack
    # initialization
    visited = set()
    fringe = Stack()
    startState = problem.getStartState()
    fringe.push((startState, []))  

    # start searching :)
    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for childState, direction, stepCost in successors:
                newActions = actions + [direction]
                fringe.push((childState, newActions))

    print("This search doesn't have any answer!")
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    # initialization
    visited = set()
    fringe = Queue()
    startState = problem.getStartState()
    fringe.push((startState, []))  

    # start searching :)
    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for childState, direction, stepCost in successors:
                newActions = actions + [direction]
                fringe.push((childState, newActions))

    print("This search doesn't have any answer!")
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    # initialization
    visited = set()
    fringe = PriorityQueue()
    startState = problem.getStartState()
    fringe.push((startState, [], 0), 0)

    # start searching :)
    while not fringe.isEmpty():
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for childState, direction, childCost in problem.getSuccessors(state):
                newAction = actions + [direction]
                newCost = cost + childCost
                fringe.push((childState, newAction, newCost), newCost)

    print("This search doesn't have any answer!")
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    # initialization
    visited = set()
    fringe = PriorityQueue()
    startState = problem.getStartState()
    fringe.push((startState, [], 0), heuristic(startState, problem))

    # start searching :)
    while not fringe.isEmpty():
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for childState, direction, childCost in problem.getSuccessors(state):
                newAction = actions + [direction]
                newCost = cost + childCost
                fringe.push((childState, newAction, newCost), newCost + heuristic(childState, problem))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
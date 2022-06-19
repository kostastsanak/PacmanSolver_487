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

    def getCostOfActions(self, RE_actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #LIFO
    stack = util.Stack()
    #Contains all nodes pacman traveled
    traveled = []
    #PacmanMove is a list of 3 indexes 0=currrent position of pacman 1=To move Direction, 2=steps cost
    PacmanMove = []
    #Contains only the nodes needed for pacman to get to the goal state
    solution = util.Stack()
    
    steps = 0
    #creating the starting node of our stack
    stack.push((problem.getStartState(), 'StrartingNode', 0))

    while not stack.isEmpty():
        PacmanMove = stack.pop()
        ##print(PacmanMove)
        # Check if it arrived at goal state
        if problem.isGoalState(PacmanMove[0]):
            #print("From-To")
            #print(traveled)
            solution.push(PacmanMove[1])
            steps += 1
            return solution.list
        
        # Adding new move to the solution stack
        if PacmanMove[1] != 'StrartingNode':
            solution.push(PacmanMove[1])
            steps += 1
        
        traveled.append(PacmanMove[0])
        
        # Step of the while loop
        valid_moves = 0
        successors = problem.getSuccessors(PacmanMove[0])
        #1-4 loops
        for successor in successors:
            #checking for every loop if the move is valid and push it in to stack
            next_position = successor[0]
            next_direction = successor[1]
            
            # Get only valid moves
            if next_position not in traveled:
                valid_moves += 1
                stack.push((next_position, next_direction, steps))
        # If we found no valid moves and its not the goal we go to the next direction that was in the stack
        if valid_moves == 0:
            while steps != stack.list[-1][2]: # fixing the position of the solution
                steps -= 1
                solution.pop()
        
    print("Your Code is wrong find the mistake")    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    #FIFO
    queue = util.Queue()
    #Contains all nodes pacman traveled
    traveled = []
    #Contains all the info needed to get from one node to the other
    Dics = {}
    #reverse path
    RE_actions = []
    #Later will be filled with the exam steps to get from the start to the goal
    solution = util.Queue()
    
    #creating the starting node of our queue
    queue.push(problem.getStartState())
    traveled.append(problem.getStartState())
    
    while not queue.isEmpty():
        #PacmanMove now contains only the current potision of pacman
        PacmanMove = queue.pop()
        if problem.isGoalState(PacmanMove):
            break
    
        successors = problem.getSuccessors(PacmanMove)
        #1-4 loops
        for successor in successors:
            #checking for every loop if the move is valid and push it in to queue
            next_position = successor[0]
            next_direction = successor[1]        
            # Get only valid moves
            if next_position not in traveled:
                queue.push(next_position)
                traveled.append(next_position)
                #Could also be translated as, in order to get to next_position you have to be at PacmanMove and move to next_direction
                Dics[next_position] = (PacmanMove, next_direction)
    
    GoaltoStart = PacmanMove # goal position
    while GoaltoStart != problem.getStartState():
        previous_pos, direction = Dics[GoaltoStart]
        RE_actions.append(direction)
        GoaltoStart = previous_pos
    index = 0
    #reversing the steps by passing it to a queue
    for i in RE_actions:
        solution.push(RE_actions[index])
        index = index + 1
    #print(traveled)
    return solution.list

    util.raiseNotDefined()

def uniformCostSearch(problem):
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #g refers to the cost of our current position to the next node, while the heuristic estimates the cost of the cheapest path to the goal state.
    g = {}
    g[problem.getStartState()] = 0
    
    def update():
        g[next_position] = totalCost
        pq.update(item=next_position, priority=g[next_position] + heuristic(next_position, problem))
        passed.append(next_position)
        
    #Cheapest in first out
    pq = util.PriorityQueue()
    #Contains all the steps pacman has made
    traveled = []
    #Contains info of how you end up on the node you currently are in
    Dics = {}
    
    #reverse path
    RE_actions = []
    #solution path
    solution = util.Queue()
    
    pq.push(problem.getStartState(), 0)
    #Contains the nodes that pacman is currently neighbour of.
    passed = [problem.getStartState()]
    Dics[problem.getStartState()] = [None, None, 0]
    
    while not pq.isEmpty():
        #PacmanMove now contains only the current potision of pacman
        PacmanMove = pq.pop()
        passed.remove(PacmanMove)
        
        # Checks if we arived goal state
        if problem.isGoalState(PacmanMove):
            break
        successors = problem.getSuccessors(PacmanMove)
        
        #1-4 loops
        for successor in successors:
            #checking for every loop if the move is valid
            next_position = successor[0]
            next_direction = successor[1]
            next_cost = successor[2]
            
            totalCost = g[PacmanMove] + next_cost
            #if the neighbour has already been seen
            if next_position in passed or next_position in traveled:
                if g[next_position] > totalCost:
                    update()
            else:
                update()
            #inform dics
            if next_position in Dics:
                if Dics[next_position][2] > totalCost: #Dics[next_position][2] is totalCost
                    Dics[next_position] = [PacmanMove, next_direction, totalCost]
            else:
                Dics[next_position] = [PacmanMove, next_direction, totalCost]
            #print(totalCost)
            #print(PacmanMove,passed)
        traveled.append(PacmanMove)

    GoaltoStart = PacmanMove # goal position
    while GoaltoStart != problem.getStartState():
        previous_pos, direction, cost = Dics[GoaltoStart]
        RE_actions.append(direction)
        GoaltoStart = previous_pos
    index = 0
    #reversing the steps by passing it to a queue
    for i in RE_actions:
        solution.push(RE_actions[index])
        index = index + 1
    #print(traveled)
    
    return solution.list

    util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

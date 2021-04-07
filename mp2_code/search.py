# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
import queue
from queue import PriorityQueue
def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.
    """
    start_pos = maze.getStart()
    endlist = maze.getObjectives()
    print(endlist)
    endp = endlist[0]
    maze_dim = maze.getDimensions()
    print(maze_dim,endlist[0])
    maze_rows = maze_dim[0]
    maze_cols = maze_dim[1]
    maze_depth = maze_dim[2]
    path = []
    pathdict = {}
    visited = set()
    q = queue.Queue()
    visited.add(start_pos)
    q.put(start_pos)
    while(q.empty() != True):
        cur = q.get()
        if (maze.isObjective(cur[0],cur[1],cur[2])):
            break
        else:
            ne = maze.getNeighbors(cur[0],cur[1],cur[2])
            for i in ne:
                if (i not in visited) :
                    q.put(i)
                    visited.add(i)
                    pathdict[i] = cur
    i = cur
    
    if i not in pathdict:
        print('no')
        return None
    while(i != start_pos):
        path.append(i)
        if i not in pathdict:
            return None
        i = pathdict[i]
    path.append(start_pos)
    path.reverse()
    print(path)
    if (path == []) :
        return None
    return path

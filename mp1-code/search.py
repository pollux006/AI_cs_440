# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)
import queue
import maze
import sys
import copy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

# define a  Manhattan distance
def mah_d(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

# define a node class to keep track of the state
class mazenode:
    def __init__(self,position,lastnode,gx=0,hx=0,obj=[],mst=0,v_g=[False]):
        self.position = position # tuple of (x,y)
        self.row = position[0]
        self.col = position[1]
        self.visited = False
        self.lastnode = lastnode
        self.gx = gx
        self.hx = hx
        self.remain_obj = obj
        self.cur_mst = mst
        self.v_g = v_g
    def __eq__(self, value):
        return (self.position == value.position)
    def __lt__(self, value):
        return (self.gx+self.hx)<(value.gx+value.hx)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.Queue()
    start = maze.getStart()
    path =[]
    obj = maze.getObjectives()
    obj_num = len(obj)    
    visited = []

    cur = mazenode(start,None)
    visited.append(cur.position)                         #  set visitied
    while(not maze.isObjective(cur.row,cur.col)):
        nei = maze.getNeighbors(cur.row,cur.col)    # get neighbour
        for i in nei:
            if not (i in visited):
                q.put(mazenode((i[0],i[1]),cur))    # add the next node into queue
                visited.append((i[0],i[1]))
        cur = q.get()
        # print(visited)
        # print(cur.position)
    
    # get the path
    while (not cur.lastnode is None):     # extract the path
        path.append(cur.position)
        cur = cur.lastnode
    path.append(cur.position)
    return path[::-1]


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    # a priority queue
    q = queue.PriorityQueue()
    start = maze.getStart()
    path =[]
    obj = maze.getObjectives()
    obj_num = len(obj)    
    visited = []

    cur = mazenode(start,None,mah_d(start,start),mah_d(start,obj[0]))
    # visited.append(cur.position)    
    while(not maze.isObjective(cur.row,cur.col)):
        visited.append(cur.position)                         #  set visitied
        nei = maze.getNeighbors(cur.row,cur.col)    # get neighbour
        for i in nei:
            if not i in visited:
                gx = 1+cur.gx
                hx = mah_d(i,obj[0])
                q.put((gx+hx,mazenode((i[0],i[1]),cur,gx,hx)))    # add the next node into queue
                # visited.append((i[0],i[1]))
        cur = q.get()[1]


    # get the path
    while (not cur.lastnode is None):     # extract the path
        path.append(cur.position)
        cur = cur.lastnode
    path.append(cur.position)
    return path[::-1]

def findmst(D,first,num_point):
    key = [sys.maxsize]*num_point
    key[first] = 0
    mst_v = [False]*num_point
    mst = 0
    for i in range(num_point):
        #find the shortest vertex to 
        min = sys.maxsize
        for k in range(num_point):
            if key[k]<min and mst_v[k] == False:
                min = key[k]
                min_index = k
        mst+=min
        mst_v[min_index] = True

        # update the shortest edge adding egdes that goes from the last added veertex
        for k in range(num_point):
            if mst_v[k] == False and D[min_index][k]>0 and key[k] > D[min_index][k]: # case that the new adding edge is the samllest
                key[k] = D[min_index][k]

    return mst

def cal_dis_mat(points):
    d=[[0 for i in range(len(points))]for k in range(len(points))]
    for i in range(len(points)):
        for k in range(len(points)):
            d[i][k] = mah_d(points[i],points[k])
    return d

def find_min_dis(obj,point):
    min = sys.maxsize
    idx=0
    for goal in obj:
        dis = mah_d(point,goal)
        if dis<min:
            min = dis
            idx +=1
            
    # print('goal ',idx,' DIS ', min)
    return min,idx

def not_visited(pos,obj,visited):
    for i in visited:
        if i[0] == pos and i[1] == obj:
            return False
    return True


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    q = queue.PriorityQueue()
    start = maze.getStart()
    path = []
    obj = maze.getObjectives()
    obj_num = len(obj)    
    visited = []

    cur = mazenode(start,None,0,0,obj)
    # while(len(obj)>0):
    d = cal_dis_mat(obj)
    cur.cur_mst = findmst(d,0,len(obj))
    visited.append((cur.position,cur.remain_obj))     
    while(len(cur.remain_obj)>0):
        if(cur.position in cur.remain_obj):
            # print(cur.position, cur.remain_obj)
            if (len(cur.remain_obj)==1):break
            cur.remain_obj.remove(cur.position)
            d = cal_dis_mat(cur.remain_obj)
            cur.cur_mst = findmst(d,0,len(cur.remain_obj))

        # visited.append((cur.position,cur.remain_obj))                #  set visitied
        nei = maze.getNeighbors(cur.row,cur.col)    # get neighbour
        for i in nei:
            if not_visited(i,cur.remain_obj,visited):
                gx = cur.gx+1
                hx = cur.cur_mst + find_min_dis(cur.remain_obj,i)[0]
                # print(cur.position,'->',i)
                # print('hx:',hx,' ','gx:',gx,' ','fx:',gx+hx)
                q.put((gx+hx,mazenode((i[0],i[1]),cur,gx,hx,cur.remain_obj.copy(),cur.cur_mst)))    # add the next node into queue
                visited.append((i,cur.remain_obj))     
        cur = q.get()[1]
        # visited = []
        # print(cur.position)
        # print(len(cur.remain_obj))
        # obj.remove(cur.position)

    while (not cur.lastnode is None):     # extract the path
        path.append(cur.position)
        cur = cur.lastnode
    path.append(cur.position)
    # print(path)

    return path[::-1]

def astar_dis(maze,a,b):
    q = queue.PriorityQueue()
    visited = []

    cur = mazenode(a,None,0,mah_d(a,b))  
    while(not cur.position==b):
        visited.append(cur.position)                         #  set visitied
        nei = maze.getNeighbors(cur.row,cur.col)            # get neighbour
        for i in nei:
            if not i in visited:
                gx = 1+cur.gx
                hx = mah_d(i,b)
                q.put((gx+hx,mazenode((i[0],i[1]),cur,gx,hx)))    # add the next node into queue
        cur = q.get()[1]
    return cur.gx

def find_min_astar_dis(maze,obj,point):
    min = sys.maxsize
    for goal in obj:
        dis = astar_dis(maze,point,goal)
        if dis<min:
            min = dis
            idx = goal
    return min

def find_dis_goal_astar(maze,points):
    d=[[0 for i in range(len(points))]for k in range(len(points))]
    for i in range(len(points)):
        for k in range(len(points)):
            d[i][k] = astar_dis(maze,points[i],points[k])
    return d

def find_same_in_queue(q,position,fx,obj):
    for i in q.queue:
        if i[1].position == position and i[1].remain_obj == obj:
            if(i[0]>fx): i[0] =fx
            print('!')
            return True
    return False

def adjust_dis_max(d,v_g,obj_num):
    minus = 0
    d1 = copy.deepcopy(d)
    for i in range(obj_num):
        if v_g[i]:
            d1.pop(i-minus)
            for j in d1:
                j.pop(i-minus)
            minus+=1
    return d1

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.PriorityQueue()
    start = maze.getStart()
    path = []
    obj = maze.getObjectives()
    # print(obj)
    obj_num = len(obj)    
    d = find_dis_goal_astar(maze,obj)
    visited = []

    cur = mazenode(start,None,0,0,obj)
    # while(len(obj)>0):
    cur.cur_mst = findmst(d,0,len(obj))
    cur.v_g = [False for i in obj]
    visited.append((cur.position,cur.remain_obj))     
    counter = 0
    
    while(len(cur.remain_obj)>0):
        if(cur.position in cur.remain_obj):
            # print(cur.position, cur.remain_obj)

            #case that breaks
            if (len(cur.remain_obj)==1):break

            # set and remove reached goal
            cur.v_g[obj.index(cur.position)] = True
            cur.remain_obj.remove(cur.position)
            d1 = adjust_dis_max(d,cur.v_g,obj_num)
            # print('len:',len(d1[0]),len(cur.remain_obj))
            #calculate mst
            cur.cur_mst = findmst(d1,0,len(cur.remain_obj))
           

        # visited.append((cur.position,cur.remain_obj))                #  set visitied
        nei = maze.getNeighbors(cur.row,cur.col)    # get neighbour
        for i in nei:
            if not_visited(i,cur.remain_obj,visited):
                gx = cur.gx+1
                hx = cur.cur_mst + find_min_dis(cur.remain_obj,i)[0]
                if not find_same_in_queue(q,i,gx+hx,cur.remain_obj):
                #print(cur.position,'->',i)
                #print('hx:',hx,' ','gx:',gx,' ','fx:',gx+hx)
                    q.put((gx+hx,mazenode((i[0],i[1]),cur,gx,hx,cur.remain_obj.copy(),cur.cur_mst,cur.v_g.copy())))    # add the next node into queue
                    visited.append((i,cur.remain_obj))     
        cur = q.get()[1]
        # visited = []
        # print(cur.hx+cur.gx,' ',gx)
        #print(len(cur.remain_obj))
        counter+=1
        # if counter==7703:break
        # obj.remove(cur.position)

    while (not cur.lastnode is None):     # extract the path
        path.append(cur.position)
        cur = cur.lastnode
    path.append(cur.position)
    # print(path)

    return path[::-1]


def astar_dis_path(maze,a,b):
    q = queue.PriorityQueue()
    visited = []
    path=[]
    cur = mazenode(a,None,0,mah_d(a,b))  
    while(not cur.position==b):
        visited.append(cur.position)                         #  set visitied
        nei = maze.getNeighbors(cur.row,cur.col)            # get neighbour
        for i in nei:
            if not i in visited:
                gx = 1+cur.gx
                hx = mah_d(i,b)
                q.put((gx+hx,mazenode((i[0],i[1]),cur,gx,hx)))    # add the next node into queue
        cur = q.get()[1]
    
      # get the path
    while (not cur.lastnode is None):     # extract the path
        path.append(cur.position)
        cur = cur.lastnode
    path.append(cur.position)

    return cur.gx,path[::-1]

def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    path = []
    obj = maze.getObjectives()
    obj_num = len(obj)    
    visited = [False for i in obj]

    cur = mazenode(start,None,0,0,obj)
    min,idx = find_min_dis(obj,start)
    gx,path = astar_dis_path(maze,start,obj[idx])
    visited[idx] = True
    visited_num = 1

    
    while(1):
        if visited_num == len(obj):
            break
        min =  sys.maxsize
        next_idx = idx
        for i in range(len(obj)):
            if not visited[i]:
                dis = mah_d(obj[i],obj[idx])
                if dis<min:
                    min = dis
                    next_idx = i
        gx,minpath = astar_dis_path(maze,obj[idx],obj[next_idx])
        idx = next_idx
        visited[next_idx] = True
        visited_num+=1
        # print(visited_num)
        # print(next_idx)
        for i in minpath[1:]:
            path.append(i)

    return path

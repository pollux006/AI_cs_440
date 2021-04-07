
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    dim = len(arm.getArmAngle())
    if (dim==1):
        alpha = arm.getArmAngle()[0]
        beta = 0
        gamma =0
        alimit= arm.getArmLimit()[0]
        blimit=(0,0)
        hlimit=(0,0)
        row_num = int((alimit[1]-alimit[0])/granularity+1)
        col_num =1
        hei_num =1
        cur_r,cur_c,cur_h = angleToIdx((alpha,beta,gamma),(alimit[0],blimit[0],hlimit[0]),granularity)
    if(dim==3):
        alpha,beta,gamma = arm.getArmAngle()
        alimit,blimit,hlimit= arm.getArmLimit()
        row_num = int((alimit[1]-alimit[0])/granularity+1)
        col_num = int((blimit[1]-blimit[0])/granularity+1)
        hei_num = int((hlimit[1]-hlimit[0])/granularity+1)
        cur_r,cur_c,cur_h = angleToIdx((alpha,beta,gamma),(alimit[0],blimit[0],hlimit[0]),granularity)

    # print(cur_r,cur_c)
    map = [[[SPACE_CHAR for i in range(hei_num)] for j in range(col_num)]for k in range(row_num)]

    # go through map
    # print(obstacles)
    for i in range(row_num):
        for j in range(col_num):
            flag = False
            for k in range(hei_num):
                # if(flag):
                #     map[i][j][k] = WALL_CHAR
                #     continue
                cur_alpha,cur_beta,cur_gamma = idxToAngle((i,j,k),(alimit[0],blimit[0],hlimit[0]),granularity)
                arm.setArmAngle([cur_alpha,cur_beta,cur_gamma])
                if (not isArmWithinWindow(arm.getArmPos(),window)):
                    map[i][j][k] = WALL_CHAR
                elif(doesArmTouchObjects(arm.getArmPosDist(),obstacles,False)): 
                    map[i][j][k] = WALL_CHAR
                elif(i==cur_r and j == cur_c and k == cur_h):
                    map[i][j][k] = START_CHAR
                elif(dim==1 and i==cur_r):
                    map[i][j][k] = START_CHAR
                elif(doesArmTipTouchGoals(arm.getEnd(),goals)):
                    map[i][j][k] = OBJECTIVE_CHAR
                    # flag=True
                elif(doesArmTouchObjects(arm.getArmPosDist(),goals,True)):      
                    map[i][j][k] = WALL_CHAR

    return Maze(map,[alimit[0],blimit[0],hlimit[0]],granularity)

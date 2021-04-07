import numpy as np
import utils
import random

'''param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment'''
def transit(state):
    s_x = state[0]
    s_y = state[1]
    body = state[2]
    f_x = state[3]
    f_y = state[4]

    a1=0
    a2=0
    a3=0
    a4=0
    a5=0
    a6=0
    a7=0
    a0=0
    # if(s_x< 40 or s_x>=520 or s_y< 40 or s_y>=520):
    #     return_state[0] = 0
    #     return_state[1] = 0
    if(s_x==40): a0 = 1
    if(s_x==480): a0 = 2
    if(s_y==40): a1 = 1
    if(s_y==480): a1 = 2

    if (s_x<f_x): a2 = 2
    elif (s_x>f_x): a2 = 1
    
    if (s_y<f_y): a3 = 2
    elif (s_y>f_y): a3 = 1
    

    if (s_x,s_y-40) in body: a4 = 1
    if (s_x,s_y+40) in body: a5 = 1
    if (s_x-40,s_y) in body: a6 = 1
    if (s_x+40,s_y) in body: a7 = 1

    return (a0,a1,a2,a3,a4,a5,a6,a7)





class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.points = 0
        self.s = None
        self.a = None

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def find_best(self,stat):
        a_best = 0
        q_best = self.Q[stat+(0,)]
        for a in range(4):
            q = self.Q[stat+(a,)]
            if  q >= q_best:
                a_best = a
                q_best = q
        return a_best,q_best

    def find_next(self,stat):    
        a_next = 0
        q_next = self.Q[stat+(0,)]
        for a in range(4):
            q = self.Q[stat+(a,)]
            n = self.N[stat+(a,)]
            if n<self.Ne: q=1
            if  q >= q_next:
                a_next = a
                q_next = q
        return a_next,q_next


    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        s = transit(state)
        ## reward
        if dead: r = -1.0
        elif self.points<points: 
            r = 1.0
            self.points = points
        else: r = -0.1

        if self._train == True:
            if not self.s==None:
                
                #update

                pre_s = self.s  
                last_a = self.a
                Q = self.Q[pre_s+(last_a,)]
                
                self.N[pre_s+(last_a,)]+=1
                alpha = self.C/(self.C+self.N[pre_s+(last_a,)])
                a_best,q_best = self.find_best(s)
                self.Q[pre_s+(last_a,)] = Q + alpha*(r+self.gamma*(q_best)-Q)

            #update N
            a_next,q_next = self.find_next(s)
            # if not dead: self.N[s+(a_next,)]+=1
            
            #cache
            self.s = s
            self.a = a_next
            # check dead
            if dead: self.reset()
            return a_next

        else:
            # print(s)

            a_best,q_best = self.find_best(s)

            if dead: self.reset()
            return a_best

          


# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""

import numpy as np
import queue

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    
    n,d = train_set.shape
    W = np.zeros(d)
    b = 0

    
    for iter in range(max_iter):
        for i in range(n):
            image = train_set[i]
            # calculate yhat
            yhat = np.dot(W,image)+b
            if yhat>0:
                yhat=1
            else:
                yhat=0
            W += 1.0*learning_rate*(train_labels[i]-yhat)*image
            b += 1.0*learning_rate*(train_labels[i]-yhat)
        
        
        
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set

    W,b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)

    n,d = dev_set.shape
    dev_label = []
    for i in range(n):
        out = np.dot(W,dev_set[i])+b
        if out>0:
            dev_label.append(1)
        else:
            dev_label.append(0)
        
    return dev_label

def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here

    dev_label = []

    t_n,d = train_set.shape
    d_n,d = dev_set.shape
    for d_i in range(d_n):
        yh = 0
        q = queue.PriorityQueue()
        for t_i in range(t_n):
            q.put((np.linalg.norm(train_set[t_i]-dev_set[d_i]),t_i))
        for j in range(k):
            val,idx = q.get()
            yh+=train_labels[idx]
        if 1.0*yh/k > 0.5:
            dev_label.append(1)
        else:
            dev_label.append(0)
    
    return dev_label

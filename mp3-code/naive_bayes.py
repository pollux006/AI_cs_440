# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
import nltk
from nltk.corpus import stopwords
def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=0.8, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set

    pos_list = {}
    neg_list = {}
    pos_p = {}
    neg_p = {}
    # the count of pos word and neg word
    num_pos_word = 0
    num_neg_word = 0
    num_pos_review = 0
    num_neg_review = 0

    length = len(train_set)
    for i in range(length):
        if train_labels[i] == 1:
            num_pos_review+=1
            for word in train_set[i]:
                num_pos_word+=1
                if word not in pos_list:
                    pos_list[word] = 1
                else:
                    pos_list[word] += 1
        else:
            num_neg_review+=1
            for word in train_set[i]:
                num_neg_word+=1
                if word not in neg_list:
                    neg_list[word] = 1
                else:
                    neg_list[word] += 1

    
    pos_d = num_pos_word+smoothing_parameter*(len(pos_list)+1)
    neg_d = num_neg_word+smoothing_parameter*(len(neg_list)+1)

    for word in pos_list:
        pos_p[word] = 1.0*(pos_list[word]+smoothing_parameter)/pos_d
    for word in neg_list:
        neg_p[word] = 1.0*(neg_list[word]+smoothing_parameter)/neg_d
    
    UNK_pos = smoothing_parameter*1.0/pos_d
    UNK_neg = smoothing_parameter*1.0/neg_d
    
    
    ## train complete
    ## look at dev
    result = []
    for review in dev_set:
        # first see pos
        pos_value = math.log(num_pos_review/(num_pos_review+num_neg_review))
        neg_value = math.log(num_neg_review/(num_pos_review+num_neg_review))
        for word in review:
            if word in pos_p:
                pos_value += math.log(pos_p[word])
            else:
                pos_value += math.log(UNK_pos)
            
            if word in neg_p:
                neg_value += math.log(neg_p[word])
            else:
                neg_value += math.log(UNK_neg)
        if pos_value>= neg_value:
            result.append(1)
        else:
            result.append(0)

    return result

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=0.1, bigram_smoothing_parameter=0.1, bigram_lambda=0.5,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model
    stop = []
    new_train = []
    new_dev = []
    for review in train_set:
        new_review = []
        for word in review:
            if word not in stop:
                new_review.append(word)
        new_train.append(new_review)
    for review in dev_set:
        new_review = []
        for word in review:
            if word not in stop:
                new_review.append(word)
        new_dev.append(new_review)

    ## for unigram
    pos_uni_list = {}
    neg_uni_list = {}
    pos_uni_p = {}
    neg_uni_p = {}
    # the count of pos word and neg word
    num_pos_word = 0
    num_neg_word = 0
    num_pos_review = 0
    num_neg_review = 0

    length = len(new_train)
    for i in range(length):
        if train_labels[i] == 1:
            num_pos_review+=1
            for word in new_train[i]:
                #if word not in stop:
                    num_pos_word+=1
                    if word not in pos_uni_list:
                        pos_uni_list[word] = 1
                    else:
                        pos_uni_list[word] += 1
        else:
            num_neg_review+=1
            for word in new_train[i]:
                #if word not in stop:
                    num_neg_word+=1
                    if word not in neg_uni_list:
                        neg_uni_list[word] = 1
                    else:
                        neg_uni_list[word] += 1

    
    pos_d = num_pos_word+unigram_smoothing_parameter*(len(pos_uni_list)+1)
    neg_d = num_neg_word+unigram_smoothing_parameter*(len(neg_uni_list)+1)

    for word in pos_uni_list:
        pos_uni_p[word] = 1.0*(pos_uni_list[word]+unigram_smoothing_parameter)/pos_d
    for word in neg_uni_list:
        neg_uni_p[word] = 1.0*(neg_uni_list[word]+unigram_smoothing_parameter)/neg_d
    
    UNK_pos = unigram_smoothing_parameter*1.0/pos_d
    UNK_neg = unigram_smoothing_parameter*1.0/neg_d
    



     ## for bigram
    pos_bi_list = {}
    neg_bi_list = {}
    pos_bi_p = {}
    neg_bi_p = {}
    # the count of pos word and neg word
    num_pos_wordpair = 0
    num_neg_wordpair = 0

    length = len(new_train)
    for i in range(length):
        if train_labels[i] == 1:
            
            for j in range(len(new_train[i])-1):
                wordpair = (new_train[i][j],new_train[i][j+1])
                num_pos_wordpair+=1
                if wordpair not in pos_bi_list:
                    pos_bi_list[wordpair] = 1
                else:
                    pos_bi_list[wordpair] += 1
        else:
            
            for j in range(len(new_train[i])-1):
                wordpair = (new_train[i][j],new_train[i][j+1])
                num_neg_wordpair+=1
                if wordpair not in neg_bi_list:
                    neg_bi_list[wordpair] = 1
                else:
                    neg_bi_list[wordpair] += 1

    
    pos_d_pair = num_pos_wordpair+bigram_smoothing_parameter*(len(pos_bi_list)+1)
    neg_d_pair = num_neg_wordpair+bigram_smoothing_parameter*(len(neg_bi_list)+1)

    for word in pos_bi_list:
        pos_bi_p[word] = 1.0*(pos_bi_list[word]+bigram_smoothing_parameter)/pos_d_pair
    for word in neg_bi_list:
        neg_bi_p[word] = 1.0*(neg_bi_list[word]+bigram_smoothing_parameter)/neg_d_pair
    
    UNK_bi_pos = bigram_smoothing_parameter*1.0/pos_d_pair
    UNK_bi_neg = bigram_smoothing_parameter*1.0/neg_d_pair
    
    
    

    ## train complete
    ## look at dev
    result = []
    for review in new_dev:
        # first see pos
        pos_value_uni = math.log(num_pos_review/(num_pos_review+num_neg_review))
        neg_value_uni = math.log(num_neg_review/(num_pos_review+num_neg_review))
        pos_value_bi = pos_value_uni
        neg_value_bi = neg_value_uni

        for word in review:
            #if word not in stop:
                if word in pos_uni_p:
                    pos_value_uni += math.log(pos_uni_p[word])
                else:
                    pos_value_uni += math.log(UNK_pos)
            
                if word in neg_uni_p:
                    neg_value_uni += math.log(neg_uni_p[word])
                else:
                    neg_value_uni += math.log(UNK_neg)

        for j in range(len(review)-1):
            wordpair = (review[j],review[j+1])
            if wordpair in pos_bi_p:
                pos_value_bi += math.log(pos_bi_p[wordpair])
            else:
                pos_value_bi += math.log(UNK_bi_pos)
            
            if wordpair in neg_bi_p:
                neg_value_bi += math.log(neg_bi_p[wordpair])
            else:
                neg_value_bi += math.log(UNK_bi_neg)

        pos_value = (1-bigram_lambda)*pos_value_uni+bigram_lambda*pos_value_bi
        neg_value = (1-bigram_lambda)*neg_value_uni+bigram_lambda*neg_value_bi

        if pos_value>= neg_value:
            result.append(1)
        else:
            result.append(0)




    return result
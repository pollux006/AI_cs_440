"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    output=[]
    word_dic={}
    tag_lis = {}
    for sentence in train:
        for pair in sentence:
            if pair[0] in word_dic:
                if pair[1] in word_dic[pair[0]]:
                    word_dic[pair[0]][pair[1]] +=1
                else:
                    word_dic[pair[0]][pair[1]] =1
            else:
                word_dic[pair[0]] = {}
                word_dic[pair[0]][pair[1]] =1
        
            if pair[1] in tag_lis:
                tag_lis[pair[1]]+=1
            else:
                tag_lis[pair[1]]=1

    ## find most common tags
    max = 0  
    for tag in tag_lis:
        if tag_lis[tag] > max:
            max = tag_lis[tag]
            com_tag = tag

    ## tag the test set
    for sentence in test:
        cur_sen = []
        for word in sentence:
            if word in word_dic:
                dic = word_dic[word]
                max = 0
                for tag in dic:
                    if dic[tag] > max:
                        max = dic[tag]
                        tag_max = tag
                cur_sen.append((word,tag_max))
            else:
                cur_sen.append((word,com_tag))
        output.append(cur_sen)

    return output
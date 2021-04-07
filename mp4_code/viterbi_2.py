"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""
import math
def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''


    tag_list = []

    word_list= {}
    tag_count ={}

    tag_prob = {}
    # times of pre tag to this tag
    tag_tag={}
    #times of tag given word

    tag_word={}
    init = {}

    #smooth factor
    i_alpha = 0.001
    alpha = 0.00001
    e_alpha = 0.05

    for sentence in train:
        pre = sentence[0]
        length = len(sentence)
        for i in range(length):
            cur = sentence[i]
            if cur[1] not in tag_list: tag_list.append(cur[1])
            
            if cur[0] not in word_list: word_list[cur[0]] = cur[1]
            else:  word_list[cur[0]] = 0

            
            if i == 0:
                if cur[1] in init:
                    init[cur[1]] +=1
                else:
                    init[cur[1]]=1
            else:
                pre = sentence[i-1]
            
            # if not first then we have tag to tag
                if pre[1] in tag_tag:
                    if cur[1] in tag_tag[pre[1]]:
                        tag_tag[pre[1]][cur[1]]+=1
                    else:
                        tag_tag[pre[1]][cur[1]]=1
                else:
                    tag_tag[pre[1]]={}
                    tag_tag[pre[1]][cur[1]]=1

            # cur word to tag
            if cur[1] in tag_word:
                if cur[0] in tag_word[cur[1]]:
                    tag_word[cur[1]][cur[0]]+=1
                else:
                    tag_word[cur[1]][cur[0]]=1
            else:
                tag_word[cur[1]]={}
                tag_word[cur[1]][cur[0]]=1

    tag_sum = 0    
    for word in word_list:
        if not word_list[word]==0:
            tag = word_list[word]
            tag_sum+=1
            if tag not in tag_count:
                tag_count[tag]=1
            else:
                tag_count[tag]+=1

    for tag in tag_count:
        tag_prob[tag] = tag_count[tag]/tag_sum
    print(tag_prob)
    
    # initial probability and  
    P_i = {}
    P_i_un = 0
    i_n =0  # number and types
    i_v =0
   

    for tag in init:
        i_v+=1
        i_n+=init[tag]
    for tag in init:
        P_i[tag] = math.log((init[tag]+i_alpha)/(i_n+i_alpha*(i_v+1)))
    P_i_un = math.log(i_alpha/(i_n+i_alpha*(i_v+1)))

    # transition probability  (pre,cur)
    P_tag_tag = {}
    P_tt_un = {}
    tt_n=0  # number and types
    tt_v=0

    for pre in tag_tag:
        tt_v=0
        tt_n=0
        for tag in tag_tag[pre]:
            tt_v+=1
            tt_n+= tag_tag[pre][tag]

        #calculate probabilities
    
        for tag in tag_tag[pre]:
            P_tag_tag[(pre,tag)] = math.log((tag_tag[pre][tag]+alpha)/(tt_n+alpha*(tt_v+1)))
        #unkown case:
        P_tt_un[pre]= math.log(alpha/(tt_n+alpha*(tt_v+1)))
    P_t_un = 0

    # emission probability  (cur_word,tag)
    P_word_tag = {}
    P_wt_un = {}
    wt_n=0  # number and types
    wt_v=0
    for tag in tag_word:
        wt_n=0
        wt_v=0
        for word in tag_word[tag]:
            wt_v+=1
            wt_n+= tag_word[tag][word]

        if tag not in tag_prob: e_alpha_t=e_alpha*0.000001
        else: e_alpha_t = e_alpha*tag_prob[tag]
        for word in tag_word[tag]:
            P_word_tag[(tag,word)] = math.log((tag_word[tag][word]+e_alpha_t)/(wt_n+e_alpha_t*(wt_v+1)))
        P_wt_un[tag]= math.log(e_alpha_t/(wt_n+e_alpha_t*(wt_v+1)))



    res=[]

    test_time = 0


    for sentence in test:
        v = []
        b = []
        length = len(sentence)
        for i in range(length):
            word = sentence[i]
            vk = {}
            bk= {}

            for tag_b in tag_list:    
                if i==0:
                    if tag_b in P_i:
                        p1 = P_i[tag_b]
                    else:
                        p1 = P_i_un
                    if (tag_b,word) in P_word_tag:
                        p2 = P_word_tag[(tag_b,word)]
                    else:
                        p2 = P_wt_un[tag_b]
                    vk[tag_b] = p1+p2
                    bk[tag_b] = ''
                else:
                    maxa= 0
                    max_p= -math.inf
                    for tag_a in tag_list:
                        if (tag_a,tag_b) in P_tag_tag:
                            p2 = P_tag_tag[(tag_a,tag_b)]
                        else:
                            if tag_a not in tag_tag:
                                p2=0
                            else: p2 = P_tt_un[tag_a]
                        if (tag_b,word) in P_word_tag:
                            p3 = P_word_tag[(tag_b,word)]
                        else:
                            p3 = P_wt_un[tag_b]

                        p = v[i-1][tag_a] + p2 + p3
                        if p> max_p:
                            max_p = p
                            maxa = tag_a
                    
                    vk[tag_b] = max_p
                    bk[tag_b] = maxa
            v.append(vk)
            b.append(bk)
            
            

        k = length-1
        new_sentence = []
        arg_b=[]
        #find last
        maxa= 0
        max_p= -math.inf
        for tag in v[k]:
            if v[k][tag]>max_p:
                max_p = v[k][tag]
                maxa = tag
        arg_b.append(maxa)
        
        
        while(not k<1):
            maxa = b[k][maxa]
            arg_b.append(maxa)
            k-=1
        
        arg_b.reverse()
        for i in range(length):
            new_sentence.append((sentence[i],arg_b[i]))

        res.append(new_sentence)

        ###############test
        # test_time+=1
        # print("______________________\nSENTENCE:    \n",sentence)
        # print("______________________\nOUT:    \n",new_sentence)
        # print("______________________\n")
        # print("t-t-un:",P_tag_tag[('NOUN','PERIOD')],P_tag_tag[('START','X')],P_tt_un['X'],P_wt_un['X'])
        # print('\n')
        # print("______________________\n V:    \n")
        # for c in v:
        #     for k in c.items():
        #         print(k[0],'[',k[1],']',' ',end='')
        #     print(end='\n\n')

        # print("_________________\n bk:",)
        # for c in b:
        #     for k in c.items():
        #         print(k[0],'[',k[1],']',' ',end='')
        #     print(end='\n\n')
        
        # print(P_wt_un)
        # print("_____________________________________________________________________________")
        
        
        # if test_time>1:
        #     break
       
        
    
    return res
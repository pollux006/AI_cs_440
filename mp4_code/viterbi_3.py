"""
Part 4: Here should be your best version of viterbi, 
with enhancements such as dealing with suffixes/prefixes separately
"""
import math
def contain_ly(word):
    if len(word)<2: return False
    if(word[-1]=='y' and word[-2]=='l'):
        return True
    else: return False
def contain_ing(word):
    if len(word)<3: return False
    if(word[-1]=='g' and word[-2]=='n'and word[-3]=='i'):
        return True
    else: return False
def contain_ed(word):
    if len(word)<2: return False
    if(word[-1]=='d' and word[-2]=='e'):
        return True
    else: return False
def contain_ness(word):
    if len(word)<4: return False
    if(word[-1]=='s' and word[-2]=='s' and word[-3]=='e' and word[-4]=='n'):
        return True
    else: return False
def contain_ive(word):
    if len(word)<3: return False
    if(word[-1]=='e' and word[-2]=='v' and word[-3]=='i'):
        return True
    else: return False
def contain_able(word):
    if len(word)<4: return False
    if(word[-1]=='e' and word[-2]=='l' and word[-3]=='b'):
        return True
    else: return False
def contain_ful(word):
    if len(word)<3: return False
    if(word[-1]=='l' and word[-2]=='u' and word[-3]=='f'):
        return True
    else: return False
def contain_er(word):
    if len(word)<2: return False
    if(word[-1]=='r' and word[-2]=='e'):
        return True
    else: return False
def contain_less(word):
    if len(word)<4: return False
    if(word[-1]=='s' and word[-2]=='s' and word[-3]=='e' and word[-4]=='l'):
        return True
    else: return False

def viterbi_3(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    
    tag_list = []

    word_list= {}
    tag_count ={}

    
    # times of pre tag to this tag
    tag_tag={}
    #times of tag given word

    tag_word={}
    init = {}

    #smooth factor
    i_alpha = 0.00001
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


    ### handle special words
    tag_prob = {}

    tag_ly_prob = {}
    tag_ing_prob = {}
    tag_ed_prob = {}
    tag_ness_prob = {}
    tag_ive_prob = {}
    tag_able_prob = {}
    tag_ful_prob = {}
    tag_er_prob = {}
    tag_less_prob = {}

    tag_ing_count ={}
    tag_ly_count = {}
    tag_ed_count = {}
    tag_ness_count = {}
    tag_ive_count = {}
    tag_able_count = {}
    tag_er_count = {}
    tag_ful_count = {}
    tag_less_count = {}


    tag_sum = 0
    tag_ly_sum = 0  
    tag_ing_sum = 0  
    tag_ed_sum = 0  
    tag_ness_sum = 0  
    tag_ive_sum = 0
    tag_able_sum = 0  
    tag_ful_sum = 0  
    tag_er_sum = 0  
    tag_less_sum = 0  

    for word in word_list:
        if not word_list[word]==0:
            tag = word_list[word]
            if contain_ly(word):
                print(word)
                tag_ly_sum+=1
                if tag not in tag_ly_count:
                    tag_ly_count[tag]=1
                else:
                    tag_ly_count[tag]+=1
            elif contain_ing(word):
                tag_ing_sum+=1
                if tag not in tag_ing_count:
                    tag_ing_count[tag]=1
                else:
                    tag_ing_count[tag]+=1
            elif contain_ed(word):
                tag_ed_sum+=1
                if tag not in tag_ed_count:
                    tag_ed_count[tag]=1
                else:
                    tag_ed_count[tag]+=1
            elif contain_ness(word):
                tag_ness_sum+=1
                
                if tag not in tag_ness_count:
                    tag_ness_count[tag]=1
                else:
                    tag_ness_count[tag]+=1
            elif contain_ive(word):
                
                tag_ive_sum+=1
                if tag not in tag_ive_count:
                    tag_ive_count[tag]=1
                else:
                    tag_ive_count[tag]+=1
            elif contain_able(word):
                tag_able_sum+=1
                if tag not in tag_able_count:
                    tag_able_count[tag]=1
                else:
                    tag_able_count[tag]+=1
            elif contain_er(word):
                tag_er_sum+=1
                if tag not in tag_er_count:
                    tag_er_count[tag]=1
                else:
                    tag_er_count[tag]+=1

            elif contain_ful(word):
                tag_ful_sum+=1
                if tag not in tag_ful_count:
                    tag_ful_count[tag]=1
                else:
                    tag_ful_count[tag]+=1

            elif contain_less(word):
                tag_less_sum+=1
                if tag not in tag_less_count:
                    tag_less_count[tag]=1
                else:
                    tag_less_count[tag]+=1
            else:
                tag_sum+=1
                if tag not in tag_count:
                    tag_count[tag]=1
                else:
                    tag_count[tag]+=1
            
            

    for tag in tag_count:
        tag_prob[tag] = tag_count[tag]/tag_sum
    for tag in tag_ly_count:
        tag_ly_prob[tag] = tag_ly_count[tag]/tag_ly_sum
    for tag in tag_ing_count:
        tag_ing_prob[tag] = tag_ing_count[tag]/tag_ing_sum
    for tag in tag_ed_count:
        tag_ed_prob[tag] = tag_ed_count[tag]/tag_ed_sum
    for tag in tag_ness_count:
        tag_ness_prob[tag] = tag_ness_count[tag]/tag_ness_sum
    for tag in tag_ive_count:
        tag_ive_prob[tag] = tag_ive_count[tag]/tag_ive_sum
    for tag in tag_able_count:
        tag_able_prob[tag] = tag_able_count[tag]/tag_able_sum
    for tag in tag_er_count:
        tag_er_prob[tag] = tag_er_count[tag]/tag_er_sum
    for tag in tag_ful_count:
        tag_ful_prob[tag] = tag_ful_count[tag]/tag_ful_sum
    for tag in tag_less_count:
        tag_less_prob[tag] = tag_less_count[tag]/tag_less_sum
    




    
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
    P_wt_un_ly = {}
    P_wt_un_ing = {}
    P_wt_un_ed = {}
    P_wt_un_ness = {}
    P_wt_un_ive = {}
    P_wt_un_able = {}
    P_wt_un_ful = {}
    P_wt_un_er = {}
    P_wt_un_less = {}
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
        if tag not in tag_ly_prob: e_alpha_t_ly=e_alpha*0.000001
        else: e_alpha_t_ly = e_alpha*tag_ly_prob[tag]
        if tag not in tag_ing_prob: e_alpha_t_ing=e_alpha*0.000001
        else: e_alpha_t_ing = e_alpha*tag_ing_prob[tag]
        if tag not in tag_ed_prob: e_alpha_t_ed=e_alpha*0.000001
        else: e_alpha_t_ed = e_alpha*tag_ed_prob[tag]
        if tag not in tag_ness_prob: e_alpha_t_ness=e_alpha*0.000001
        else: e_alpha_t_ness = e_alpha*tag_ness_prob[tag]
        if tag not in tag_ive_prob: e_alpha_t_ive=e_alpha*0.000001
        else: e_alpha_t_ive = e_alpha*tag_ive_prob[tag]
        if tag not in tag_able_prob: e_alpha_t_able=e_alpha*0.000001
        else: e_alpha_t_able = e_alpha*tag_able_prob[tag]
        if tag not in tag_ful_prob: e_alpha_t_ful=e_alpha*0.000001
        else: e_alpha_t_ful = e_alpha*tag_ful_prob[tag]
        if tag not in tag_er_prob: e_alpha_t_er=e_alpha*0.000001
        else: e_alpha_t_er = e_alpha*tag_er_prob[tag]
        if tag not in tag_less_prob: e_alpha_t_less=e_alpha*0.000001
        else: e_alpha_t_less = e_alpha*tag_less_prob[tag]

        for word in tag_word[tag]:
            P_word_tag[(tag,word)] = math.log((tag_word[tag][word]+e_alpha_t)/(wt_n+e_alpha_t*(wt_v+1)))

        P_wt_un[tag]= math.log(e_alpha_t/(wt_n+e_alpha_t*(wt_v+1)))
        P_wt_un_ly[tag]= math.log(e_alpha_t_ly/(wt_n+e_alpha_t_ly*(wt_v+1)))
        P_wt_un_ing[tag]= math.log(e_alpha_t_ing/(wt_n+e_alpha_t_ing*(wt_v+1)))
        P_wt_un_ed[tag]= math.log(e_alpha_t_ed/(wt_n+e_alpha_t_ed*(wt_v+1)))
        P_wt_un_ness[tag]= math.log(e_alpha_t_ness/(wt_n+e_alpha_t_ness*(wt_v+1)))
        P_wt_un_ive[tag]= math.log(e_alpha_t_ive/(wt_n+e_alpha_t_ive*(wt_v+1)))
        P_wt_un_able[tag]= math.log(e_alpha_t_able/(wt_n+e_alpha_t_able*(wt_v+1)))
        P_wt_un_er[tag]= math.log(e_alpha_t_er/(wt_n+e_alpha_t_er*(wt_v+1)))
        P_wt_un_ful[tag]= math.log(e_alpha_t_ful/(wt_n+e_alpha_t_ful*(wt_v+1)))
        P_wt_un_less[tag]= math.log(e_alpha_t_less/(wt_n+e_alpha_t_less*(wt_v+1)))



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
                        if contain_ing(word):
                            p2 = P_wt_un_ing[tag_b]
                        elif contain_ly(word):
                            p2 = P_wt_un_ly[tag_b]
                        elif contain_ed(word):
                            p2 = P_wt_un_ed[tag_b]
                        elif contain_ness(word):
                            p2 = P_wt_un_ness[tag_b]
                        elif contain_ive(word):
                            p2 = P_wt_un_ive[tag_b]
                        elif contain_able(word):
                            p2 = P_wt_un_able[tag_b]
                        elif contain_er(word):
                            p2 = P_wt_un_er[tag_b]
                        elif contain_ful(word):
                            p2 = P_wt_un_ful[tag_b]
                        elif contain_less(word):
                            p2 = P_wt_un_less[tag_b]
                        else: p2 = P_wt_un[tag_b]
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
                            if contain_ing(word):
                                p3 = P_wt_un_ing[tag_b]
                            elif contain_ly(word):
                                p3 = P_wt_un_ly[tag_b]
                            elif contain_ed(word):
                                p3 = P_wt_un_ed[tag_b]
                            elif contain_ness(word):
                                p3 = P_wt_un_ness[tag_b]
                            elif contain_ive(word):
                                p3 = P_wt_un_ive[tag_b]
                            elif contain_able(word):
                                p3 = P_wt_un_able[tag_b]
                            elif contain_er(word):
                                p3 = P_wt_un_er[tag_b]
                            elif contain_ful(word):
                                p3 = P_wt_un_ful[tag_b]
                            elif contain_less(word):
                                p3 = P_wt_un_less[tag_b]
                            else: p3 = P_wt_un[tag_b]
                            

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
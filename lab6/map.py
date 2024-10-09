
def getProbMap(course_map, challenge):
    newMap = []
    for i in range(len(course_map)):
        newMap += [0]
    p_exact = 5/6
    p_off_1 = 0
    p_off_2 = 0
    if challenge:
        p_exact = 215/324
        p_off_1 = 25/324
        p_off_2 = 15/324
        
    for i in range(len(course_map)):
        if course_map[i]==1:
            newMap[i]+=p_exact
            i1_back = (i-1)%len(course_map)
            i1_front = (i+1)%len(course_map)
            i2_back = (i-2)%len(course_map)
            i2_front = (i+2)%len(course_map)
            newMap[i1_back]+=p_off_1
            newMap[i1_front]+=p_off_1
            newMap[i2_back]+=p_off_2
            newMap[i2_front]+=p_off_2
        else:
            newMap[i]+=1/6

    return newMap

#p_map=getProbMap([1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], True)


'''currInfo = []
curr_map=[1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(len(curr_map)):
    currInfo += [1/len(curr_map)]'''

def getLoc(pmap, obs, info):
    maxP=0
    start_guess=0
    newInfo=[]
    psum=0
    for i in range(len(pmap)):
        p=1
        for j in range(len(obs)):
            ind=(i+j)%len(pmap)
            if obs[j]==1:
                p*=pmap[ind]
            else:
                p*=(1-pmap[ind])
        p=p*info[i]
        if p>maxP:
            maxP=p
            start_guess=i
        newInfo+=[p]
        psum+=p
    normalized_info = []
    for term in newInfo:
        normalized_info+=[term/psum]

    curr_pos=(start_guess+len(obs)-1)%len(pmap)

    return curr_pos, normalized_info[start_guess], normalized_info
    

#print(currInfo)
#print(p_map)
#print(getLoc(p_map, [0, 1, 0, 1], currInfo))
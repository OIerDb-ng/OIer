cs = []
for i in open("school_oped.txt").readlines():
    cs.append(i[:-1].split(','))
def fndlcs2(s1, s2):
    m = [ [ 0 for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]
    d = [ [ None for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]
    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:
                m[p1+1][p2+1] = m[p1][p2]+1
                d[p1+1][p2+1] = 'ok'
            elif m[p1+1][p2] > m[p1][p2+1]:
                m[p1+1][p2+1] = m[p1+1][p2]
                d[p1+1][p2+1] = 'left'
            else:
                m[p1+1][p2+1] = m[p1][p2+1]
                d[p1+1][p2+1] = 'up'
    (p1, p2) = (len(s1), len(s2))
    s = []
    while m[p1][p2]:
        c = d[p1][p2]
        if c == 'ok':
            s.append(s1[p1-1])
            p1-=1
            p2-=1
        if c =='left':
            p2 -= 1
        if c == 'up':
            p1 -= 1
    s.reverse()
    return ''.join(s)
def fndlcs(s1, s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]
    mmax=0
    p=0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
                    p=i+1
    return s1[p-mmax:p]
f_file = open("fail.txt","w")
for i in open("b.txt").readlines():
    cc = i[:-1].split(',')
    if len(cc)!=3:
        print(cc)
        break
    mlen = -1
    mid = -1
    
    keywd = cc[2][:]
    l = ["中学","高中","学校","小学"]
    if "市" in keywd:
        keywd = keywd.split("市")[1]
    if "省" in keywd:
        keywd = keywd.split("省")[1]
    for i in l:
        keywd = keywd.replace(i,"")
    for j in range(len(cs)):
        cu = cs[j]
        if cc[0] != cu[0] or cc[1]!=cu[1]:
            continue
        for k in cu[2:]:
            if len(fndlcs(k,keywd)) > mlen:
                mlen = len(fndlcs2(k,keywd))
                mid = j

    print("MERGE ",cc[2]," INTO ",cs[mid],"?")
    if mlen<2:
        cop = ""
    else:
        cop = input()
    if cop == "y":
        print("MERGED ",cc[2]," INTO ",cs[mid],"!")
        cs[mid].append(cc[2])
    else:
        f_file.write(cc[0]+","+cc[1]+","+cc[2]+'\n')
f_file.close()
print(2348)
opt = open("school_new.txt","w")
for i in cs:
    opt.write("".join([j+"," for j in i])[:-1]+'\n')
opt.close()

import random as rd
def random_input():
    N = rd.randint(5, 25) # "N"umbers of fields  
    M = rd.randint(2*N, 7*N) # "M"aximum factory capacity
    m = rd.randint(N//2, M-10) # "m"inimum factory capacity  
    d = [None] * N # yiel"d"
    s = [None] * N # "s"tart day
    e = [None] * N # "e"nd day, e > s
    l = 0 # "l"ast day of all fields
    for i in range(0, N):
        d[i] = rd.randint(1, 10)
        s[i] = rd.randint(1, N//2 + 2)
        e[i] = rd.randint(s[i]+1, 3*N)
        l = max(l, e[i])
    return N, m, M, d, s, e, l
N, m, M, d, s, e, l = random_input()
print(N, m, M, d, s, e, l)
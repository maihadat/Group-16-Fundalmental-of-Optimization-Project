import random as rd
import numpy as np

def GenData(N, Y, lb, ub):
    '''--parameter: input size
       N: number of field
       Y : number of day
       lb: lower bound of d[i]
       ub: upper bound of d[i]
       --solution: a solution to make the data always solverable '''

    solution = np.zeros((N,Y))
    d = [0]*(N)
    s = [0]*(N)
    e = [0]*(N)
    for i in range(len(solution)):
        j = rd.randint(0,Y-1)
        if j != 0:
            if j - 2 > 0:
                s[i] = rd.randint(j-2,j)+1
            else:
                s[i] = 1
            e[i] = j+1

        else:
            s[i] = rd.randint(Y-2,Y-1)+1
            e[i] = Y
        d[i] = rd.randint(lb,ub)
        solution[i][j] = d[i]
    z = np.sum(solution,axis=0)
    M = int(max(z))
    if min(z) == 0:
        q = set(z)
        q.discard(min(z))
        m = int(min(q))
    else:
        m = int(min(z))
    print(solution)
    return N, M, m, d, s, e

def export_to_txt(filename,func):
    '''export the data to txt file(as the teacher's sample)'''
    N, M, m, d, s, e = func
    f = open(filename,'w')
    f.write(str(N)+' '+str(m)+' '+str(M)+ '\n')
    for i in range(N):
        f.writelines([str(d[i])+' ',str(s[i])+' ',str(e[i]) +'\n'])
    f.close()


# gen ra 7 file có số ruộng lần lượt theo lst_of_N = [5, 10, 15, 25, 50, 150, 500]
def random_gen_data_into_text_Dat():
    lst_of_N = [5, 10, 15, 25, 50, 150, 300]
    for i in range(1, 8):
        N = lst_of_N[i-1]
        Y = rd.randint(int(N/5)*2, N)
        lb = rd.randint(5, 30)
        ub = rd.randint(10, 40)
        while ub <= lb:
            ub = rd.randint(10, 25)
        export_to_txt(f'data{i}.txt', GenData(N, Y, lb, ub))


if __name__ == '__main__':
    random_gen_data_into_text()
    print(export_to_txt('data.txt',GenData(10,5,25,50)))



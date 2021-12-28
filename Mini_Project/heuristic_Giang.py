import random as rd
import time


def input(filename):  # lấy data từ file
    with open(filename) as f:
        [N, m, M] = [int(x) for x in f.readline().split()]
        d = []
        e = []
        s = []
        for i in range(N):
            r = [int(x) for x in f.readline().split()]
            d.append(r[0])
            s.append(r[1])
            e.append(r[2])
        return N, M, m, d, s, e
#end = max(e)


def production(plan):            #Biến plan là 1 list để chỉ ruộng nào cày ngày nào(VD:[1,5,2] nghĩa là ruộng 1 cày ngày 1 ruộng 2 cày ngày 5....)
    F = plan                     #Hàm production trả về năng suất của kế hoạch theo ngày(VD:[55,14,25] nghĩa là ngày 1 năng suất 55....)
    end = max(e)
    P = [0] * end
    index = 0
    if F != None:
        for i in F:
            P[i - 1] += d[index]
            index += 1
    else:
        return None
    return P


def count_violation(plan):                               #Hàm count_violation đếm số vi phạm về năng suất của các kế hoạch
    violation = 0
    a = production(plan)
    if a != None:
        for i in range(0, len(a)):
            if ((a[i] > M or a[i] < m) and a[i] != 0):
                violation += 1
    else:
        return None
    return violation


def first_plan():                                        #Hàm chọn random 1 kế hoạch nào đó
    F = [0] * N
    for i in range(0, N):
        F[i] += rd.randint(s[i], e[i])
    return F


def change_of_plan(y):                                   #Hàm chọn ra kế hoạch không có vi phạm
    a = y                                                 #Đoạn leo đồi t đang để random nên có vẻ không hiệu quả lắm, nếu có ý tưởng gì
    c = y                                                 #tốt nhắc t
    b = count_violation(c)
    for i in range(0, 100000000):
        ra = rd.randint(0, N - 1)
        c[ra] = rd.randint(s[ra], e[ra])
        d = count_violation(c)
        if d < b:
            a = c
            b = d
        if d == 0:
            return a
    if d != 0:
        f = first_plan()
        change_of_plan(f)

def grand_change_of_plans():                               #Hàm chọn ra kế hoạch có chênh lệch giữa năng suất lớn nhất và năng suất nhỏ nhất  thấp nhất
    r = M
    true_plan = None
    start = time.time()
    while True:
        if time.time() - start > 60:
            return true_plan
        pl = change_of_plan(first_plan())
        pr = production(pl)
        pr.sort()
        w = 0
        for j in pr:
            if j != 0:
                w = j
                break
        l = (max(pr)-w)
        if l < r:
            r = l
            true_plan = pl
    return true_plan


if __name__ =='__main__':
    filename =  'MyData/data0.txt'
    N, M, m, d, s, e =  input(filename)
    end = max(e)
    c = grand_change_of_plans()
    print(c)
    print(production(c))
    #print(count_violation(c))
#giải
#c=grand_change_of_plans()
#print(c)
#print(production(c))
#print(count_violation(c))
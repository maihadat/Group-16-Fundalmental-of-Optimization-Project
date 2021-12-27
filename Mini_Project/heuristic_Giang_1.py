import time
from datetime import timedelta, datetime



def input(filename):                                                  #lấy data từ file
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


def heuristic(filename):

    N, M, m, d, s, e = input(filename)
    starttime =  time.time()
    end=max(e)

    R = []                                                  #Tạo ma trận 3D tên D chứa thông tin về những cánh đồng có thể cày từng ngày,
    F = []                                                  #năng suất của các cánh đồng, và số thứ tự của cánh đồng
    D = []
    for i in range(1,end+1):
        for j in range(1,N+1):
            if (i>=s[j-1] and i<=e[j-1]):
                R.append(d[j-1])
                R.append(j)
                F.append(R)
                R=[]
        D.append(F)
        F=[]

    total=[0]*end                                          #Tìm giá trị trung bình medium.
    for i in range(0,end):                                  #Giá trị này bằng với giá trị thấp nhất của tất cả tổng năng suất trong 1 ngày
        Ds = D[i]                                           #Trường hợp giá trị thấp nhất nhỏ hơn m, đặt giá trị trung bình bằng m
        Ds.sort(reverse=True)
        for j in range(0,len(D[i])):
            total[i]+=Ds[j][0]
    total.sort()
    medium=total[0]
    if medium<m:
        medium=m


    pro=[0]*end                                           #Lập danh sách năng suất cho từng ngày và danh sách cày ruộng cho từng ngày
    proplan=[0]*end                                       #Chọn ruộng cày theo thứ tự năng suất thấp nhất đến cao nhất
    b_medium=[0]*end                                      #Lưu 2 giá trị: giá trị năng suất trước khi vượt qua và sau khi vượt qua giá trị trung bình
    a_medium=[0]*end                                      #Trong 2 giá trị: Lựa chọn giá trị gần với giá trị trung bình hơn
    b_medium_field=[]
    a_medium_field=[]
    b_medium_fieldcopy=[]
    a_medium_fieldcopy=[]
    for i in range(0,end):

        Ds=D[i]
        Ds.sort(reverse=False)
        for j in range(0,len(D[i])):
            b_medium[i]=pro[i]
            pro[i]+=Ds[j][0]
            if pro[i]>=medium:
                a_medium[i]=pro[i]
                a_medium_fieldcopy.append(Ds[j][1])
                break
            if pro[i]<medium:
                b_medium_fieldcopy.append(Ds[j][1])
                a_medium_fieldcopy.append(Ds[j][1])
        b_medium_field.append(b_medium_fieldcopy)
        a_medium_field.append(a_medium_fieldcopy)
        b_medium_fieldcopy=[]
        a_medium_fieldcopy=[]
        if (a_medium[i]-medium>medium-b_medium[i]):
            pro[i]=b_medium[i]
            proplan[i]=b_medium_field[i]
        elif a_medium[i]-medium<=medium-b_medium[i]:
            pro[i]=a_medium[i]
            proplan[i]=a_medium_field[i]


    endtime = time.time()
    runtime = endtime - starttime
    return pro, proplan, runtime

def get_solution(pro):
    print(pro)
    for i in range(0,len(pro)):                                                 #In lời giải: năng suất từng ngày
        print('Sản lượng ngày %i là %i'%((i+1),pro[i]))

def specific_solution(proplan):                                                 #In lời giải: danh sách cày ruộng
    for i in range(0,len(proplan)):
        for j in proplan[i]:
            print('Ngày %i cày ruộng %s'%((i+1),j))

#Giải:
# Main
#filename = 'MyData\data.txt'
#pro, proplan, runtime = heuristic(filename)
#get_solution(pro)
#specific_solution(proplan)
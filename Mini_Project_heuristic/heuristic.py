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

medium=m                                                                     #lấy giá trị trung bình medium. medium = m


dumpsteri=[]
dumpster=[]
pro=[0]*end                                                                  #Lập danh sách năng suất cho từng ngày và danh sách cày ruộng cho từng ngày
proplan=[0]*end                                                              #Chọn ruộng cày theo thứ tự năng suất  từ thấp nhất đến cao nhất
b_medium=[0]*end                                                             #Lưu 2 giá trị: giá trị năng suất trước khi vượt qua và sau khi vượt qua giá trị trung bình
a_medium=[0]*end                                                             #Trong 2 giá trị: Lựa chọn giá trị gần với giá trị trung bình hơn
b_medium_field=[]
a_medium_field=[]
b_medium_fieldcopy=[]
a_medium_fieldcopy=[]
for i in range(0,end):
    n=0
    Ds=D[i]
    Ds.sort(reverse=False)
    for j in range(0,len(D[i])):
        if Ds[j][1] not in dumpster:                                            #Tên biến: Năng suất: pro
            b_medium[i]=pro[i]                                                  #Năng suất trước khi vượt qua m:b_medium
            pro[i]+=Ds[j][0]                                                    #Năng suất sau khi vượt qua m:a_medium
            dumpsteri.append(Ds[j][1])
            dumpster.append(Ds[j][1])
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
    if a_medium[i]==0 and b_medium[i]>m:
        pro[i]=b_medium[i]
        dumpster.pop()
    if a_medium[i]-medium<medium-b_medium[i] and b_medium[i]>m:
        pro[i]=b_medium[i]
        dumpster.pop()
        proplan[i]=b_medium_field[i]
    elif a_medium!=0:
        pro[i]=a_medium[i]
        proplan[i]=a_medium_field[i]
    else:
        pro[i]=0
        proplan[i]=[]
        for k in dumpsteri:
            dumpster.remove(k)
    dumpsteri=[]



def get_solution():
    print(pro)
    for i in range(0,len(pro)):                                                 #In lời giải: năng suất từng ngày
        print('Sản lượng ngày %i là %i'%((i+1),pro[i]))

def specific_solution():                                                        #In lời giải: danh sách cày ruộng
    for i in range(0,len(proplan)):
        for j in proplan[i]:
            print('Ngày %i cày ruộng %s'%((i+1),j))

#Giải:
#input()
#get_solution()
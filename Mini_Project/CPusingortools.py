from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import numpy as np
import MyData as da
import random as rd
import time

def input(filename):
    '''lấy input từ file data'''
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

class LapKeHoachThuHoachNongSan():
    def __init__(self):
        #data
        self.__N = 0
        self.__M = 0
        self.__m = 0
        self.__d = []
        self.__s = []
        self.__e = []
        #solution
        [self.__x, self.__y, self.z, self.t] = [0, 0, 0, 0]
        self.__solution = 0
        #time
        self.time = 0

    def __Modelling(self):
        '''Tạo model cho bài toán Lập kế hoạch thu hoạch nông sản'''
        model = cp_model.CpModel()

        #Variable
        x = [model.NewIntVar(self.__s[k], self.__e[k], 'x[' + str(k+1) + ']') for k in range(self.__N)] # ngày thu hoạch cánh đồng k
        y = [model.NewIntVar(0, self.__M, 'y[' + str(i+1) +']')for i in range(max(self.__e))]  # sản lượng ngày i
        z = model.NewIntVar(self.__m, self.__M, 'z')   # biến trung gian tính chênh lệch sản lượng giữa các ngày
        t = model.NewIntVar(self.__m, self.__M, 't')
        c = [model.NewBoolVar('c[%r]'%(i+1)) for i in range(max(self.__e))]  # biến binary cho mệnh đề y[i] thuộc [self.m, self.M] hoặc y[i] = 0
        #Constraint

        #y[i] = sigma( (X[k] = i), d[k]))
        for i in range(max(self.__e)):
            b = [model.NewBoolVar('b[%r]' %(k+1)) for k in range(self.__N)] #biến binary cho mệnh đề X[k] ==i
            for k in range(self.__N):
                c1 = model.Add(x[k] == i+1).OnlyEnforceIf(b[k])
                c2 = model.Add(x[k] != i+1).OnlyEnforceIf(b[k].Not())
            c3 = model.Add(y[i] == sum(self.__d[k] * b[k] for k in range(self.__N))) #(y[i] == sigma(d[k]) với k thỏa mãn biến b)
            c4 = model.Add(y[i] >= self.__m).OnlyEnforceIf(c[i])
            c5 = model.Add(y[i] == 0).OnlyEnforceIf(c[i].Not())
            c7 = model.Add(t <= y[i]).OnlyEnforceIf(c[i])   # t = min(y) và t != 0

        c0 = model.AddMaxEquality(z, [y[i] for i in range(max(self.__e))])#(z = max(y))

        #Objective function
        model.Minimize(z-t)

        return [model, x, y, z, t]

    def Solver(self):
        '''tạo solver cho bài toán bằng Ortools'''

        [self.__x, self.__y, self.z, self.t] = self.__Modelling()[1:]
        model = self.__Modelling()[0]

        start = time.time()
        #create solver
        solver = cp_model.CpSolver()

        solver.parameters.max_time_in_seconds = 1800.0

        status = solver.Solve(model)
        end = time.time()
        self.time = end - start

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print('Thu hoạch thành công!')
            self.t = solver.Value(self.t)
            self.z = solver.Value(self.z)
            self.__x = [solver.Value(self.__x[i]) for i in range(self.__N)]
            self.__y = [solver.Value(self.__y[i]) for i in range(max(self.__e))]
            self.__solution = np.zeros((len(self.__x), len(self.__y)))
            for i in range(len(self.__y)):
                for j in range(len(self.__x)):
                    if i+1 == self.__x[j]:
                        self.__solution[j][i] = self.__d[j]
                    else:
                        self.__solution[j][i] = 0
            return self.z, self.__x, self.__y, self.__solution, self.time, self.t
        else:
            print('Thu hoạch thất bại do không đáp ứng đủ điều kiện!')



    def getInput(self, N: 0, M: 0, m: 0, d: list(), s: list(), e: list()):
        ''' N: int: số lượng cánh đồng cần thu hoạch
            M: int: sản lượng tối đa trong 1 ngày
            m: int: sản lượng tối thiểu trong 1 ngày
            d: list: sản lượng các thửa ruộng lần lượt
            s,e: list: ngày bắt đầu và kết thúc của các thửa ruộng lần lượt
            Lấy dữ liệu cho bài toán '''

        self.__N = N
        self.__M = M
        self.__m = m
        self.__d = d
        self.__s = s
        self.__e = e

    def printSolution(self):
        '''in lời giải tối ưu'''
        if isinstance(self.__x[0], int):
            for i in range(len(self.__x)):
                print('Cánh đồng %i thu hoạch vào ngày %i'%(i+1, self.__x[i]))
            print()
            for i in range(len(self.__y)):
                print('Sản lượng ngày %i là %i'%(i+1, self.__y[i]))


    def Visualization(self):
        '''visualization lời giải'''
        if isinstance(self.__solution, np.ndarray):
            plt.style.use('classic')
            plt.figure(figsize=(9, 7.5))
            bd1 = plt.subplot()

            data = np.array([i for i in self.__solution])
            bottom = np.cumsum(data, axis=0)
            index = np.arange(1, len(self.__y)+1)
            bd1.bar(index, self.__solution[0], width = 0.5, label = 'Cánh đồng 1')
            for i in range(1, len(self.__x)):
                bd1.bar( index, self.__solution[i],
                         width = 0.5, label = 'Cánh đồng %i' %(i+1),
                         bottom = bottom[i-1],
                         color = (rd.randint(0,255)/255, rd.randint(0,255)/255, rd.randint(0,255)/255))
            plt.suptitle('Biểu đồ thu hoạch nông sản', fontsize = '20')
            plt.axis([0, len(self.__y)+1, 0, (max(self.__y)*1.5)])

            for i in range(len(self.__y)):
                plt.text(i-0.04+1, self.__y[i]+0.2, self.__y[i])

            plt.xlabel('Ngày', fontsize = '15')
            plt.ylabel('Sản lượng', fontsize = '15')

            #chú thích
            plt.legend(loc='best')
            plt.show()


if __name__ == '__main__':
    n = '0'
    filename = 'MyData\data%s.txt'%(n)
    #da.export_to_txt(filename, da.GenData(50,40,25,50)) #tạo file test vs tên file như trên :)))
    N, M, m, d, s, e = input(filename)
    K = LapKeHoachThuHoachNongSan()
    K.getInput(N, M, m, d, s, e)
    K.Solver()
    K.printSolution()
    K.Visualization()

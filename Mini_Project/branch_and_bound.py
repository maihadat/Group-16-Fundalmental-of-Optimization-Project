import CPusingortools as cp
import time

def min_diff_zero(l :list):
    minmin = 999999999
    for i in l:
        if i < minmin and i != 0:
            minmin = i
    return minmin


def Branch(k :int):
    global f_max_opt, f, x, f_min_opt, start

    if time.time()-start > 1800:
        return

    for v in range(1,max(e)+1):
        if v in [i for i in range(s[k-1], e[k-1]+1)]:
            x[k] = v
            f[v] += d[k-1]
            if k == N:
                if max(f) <= f_max_opt and min_diff_zero(f) >= f_min_opt:
                    f_max_opt = max(f)
                    f_min_opt = min_diff_zero(f)
                    print(f,x)
                    z.append([f.copy(),x.copy()])

            else:
                #lower bound
                g = max(f)
                #upper bound
                h = min_diff_zero(f) + (sum(d) -sum(f))
                if g <= f_max_opt and h >= f_min_opt:
                    Branch(k+1)
            f[v] -= d[k-1]



def BranchAndBound(filename):
    '''Branch and bound algorithm'''
    global f_max_opt, f, x, f_min_opt ,d, e, s, z, N, start
    start = time.time()
    N, M, m, d, s, e = cp.input(filename)

    z = []
    x = [0]*(N+1)
    f = [0]*(max(e)+1)
    f_max_opt = M
    f_min_opt = m
    Branch(1)
    end = time.time()
    # f_max_opt là hàm f* nếu các ông cho vào bảng nha
    # z là tập các kết quả tìm được, các ông cứ lấy cái đầu cho chắc
    # end-start là thời gian chạy, tôi cx time limit luôn r nha
    return f_max_opt, f_min_opt, z, end-start

def PrintSolution(func):
    f_max_opt, f_min_opt, z, time = func
    print(time)
    if len(z) != 0:
        for i in range(1, len(z[-1][1])):
            print('Thửa ruộng %i cày ngày %i'%(i,z[-1][1][i]))
        print()
        for i in range(1, len(z[-1][0])):
            print('Sản lượng ngày %i là %i'%(i,z[-1][0][i]))
    else:
        print('Cannot solve')

if __name__ == '__main__':
    # Tùy chỗ ông lưu file mà chỉnh directory nha
    filename = 'MyData\data0.txt'
    # Dùng hàm BranchAndBound(filename) để lấy dữ liệu nha
    # BranchAndBound(filename)
    PrintSolution(BranchAndBound(filename))
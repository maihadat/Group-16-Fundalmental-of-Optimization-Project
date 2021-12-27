
import time
from ortools.linear_solver import pywraplp


def read_file(filename):
    d, s, e = [], [], []
    with open(filename) as f:
        N, m, M = [int(x) for x in f.readline().strip().split()]
        for i in range(N):
            tmp1, tmp2, tmp3 = [int(x) for x in f.readline().strip().split()]
            d.append(tmp1)
            s.append(tmp2)
            e.append(tmp3)
    return N, m, M, d, s, e
'''
hàm đọc file và trả về tương ứng là:
    + N: số lượng ruộng
    + m: công suất tối thiểu để nhà máy hoạt động
    + M: công suất tối đa của nhà máy
    + d: vector công suất cần để xử lí các ruộng
    + s: vector ngày khởi đầu của chuỗi ngày có thể khai thác ruộng
    + e: vector ngày kết thúc của chuỗi ngày có thể khai thác ruộng
'''


# hàm lấy vào 1 file name và các biến boolean cho việc có in ra kế hoạch, hàm mục tiêu, thời gian chạy thuật toán
def vegetables_planning(filename, print_out_plan, print_out_objective, print_out_time):
    start = time.time()
    N, m, M, d, s, e = read_file(filename)
    # J là ngày cuối cùng có thể thu hoạch ruộng
    J = max(e)
    # L là số cực lớn để có thể sử dụng cho rằng buộc 4
    L = sum(d)

    # Set variables
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    solver.set_time_limit(1800000)

    x = [[solver.IntVar(0.0, 1.0, 'x(' + str(i) + ',' + str(j) + ')') for j in range(1, J + 1)]
         for i in range(1, N + 1)]
    y = [solver.IntVar(0.0, M, 'y(' + str(j) + ')') for j in range(1, J + 1)]
    z = solver.IntVar(m, M, 'z')
    c = [solver.IntVar(0.0, 1.0, 'c(' + str(j) + ')') for j in range(1, J + 1)]
    t = solver.IntVar(m, M, 't')
    '''
    x[i][j] là biến nhị phân biểu thị ngày j thì ruộng i có được thu hoạch hay ko
    y[j] là biến công suất của ngày thứ j, y[j] có thể = 0 với c[j] = 0 và thuộc khoảng từ m đến M nếu biến c[j] = 1
    z là biến để rằng buộc mọi ngày có công suất đều nhau nhất có thể và là biến cần tối ưu
    c[j] là biến nhị phân biểu thị ngày [j] có thu hoạch hay ko
    '''

    # Constraint
    # con1: sigma(x[i][j]) = 1 với mọi i thuộc N --- Mỗi cánh đồng chỉ thu hoạch 1 lần

    for i in range(N):
        con1 = solver.Constraint(1.0, 1.0)
        for j in range(J):
            con1.SetCoefficient(x[i][j], 1)

    # con2: sigma(x[i][j]) = 1 với mọi j thuộc khoảng từ s[i] -> e[i] --- Mỗi cánh đồng i chỉ có thể thu hoạch trong những ngày thuộc khoảng s[i] đến e[i]
    for i in range(1, N + 1):
        con2 = solver.Constraint(1.0, 1.0)
        for j in range(s[i - 1], e[i - 1] + 1):
            con2.SetCoefficient(x[i - 1][j - 1], 1)

    # con3: sigma(x[i][j]) = 0 với mọi j thuộc khoảng từ 1 -> s[i]-1 và từ e[i]+1 -> J --- Mỗi cánh đồng ko thể thu hoạch ngoài khoảng s[i] đến e[i]
    '''
    for i in range(1, N + 1): (con bị sai)
        con3 = solver.Constraint(0.0, 0.0)
        for j in range(s[i - 1]):
            con3.SetCoefficient(x[i - 1][j - 1], 1)
        for j in range(e[i - 1] + 1, J + 1):
            con3.SetCoefficient(x[i - 1][j - 1], 1)
    '''
    # con4: rằng buộc dạng tuyến tính của ( nếu c[j] = 0 thì y[j] = 0 và nếu c[j] = 1 thì y[j] >= m )
    for j in range(J):
        solver.Add(y[j] <= c[j] * 10 * L)

    for j in range(J):
        solver.Add(y[j] - c[j] * m >= 0)

    # con5: y[j] = sigma(x[i][j] * d[i]) với mọi j thuộc J --- Tổng công suất cần xử lý của ngày thứ j
    for j in range(J):
        con5 = solver.Constraint(0, 0)
        con5.SetCoefficient(y[j], -1)
        for i in range(N):
            con5.SetCoefficient(x[i][j], d[i])

    # con6: Rằng buộc để cân bằng công suất các ngày bằng cách cho z-t min
    for j in range(J):
        solver.Add(z-y[j] >= 0)

    for j in range(J):
        solver.Add(y[j] - t + L*10 - c[j]*L*10 >= 0)

    obj = solver.Objective()
    obj.SetCoefficient(z, 1)
    obj.SetCoefficient(t, -1)
    obj.SetMinimization()

    status = solver.Solve()
    end = time.time()

    if status == pywraplp.Solver.OPTIMAL and print_out_plan is True:
        for j in range(J):
            tmp = []
            for i in range(N):
                if x[i][j].solution_value() == 1:
                    tmp.append(i+1)
            if len(tmp) != 0:
                print(f'Ngày thứ {j + 1} cần thu hoạch những ruộng', tmp,
                      f'với công suất của nhà máy là {int(y[j].solution_value())}')
            else:
                print(f'Không thu hoạch ngày thứ {j + 1}')
            if j == J-1:
                print()
    else:
        print('Không có kế hoạch tối ưu')
        print()

    if print_out_objective is True:
        print('Hàm tối ưu z là:', z.solution_value())
        print()

    if print_out_time is True:
        print('Thời gian hoàn thành thuật toán là:', end-start)
        print()
    return (z.solution_value(), end-start)


vegetables_planning("MyData\data4.txt", True, True, True)



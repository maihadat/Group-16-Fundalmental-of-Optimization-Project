import CPusingortools as cp
import MyData as da
import heuristic_Giang as h
import Vegetables_planning_using_MIP_Dat as vp
import branch_and_bound as bnb

import pandas as pd
import matplotlib.pyplot as plt


def Analysis_and_Comparison_Data_Table(filelist: list):
    '''The table for analyzing and comparing'''
    cp_data, mip_data, h_data, bnb_data = [], [], [], []
    for filename in filelist:
        #BranchAndBound
        f_max_opt, f_min_opt, z, time = bnb.BranchAndBound(filename)
        bnb_data.append((f_max_opt, time))


        #Heuristic (chờ ông Giang sửa xong code)
        pro, proplan, runtime = h.heuristic(filename)
        #f h.timelimit < 1800:
        h_data.append((max(pro), runtime))

        #Cp_model
        N, M, m, d, s, e = cp.input(filename)
        k = cp.LapKeHoachThuHoachNongSan()
        k.getInput(N, M, m, d, s, e)
        k.Solver()
        if k.time < 1801:
            cp_data.append((k.z, k.time))
        else:
            cp_data.append((None, None))

        #Mip_model
        tmp = vp.vegetables_planning(filename, False, False, False)
        if tmp[1] < 1801:
            mip_data.append(tmp)
        else:
            mip_data.append((None, None))

    data = {
            'Constraint Programming': cp_data,
            'Mixed Integer Programming': mip_data,
            'Heuristic': h_data,
            'Branch And Bound': bnb_data
            }
    df = pd.DataFrame(data, index = ['Data %i'%(i+1) for i in range(len(filelist))])
    print(df)
    return df

def Visualize(df):
    #define table and
    ax = plt.subplot()

    #create table
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    #modify table
    table.set_fontsize(14)
    table.scale(1, 1)
    ax.axis('off')

    #display table
    plt.show()


if __name__ == '__main__':

    filelist = ['MyData\data.txt', 'MyData\data1.txt', 'MyData\data2.txt']
    #filelist = ['MyData\data%i.txt'%(i) for i in range(20)]

    Analysis_and_Comparison_Data_Table(filelist)
    Visualize(Analysis_and_Comparison_Data_Table(filelist))






import CPusingortools as cp
import MyData as da
import heuristic_Giang as h
import Vegetables_planning_using_MIP_Dat as vp
import branch_and_bound as bnb
import time

import pandas as pd
import matplotlib.pyplot as plt


def Analysis_and_Comparison_Data_Table(filelist: list):
    '''The table for analyzing and comparing'''

    cp_data, mip_data, h_data, bnb_data = [], [], [], []
    for filename in filelist:
        N, M, m, d, s, e = cp.input(filename)
        #BranchAndBound
        f_max_opt, f_min_opt, z, tim = bnb.BranchAndBound(filename)
        #bnb_data.append((f_max_opt - f_min_opt, tim))
        bnb_data.append((f_max_opt-f_min_opt)/sum(d))



        #Heuristic
        start = time.time()
        h.N, h.M, h.m, h.d, h.s, h.e =  N, M, m, d, s, e
        c = h.grand_change_of_plans()
        end = time.time()
        #h_data.append((max(h.production(c))-bnb.min_diff_zero(h.production(c)), end - start))
        h_data.append((max(h.production(c)) - bnb.min_diff_zero(h.production(c)))/sum(d))

        #Cp_model

        k = cp.LapKeHoachThuHoachNongSan()
        k.getInput(N, M, m, d, s, e)
        k.Solver()
        if k.time <= 1800:
            #cp_data.append((k.z - k.t, k.time))
            cp_data.append((k.z - k.t)/sum(d))
        else:
            cp_data.append((None, None))

        #Mip_model
        if vp.vegetables_planning(filename, False, False, False)[1] <= 1800:
            #mip_data.append((vp.vegetables_planning(filename, False, False, False)[0]-vp.vegetables_planning(filename, False, False, False)[1],vp.vegetables_planning(filename, False, False, False)[2])
            mip_data.append((vp.vegetables_planning(filename, False, False, False)[0]-vp.vegetables_planning(filename, False, False, False)[1])/sum(d))
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
    #filelist = ['MyData\data.txt', 'MyData\data1.txt']
    filelist = ['MyData\data%i.txt'%(i) for i in range(3)]

    Analysis_and_Comparison_Data_Table(filelist)
    Visualize(Analysis_and_Comparison_Data_Table(filelist))
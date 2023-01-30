import cProfile
import pstats
from pstats import SortKey
import sys
from myEDA import myEDA

import pandas as pd
import time
import os
import copy

def eda():
    path = sys.path[0]+"/FSPS"

    os.chdir(path)
    df_list = []
    file = "tai-20-5-1.txt"
    #w2 = pd.ExcelWriter(sys.path[0]+"/Results/qap*tai-20-5-2.xlsx" ) 
    for i in range(1):#file in os.listdir():
        prob = f"{path}/{file}"
        w = pd.ExcelWriter(sys.path[0]+"/Results/"+ file +".xlsx" ) 

        #algo = myEDA(el[0],el[1],el[2],el[3])
        
        
        results = []
        start = time.time()
        algo = myEDA(prob)
    
        
        x,y,z= algo.run_myEDA(2400)
        print(time.time()-start)
        result = {
                "Solution":x,
                "Fitness":y,
                "ARPD":z
            }
        
        results.append(copy.deepcopy(result))
        df = pd.DataFrame.from_records(results)   
    
        end_time = time.time()
        df_list.append(df)
    
        
        for i, df in enumerate(df_list):
            df.to_excel(w)
        
    w.save()
if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()   
    eda()
    pr.disable()
    p = pstats.Stats()
    pr.print_stats()
'''
print('***********************************************************************')
df_list1 = []
for file in os.listdir():
    prob = f"{path}/{file}"
 
    #algo = myEDA(el[0],el[1],el[2],el[3])
    
    
    resulta = []
    for i in range(1):
        
        
        algo = myHEDA(prob)
        
        
    
        start_time = time.time()
        sol,fitness,vns_sol,fitness_vns = algo.run_myEDA(2400)
        result = {
                "Solution_EDA":sol,
                "Fitness_EDA":fitness,
                "Solution_HEDA":vns_sol,
                "Fitness_HEDA":fitness_vns,
                "sheet": file
            }
        
        resulta.append(copy.deepcopy(result))
    df1 = pd.DataFrame.from_records(resulta)   
   
    end_time = time.time()
    df_list1.append(df1)
   
    
for i, df1 in enumerate(df_list1):
   
    df1.to_excel(w2, sheet_name=df1.iloc[0,4])
   
w2.save()
'''


import cProfile
import pstats
from pstats import SortKey
import sys
from umda import umda

import pandas as pd
import time
import os
import copy

def eda():
    path = sys.path[0]+"/FSPS"

    os.chdir(path)
   
    
    files = [["tai-20-10-1.txt"],
            ["tai-20-10-2.txt"],
            ["tai-20-10-3.txt"],
            ["tai-20-10-4.txt"],
            ["tai-20-10-5.txt"],
            ["tai-20-10-6.txt"],
            ["tai-20-10-7.txt"],
            ["tai-20-10-8.txt"],
            ["tai-20-10-9.txt"],
            ["tai-20-10-10.txt"]]
            
    #w2 = pd.ExcelWriter(sys.path[0]+"/Results/qap*tai-20-5-2.xlsx" ) 
    for file in files:
        results = []
        for i in range(10):#file in os.listdir():
            prob = f"{path}/{file[0]}"
        

            #algo = myEDA(el[0],el[1],el[2],el[3])
            
            
            
            start = time.time()
            algo = umda(prob)
        
            
            x,y,z = algo.Run()
            print(time.time()-start)
            result = {
                    "Solution":x,
                    "Fitness":y,
                    "ARPD": z
                }
            
            results.append(result)
        df = pd.DataFrame.from_records(results)
        df.to_csv(sys.path[0]+"/Results3/"+file[0].split(".")[0]+".csv")
            
    
if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()   
    eda()
    pr.disable()
    p = pstats.Stats()
    pr.print_stats()

import copy

import numpy as np
from numba import njit, prange
import hello

class fssp:

    
    def __init__(self, path):
        #self.processingTimes = None
        self.path = path
        self.FEs = 0
        f = open(path, "r")

        doc = f.read()
        
        lines = np.array(doc.split("\n"))
        
        

        values  = lines[1].split()
        jobs = int(values[0])
        self.problem_size = jobs
        
                    
            
        machines = int(values[1])
       
        self.stop_crit = self.problem_size * self.problem_size *1000
           
                
                
                
       
        
        self.optimum = int(values[3])

        processingTimes = []

        for i in range(len(lines)):
            values  = lines[i].split()
            if((i > 2) and (i <= (machines + 2))):
                arr = []
                for j in range(jobs):
                    val = int(values[j])
                    arr.append(val)
                processingTimes.append(arr)
        self.processingTimes = np.array(copy.deepcopy(np.transpose(processingTimes)),  dtype= np.int32)
        self.probSize = jobs
    
    def evaluate( self,ind):
        self.FEs = self.FEs + 1
        solution = ind #convert random key representation to permutation representation
        
      #  times = np.loadtxt(self.path, dtype = int)
     #   self.processingTimes = np.transpose(self.processingTimes)
        n_jobs,n_machines = self.processingTimes.shape
        completion_times = np.zeros(self.processingTimes.shape)
        completion_times[0, :]=np.cumsum(self.processingTimes[solution[0],:])
        completion_times[:, 0] = np.cumsum(self.processingTimes[solution, 0])
        for j in np.arange(1,n_jobs):
            for m in np.arange(1,n_machines):
                completion_times[j,m] = self.processingTimes[solution[j], m] + max(completion_times[j,m-1],completion_times[j-1,m])

        fits = completion_times.tolist()
        return fits[n_jobs-1][n_machines-1]
    
    def evaluate_vns( self,ind):
        ind = np.array(ind, dtype=np.int32)
        self.FEs = self.FEs + 1

        '''
        solution = ind#convert random key representation to permutation representation
        self.FEs = self.FEs + 1
       
        n_jobs,n_machines = self.processingTimes.shape
        completion_times = np.zeros(self.processingTimes.shape)
        completion_times[0, :]=np.cumsum(self.processingTimes[solution[0],:])
        completion_times[:, 0] = np.cumsum(self.processingTimes[solution, 0])
        for j in np.arange(1,n_jobs):
            for m in np.arange(1,n_machines):
                completion_times[j,m] = self.processingTimes[solution[j], m] + max(completion_times[j,m-1],completion_times[j-1,m])

        fits = completion_times.tolist()
        return fits[n_jobs-1][n_machines-1]
     '''
        return hello.evaluate_vnsms(ind, self.processingTimes)

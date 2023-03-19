
import random
import math
import time
import numpy as np
import copy
from ProblemFSSPms import fssp

class umda:
    def __init__(self, path) :
        
       
        self.path = path
        self.p = fssp(self.path)
       
        self.problem_size = self.p.problem_size
        self.population_size = self.problem_size *10
        self.selection_size = int(self.problem_size *5)
     
        
    def normalize(self,probs):
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]


    def SampleOffspring(self, P_global):
        P = copy.deepcopy(P_global)
        identity = list(range(len(P)))
        offspring = [None]*len(P)

        for i in range(len(offspring)):
            p = P[i]
            element = np.random.choice(identity,p=p)
            offspring[i] = element
        

            # Normalize probability vector for selected element
            for index in range(i+1,len(P)):
                P[index][element] = 0
                P[index] = self.normalize(P[index])
            
        return offspring



    def Run(self, epsilon = 0.05):
    
    
        # Permutation size
        n = self.problem_size

        # Population size
        population_size = self.population_size

        # Sample size
        sample_size = population_size

        # Epsilon
        # epsilon = 0.1

        t = 0
        # Generate N points randomly 
        population = [None] * population_size
        new_sample = [None] * sample_size

        # Probabilities
        P = [[1/n]*n for _ in range(n)]

        best_permutation = None
        best_fitness = None

        
        while self.p.FEs < self.p.stop_crit:
            
            for j in range(sample_size-1):
                individual = self.SampleOffspring(P)
                fitness = self.p.evaluate(individual)
                new_sample[j] = (fitness, individual)
                
                if best_fitness is None:
                    best_permutation = [i for i in individual]
                    best_fitness = fitness
            

                    
            new_sample[sample_size-1] = (best_fitness, best_permutation)
            new_sample = sorted(new_sample, key = lambda t:(t[0],random.random()))
            population = new_sample[:self.selection_size]
            
            if population[0][0]<best_fitness:
                best_permutation = [i for i in population[0][1]]
                best_fitness = population[0][0]

            # Update probabilities
            for i in range(n):
                P[i] = [epsilon]*n
                
                for s in population:
                    P[i][s[1][i]] += 1 
                
                P[i] = self.normalize(P[i])


    
        print(best_fitness)
        # Return best permutation and its fitness
        return best_permutation, best_fitness , (best_fitness - self.p.optimum)*100/self.p.optimum






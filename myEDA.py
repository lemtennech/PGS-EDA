
from ProblemFSSPms import fssp
import numpy as np
import random
from Model1 import  Model
import copy

import hello

        
class myEDA:
    def __init__(self, path) :
        
       
        self.path = path
        self.p = fssp(self.path)
       
        self.problem_size = self.p.problem_size
        self.population_size = self.problem_size *10
        self.selection_size = int(self.problem_size *5)
     
        
        
      
        self.model = Model(self.problem_size, self.selection_size,0.005)
        
        
        
    '''   
    def selection(self, population, selection_size):
        population.sort()
        population.reverse()   # for LOP
        selected_set = population[0: selection_size]
       
        return selected_set

        selected = [population[0]]
        temp = [population[0].distfit]
        for ind in population:
            if ind.distfit not in temp:
                selected.append(ind)
                temp.append(ind.distfit)
                
                        
            if len(selected) >= selection_size:
                
                break
       # selected_set = selected[0:selection_size]
        
       
        
        
        return selected[0:selection_size]
    
    def mechanism(self, population):
        for element in population:
            if element.distfit == self.best_solution.distfit:
                continue
            for k in range(3):
                i,j = random.randint(0,self.problem_size-1) ,random.randint(0,self.problem_size-1)
            
                element.individual = self.vns.swap(element.individual,i,j)
                element.distfit = self.p.evaluate(element)
          
        return population
    
    def distance(self, best, sol):
        distance = 0
        
        for i in range(self.problem_size):
            if best[i]!=sol[i]:
                distance = distance+1
        return distance
     
    def in_population (self, population, offspring):
        check = False
        
        for element in population:
            if self.distance(element, offspring) == 0:
                check = True
                
                break
        
        check = any(np.equal(population,offspring).all(1))
        
        return check
    '''
    def replacement(self, population , offspring):
        
      #  population = sorted(population, key = lambda t:(t[-1],random.random()))
      #  population = np.array(population)
      #  population = population[population[:,-1].argsort()]
        worst = population[-1]
        
        if offspring[-1] > worst[-1]:
            return population 
        elif not any(np.equal(population,offspring).all(1)):
            
           # population.append(offspring)
           # population.remove(worst)
            population = np.insert(population, 0, offspring, axis = 0)
           
            
            population= np.delete(population,-1, axis=0)
           
          
           
        return population
    
    def initial_population(self):
        pop = [[i for i in np.random.permutation(self.problem_size)] 
              for _ in range(self.population_size)]

        population = []
        for ind in pop:
            ind = np.append(ind,0)
          #  ind = np.append(ind,int(self.p.evaluate_vns(ind)))
            ind[-1] = self.p.evaluate_vns(ind)
        
            population.append(ind)
        return population
            
    def run_myEDA(self, max_gen):
        
        
        population = self.initial_population()
        self.best_solution = population[0]     
       
        while self.p.FEs < self.p.stop_crit:
            
            population = sorted(population, key = lambda t:(t[-1],random.random()))

            population = population[0:self.selection_size]
            temp = population[-1][-1]
            '''
            for el in population[0:self.selection_size]:
               
                el = np.delete(el,np.where(el==el[-1]))
                self.selected_set.append(el)
            '''
            
            model1 = self.model.createModel1(np.array(population))
            #model2 = model.createModel2(np.array(self.selected_set))
            template = self.model.get_template(model1)
            
            
            for k in range(self.population_size):
               # if(i > 0):
                
                for k in range(int(self.problem_size/10)):
                    i,j = random.randint(0,self.problem_size-1) ,random.randint(0,self.problem_size-1)
                
                    template[j],template[i]=template[i],template[j]
                
             #   offspring = self.model.sampling_m1(model1,template)
                template = np.array(template, dtype = np.int32)
              
                offspring = hello.sampling(model1,template,self.problem_size) 
               # offspring = np.append(offspring,int(self.p.evaluate_vns(offspring)))
                offspring [-1] = self.p.evaluate_vns(offspring)
                if offspring[-1] < self.best_solution[-1]:
                    self.best_solution = copy.copy(offspring)
                    print(self.best_solution[-1], '  FEs: ',self.p.FEs, ' ARPD = ',(self.best_solution[-1] - self.p.optimum)*100/self.p.optimum)
                   # print(offspring)
                  
                if offspring[-1]< temp and not any(np.equal(population,offspring).all(1)):
                    population.append(offspring)
             #   population = self.replacement(population,offspring)#.append(offspring)
            
            
        
        
        
         #   print('gen : ',i,' min ',min(population).distfit,' max ', max(population).distfit)
        print(self.best_solution)
       
        print(self.p.FEs,' Evaluation fitness')
      #  new_solution = self.vns.VNS_4(self.best_solution.individual,24*100*24+100000)
     #   print(new_solution)
      #  print(self.p.evaluate_vns(new_solution))
        return self.best_solution, self.best_solution[-1], (self.best_solution[-1] - self.p.optimum)*100/self.p.optimum

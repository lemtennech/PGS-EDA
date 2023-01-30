
import random
import numpy as np



class Model:
    def __init__(self,p_size, selection_size, sigma) :
       self.p_size= p_size
       self.selection_size = selection_size
       self.sigma = sigma
       
    def count(self,column, len):
        '''
        count the apperance of elements in a position
        args:
         column : column in the selected individuals
         len : problem size to add zeros in the empty position (the row returned must be equal to the problem size)
        return a row to insert in the model
        '''
        counter = np.bincount(column)
        while (np.size(counter) < len):
            counter = np.append(counter,0)
            
        return counter
    
    def normalize(self,probs):
        '''
        Normalize the probabilities of model1 between 0 and 1
        '''   
        
       
        prob_factor = 1 / sum(probs)
        probs = [prob_factor * i for i in probs]
        return probs    
   
    def createModel1( self,pop):
        '''
        This function return the model1 which discribe the appereance of elements in each position
        args:
            the selected individuals
        return : the model1
        
        population =[]
        for el in pop :
            population.append(el.individual)
        '''
        model1 = np.zeros((self.p_size,self.p_size))
  
        population = np.array(pop)
        for k in range (self.p_size):
            row = self.count(population[:,k],self.p_size)
            
            model1[:,k]= row + self.sigma
        #print(model1)
        return model1
    def Element1( self,model1, element):
  
    
    
    
        prob = self.normalize(model1[element])
        d = np.random.uniform(0,1)

        
        
       
        for i in range(1,len(prob)):
                prob[i]= prob[i]+prob[i-1]
            
        for i in range(len(prob)):
            if  prob[i]>d:
                position = i
                break
        
        model1 = self.model1Adjus(model1,position)
        
        return  position #offspring #, model1
    def sampling_m1(self, model1, template):
        model = np.copy(model1)
        offspring = [None]*self.p_size
    #    identity = list(range(len(model1)))
        position = list(range(len(template)))
      
     
        for k in template:
            
            
           # position = self.Element(model,k)
         #   prob = self.normalize(model[k])
            
            
            prob_factor = 1 / sum(model[k])
            prob = [prob_factor * i for i in model[k]]
            d = np.random.uniform(0,1)
          #  position = np.random.choice(identity, p = prob)
    
         
            
            for i in range(1,len(prob)):
                prob[i]= prob[i]+prob[i-1]
             
            for i in range(len(prob)):
                if  prob[i]>d:
                   # position = i
                    break
            model = np.delete(model,i,axis=1)
           # model[:,position]=0
           
            offspring[position[i]]=k
            
            del position[i]
         
            
        return offspring
    
    def Element(self, model1, element):
        '''
        Return the position of the first element in the offspring to be sampled
        '''
        
        identity = list(range(len(model1)))
      
        prob = self.normalize(model1[element])
        
        position = np.random.choice(identity,p=prob)
       # model1 = self.model1Adjus(model1,position)
        model1[:,position]=0
        return  position #offspring #, model1
   
    
    def get_template(self, model1):
        c = []
        for i in range(len(model1)):
            c.append([max(model1[i]),i])
        c.sort(reverse=True)

        sol = []
        for i in c:
            sol.append(i[1])
        return sol
        
    """ 
    def position(self, permutation, i):
        '''
        return the position of the element i in permuatation
        '''
        permutation = np.array(permutation)
        for k in range(self.p_size):
            if permutation[k]==i:
                return k
            
    def check(self,permutation, i ,j):
        '''
        check the ordre of elements
        return 1 if i appear after j and 0 otherwise
        '''
        permutation = np.array(permutation)
        for k in range(self.p_size):
            
            
            if (self.position(permutation,i)> self.position(permutation,j)):
                return 1
            else:
                return 0
            
          
    def checkRow(self, population,i,j):
        s = 0
       
        for k in range(np.size(population,0)):
           
            s = s + self.check (population[k,:],i,j)
        return s
            
   
    def createModel2(self, pop):
        
        population =[]
        for el in pop :
            population.append(el.individual)
            
        population= np.array(population)
        model2 = np.zeros((self.p_size,self.p_size))
        for i in range(self.p_size):
            for j in range(self.p_size):
                if i == j:
                    model2[i,j]==0
                else:
                    model2[i,j]= self.checkRow(population,i,j)+self.sigma
                    
        
        
        return model2
     
    def model1Adjus(self,model1,position):
        model1[:,position]=0
        return model1  
                        
    def firstElement(self, model1,element):
        '''
        Return the position of the first element in the offspring to be sampled
        '''
        offspring = [None]*self.p_size
        identity = list(range(len(model1)))
        
        prob = self.normalize(model1[element])
        
        position = np.random.choice(identity,p=prob)
       # model1 = self.model1Adjus(model1,position)
        offspring[position]=element
        return  offspring , model1
    
    def checkPositionValidation(self, offspring,position):
         if offspring[position] is None:
             return True
         else:
             return False
            
    def adjusting(self, model, col):
       
        k = 0
        for i in model:
            indice = np.where(i != 0 )
            
            if (i[col] != 0):
                k = i[col]
               
                i[col] = 0
                for j in range(np.size(i)):
                    if (i[j] != 0):
    #                    print(j)
                        i[j] = i[j]+ (k / (np.size(indice)-1))
                        
                                  
        return model
    
    def position_direction (self,model2, element_sampled, new_element):
        '''
        Determine if new_element will be after or before the sampled element
        Returns :
            0 = befor
            1 = after
        '''
        prob_after = model2[new_element,element_sampled]/(self.selection_size + (2*self.sigma)) # selected populaion size
       
        prob_before = 1 - prob_after
        probabilities = [prob_before,prob_after]
       
        directions = [0,1]
        direction = np.random.choice(directions,p = probabilities)
        return direction
    
    def check_next_segment(self, individual, position):
        '''
        To check if there is position not yet simpled in the successors of the current position
        '''
        check = False
        for i in range(position,len(individual)):
            if individual[i] is None:
                check = True
        return check
    
    def get_segment(self, model2, new_element, individual):
        '''
        args:
             model2
             new element to be sampled
             individual (in sampling process) 
        return : 
             the first and last indices of the segement in which the new_element to be sampled
        '''
        first = 0 
        last = len(individual)-1
        indicator = False # to jump the not none position after the begin of the segment
     
        for i in range (len(individual)):
            
            
            if individual[i] is not None  :
                if not indicator:
                    first = first + 1
                if indicator :
                   
                    direction = self.position_direction(model2,individual[i],new_element)
                    if direction == 1 and self.check_next_segment(individual,i):
                       
                        indicator = False
                        first =i+1
                        
                    else:
                        
                        last = i-1
                        break
                       
                        
            else:
                indicator =True
               
                
                
                  
        return first, last
            
    def sampling_segment(self, model1,start_segment,end_segment, element):
        
        if start_segment == end_segment:
            position = start_segment
        else:   
            identity = list(range(start_segment,end_segment+1))
           
            prob = model1[element,start_segment:end_segment+1]
            
            prob = self.normalize(prob)
            position = np.random.choice(identity,p=prob)
        
        
        return position
    
    def sampling(self, model1,model2,solution):
        solution = np.array(list(range(self.p_size)))
        
        first = solution[0]
       
        offspring , model1 = self.firstElement(model1,first)
        
        solution = np.delete(solution,0)
        
        for element in solution:
           
            start_segment, end_segment = self.get_segment(model2, element , offspring)
            position = self.sampling_segment(model1,start_segment,end_segment,element)
            offspring[position]=element
       
        return offspring       
    def sampling_t(self, model1,model2,solution):
       
        offspring = [None]*self.p_size
        cuts = random.sample(range(self.p_size),2)
        cuts = np.sort(cuts)
        seg = solution[cuts[0]:cuts[1]]
        offspring[cuts[0]:cuts[1]] = seg
        solution = np.delete(solution, np.where(solution == seg[0]))
        for i in seg :
            solution = np.delete(solution, np.where(solution == i))
            
       
        for element in solution:
           
            start_segment, end_segment = self.get_segment(model2, element , offspring)
            position = self.sampling_segment(model1,start_segment,end_segment,element)
            offspring[position]=element
       
        return offspring   
    
    
 
   
    """    

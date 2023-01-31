
import numpy 
cimport numpy 
cimport cython
numpy.import_array()

     
@cython.wraparound(False)
@cython.boundscheck(False)
cpdef  sampling(numpy.ndarray[numpy.float64_t, ndim=2] model1, numpy.ndarray[numpy.int32_t, ndim=1] template, int p_size):
    
    cdef numpy.ndarray[numpy.int_t, ndim=1] offspring
    offspring = numpy.empty(p_size+1, dtype=numpy.int)
    cdef numpy.ndarray[numpy.double_t, ndim=1] prob 
    prob = numpy.empty(p_size, dtype=numpy.double)
    cdef int position 
    cdef double prob_factor
    cdef double d
    cdef numpy.ndarray[numpy.float64_t, ndim=2] model
    model = numpy.copy(model1)
    cdef int i,j,k,l


    for k in range(p_size):
       
        prob_factor = 1 / sum(model[template[k]])
      #  prob = numpy.array([prob_factor * l for l in model[template[k]]])
        for l in range(p_size):
            prob[l] = model[template[k]][l]*prob_factor

        d = numpy.random.uniform(0,1)
    
        for i in range(1,p_size):
            
            prob[i]= prob[i]+prob[i-1]
        
        for j in range(p_size):
        
            if  prob[j]>d:
                position = j
                break
        

        model[:,position]=0
        
        offspring[position]=template[k]
   # print(type(offspring))
        
    return offspring
@cython.wraparound(False)
@cython.cdivision(True)
@cython.nonecheck(False)
@cython.boundscheck(False)
def sampling_m1(numpy.ndarray[numpy.float64_t, ndim=2] model1, numpy.ndarray[numpy.int32_t, ndim=1] template, int p_size):
   
    return sampling(model1, template, p_size)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.nonecheck(False)
@cython.boundscheck(False)
cdef int evaluate( numpy.ndarray[numpy.int32_t, ndim=1] genes, numpy.ndarray[numpy.int32_t, ndim=2] processingTimes):
    
    cdef int n_machines = len(processingTimes)
    cdef int n_jobs = len(processingTimes[0])
    cdef int i,k,y,j,m, fitness
    m_timeTable = numpy.array([0]*n_machines)
    for i in range(n_machines):
        first_gene=genes[0]
        m_timeTable[0]=processingTimes[0][first_gene]
        for k in range(n_machines-1):
            j = k+1
            m_timeTable[j]=m_timeTable[j-1]+processingTimes[j][first_gene]

    fitness=m_timeTable[n_machines-1]
    for y in range(n_jobs-1):
        job=genes[y + 1]
        m_timeTable[0]+=processingTimes[0][job]
        prev_machine=m_timeTable[0]

        for m in range(n_machines-1):
            machine = m+ 1
            m_timeTable[machine]= max(prev_machine,m_timeTable[machine])+ processingTimes[machine][job]
            prev_machine=m_timeTable[machine]
        
        fitness+=m_timeTable[n_machines-1]
    return fitness

@cython.wraparound(True)
@cython.cdivision(True)
@cython.nonecheck(False)
@cython.boundscheck(False)    
def evaluate_vns(numpy.ndarray[numpy.int32_t, ndim=1] genes, numpy.ndarray[numpy.int32_t, ndim=2] processingTimes):
    return evaluate(genes, processingTimes)

cdef evaluate_vns2( numpy.ndarray[numpy.int32_t, ndim=1] solution, numpy.ndarray[numpy.int32_t, ndim=2] processingTimes):
   
    
    cdef int j,m
    cdef numpy.ndarray[numpy.int_t, ndim=1]  d
    cdef int n_jobs = len(processingTimes)
    cdef int n_machines = len(processingTimes[0])
    cdef numpy.ndarray[numpy.int_t, ndim=2]   completion_times = numpy.zeros((n_jobs, n_machines), dtype = int)
    
    completion_times[0, :]=numpy.cumsum(processingTimes[solution[0],:])
    completion_times[:, 0] = numpy.cumsum(processingTimes[solution[:-1], 0])
    for j in range(1,n_jobs):
        for m in range(1,n_machines):
            completion_times[j,m] = processingTimes[solution[j], m] + max(completion_times[j,m-1],completion_times[j-1,m])

   # fits = completion_times.tolist()
    return completion_times[n_jobs-1,n_machines-1]
def evaluate_vnsms(numpy.ndarray[numpy.int32_t, ndim=1] genes, numpy.ndarray[numpy.int32_t, ndim=2] processingTimes):
    return evaluate_vns2(genes, processingTimes)


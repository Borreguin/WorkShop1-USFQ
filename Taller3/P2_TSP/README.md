# Conclusions about solving the TSP problem

1. For the case study 1, the current solution is not optimal but is good enough for practical purposes and can be found in a reasonable amount of time.

1. For the case study 1, By increasing the exponential growth in the number of posibilities the problem becomes significantly harder to solve as the number of cities increases, loading to increased resolution times. 


    ``` 
    n_cities = [10, 20, 30, 40, 50]
     solutions = {}
     for n_city in n_cities:
         tsp, ruta = study_case_1(n_cities=n_city, tolerance=0.20, time_limit=120, tee=False)
         solutions[n_city] = [tsp, ruta]
    
     for solution in solutions:
         print(f"Para {solution} ciudades, tiempo: ", end='')
         print(solutions[solution][0].execution_time)
    ```
    
    
1. Para 10 ciudades, tiempo: 0:00:00.039944
1. Para 20 ciudades, tiempo: 0:00:00.404346 
1. Para 30 ciudades, tiempo: 0:00:05.750724
1. Para 40 ciudades, tiempo: 0:00:19.522744
1. Para 50 ciudades, tiempo: 0:02:00.116622



For less than 50 cities, the times are fine, however, when the cities exceed
the algorithm is not able to find an answer in the given time. 
the algorithm fails to find an answer in the time frame.
For these algorithms, the routes that I have marked show a good approximation, however, it is not the correct solution.
However, it is not the correct solution since at first glance it can be seen that there are better routes, however
that there are better routes, however, the solutions are very good, 
with respect to the computation time.



```
     n_cities = [10]
     solutions = {}
     for n_city in n_cities:
         tsp, ruta = study_case_1(n_cities=n_city, tolerance=0.20, time_limit=120, tee=True)
         solutions[n_city] = [tsp, ruta]
    
     for solution in solutions:
         print(f"Para {solution} ciudades, tiempo: ", end='')
         print(solutions[solution][0].execution_time)
```


1. Tee param help us to display the solver's progress. It's usefull to understand details of the optimization problem. It provides real time feedback about the solver operations, including the current solution or if no solutions is founded. 

    Last output: 

    ```
    93926: mip =   1.558250325e+03 >=   1.121793878e+03  28.0% (6277; 911) Time used: 120.0 secs.  Memory used: 23.2 Mb.
    95225: mip =   1.558250325e+03 >=   1.121793878e+03  28.0% (6365; 913) TIME LIMIT EXCEEDED; SEARCH TERMINATED 
    ```

    The solver was not able to find an optimal solution within the specified time limit. However, it did find a solution that is within 28% of the lower bound, which might be good enough for practical purposes. Also, the use of a time limit is important to prevent the solver from running indefinitely on difficult problems. However, the choice of time limit can impact the quality of the solution found.


    ```
    For 50 cities, Time: 0:02:00.127389
    ```

    This parameter is used to print the progress of the algorithm on the console while it is running.
    on console while it is running, it shows the number of iteration in which it is going,
    the target value to be reached, the current value and the gap with the target value.
    the current value and the gap with the target value.
    If we perform the same analysis with 10 cities, the gap is a minimum of approximately
    15.6%, which is considered achieved because it is less than the applied tolerance and ends the execution of the same.
    and ends the execution of the same.    


```
    solutions = {}
    
     heuristics = ['limitar_funcion_objetivo']
     tsp, ruta = study_case_2(120, 0.20, 120, True, heuristics)
     solutions['con_heuristica'] = [tsp, ruta]
    
     heuristics = []
     tsp, ruta = study_case_2(120, 0.20, 120, True, heuristics)
     solutions['sin_heuristica'] = [tsp, ruta]
    
     for solution in solutions:
         print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
               f"tiempo: {solutions[solution][0].execution_time}")
```


1. Heuristic
    
    For with_heuristic, distance: 1558.250325102994, time: 0:00:40.164015
    
    For sin_heuristica, distance: 1489.6196678078243, time: 0:00:40.220753
    
    Answer: In the runtime we notice that there is no difference between the two algorithms, however, we 
    the two algorithms, however, the distance is different, and the distance without heuristics is better.
    without heuristic, so we can say that the heuristic is not good for this case.
    Maybe if we increase the maximum execution time we could see better results.
    
    For with_heuristic, distance: 1558.250325102994, time: 0:02:00.187157
    For sin_heuristica, distance: 1489.6196678078243, time: 0:02:00.217129
    
    We tried setting a limit of 120 seconds, and we got the same result. The
    which gives us to understand that the heuristic is not good for this problem.
    
    We tried the heuristic with a few cities, and the algorithm does not find an answer or solution, so the 
    the algorithm does not find an answer or a solution, so this heuristic does not work for few cities.
    
    However, when we test with more cities the results with the heuristica
    are better, since it finds a better distance than the algorithm without heuristic.
    The attached results are for 120 cities.
    
    For with_heuristic, distance: 2064.324514299455, time: 0:01:48.063817
    
    For sin_heuristica, distance: 2166.1683409945917, time: 0:02:00.975900
    
    ```
     solutions = {}
    
     heuristics = ['vecino_cercano']
     tsp, ruta = study_case_3(20, 0.10, 60, True, heuristics)
     solutions['con_heuristica'] = [tsp, ruta]
    
     heuristics = []
     tsp, ruta = study_case_3(20, 0.10, 60, True, heuristics)
     solutions['sin_heuristica'] = [tsp, ruta]
    
     for solution in solutions:
         print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
               f"tiempo: {solutions[solution][0].execution_time}")
    ```

    For with_heuristic, distance: 1860.5849359671888, time: 0:01:00.385505
    
    For sin_heuristica, distance: 1896.2938227104403, time: 0:01:00.616954
    
    Answer: In this case, the heuristic did give us a better result, the execution time is the same for all the heuristics.
    time is the same for both, however, the distance is better for the algorithm that uses the heuristic.
    the algorithm that uses the nearest neighbor heuristic.
    However, this heuristic is not good for the problem when the number of cities is smaller.
    the same algorithm with 20 cities, and the results are better for the heuristic without heuristic.
    are better for the algorithm without heuristics.
    
    For with_heuristic, distance: 731.2632929644172, time: 0:00:00.369940
    
    For without_heuristic, distance: 698.001975055342, time: 0:00:00.491536
    
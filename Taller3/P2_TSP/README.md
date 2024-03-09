## Conclusions

1. For the case study 1, the current solution is not optimal but is good enough for practical purposes and can be found in a reasonable amount of time.

1. For the case study 1, By increasing the exponential growth in the number of posibilities the problem becomes significantly harder to solve as the number of cities increases, loading to increased resolution times. 


1. Tee param help us to display the solver's progress. It's usefull to understand details of the optimization problem. It provides real time feedback about the solver operations, including the current solution or if no solutions is founded. 

    Last output: 

    ```
    93926: mip =   1.558250325e+03 >=   1.121793878e+03  28.0% (6277; 911) Time used: 120.0 secs.  Memory used: 23.2 Mb.
    95225: mip =   1.558250325e+03 >=   1.121793878e+03  28.0% (6365; 913) TIME LIMIT EXCEEDED; SEARCH TERMINATED 
    ```

    The solver was not able to find an optimal solution within the specified time limit. However, it did find a solution that is within 28% of the lower bound, which might be good enough for practical purposes. Also, the use of a time limit is important to prevent the solver from running indefinitely on difficult problems. However, the choice of time limit can impact the quality of the solution found.
## Graphs by hour

### CO2

Vent 1
![co2](/Taller3/P1_UML/imagenes/lb_V005_vent01_CO2.png) 
Vent 2
![co2](/Taller3/P1_UML/imagenes/lb_V022_vent02_CO2.png) 

### TEMPERATURE
Vent 1
![co2](/Taller3/P1_UML/imagenes/lb_V006_vent01_temp_out.png) 
Vent 2
![co2](/Taller3/P1_UML/imagenes/lb_V023_vent02_temp_out.png) 


# Task 1: one variable

For this task we make an analysis of each variable using divided by days each day is processed with 5 clusters. This will helps us to identify patterns in each graph adding an additional ``Isolation forest`` to detect anomalies in the fit predictions used. with the help of ``kmeans`` and `zcmeans`

The graps are divided into 2 days we can analize more but we took only the first 2 days for this document. 

## VENT 5 DATA
Day 1 
![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1.png) 

Day 2 
![kmeans_day2_vent5](/Taller3/P1_UML/imagenes/kmeans_day2.png) 

![zcmeans_day2_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1.png) 

## VENT 22 DATA
Day 1 
![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1_v022.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1_v022.png) 

Day 2 
![kmeans_day2_vent5](/Taller3/P1_UML/imagenes/kmeans_day2_v022.png) 

![zcmeans_day2_vent5](/Taller3/P1_UML/imagenes/zcmeans_day2_v022.png) 


## VENT 23 DATA
Day 1 
![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1_temp_vent23_2.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1_temp_vent23_2.png) 

Day 2 
![kmeans_day2_vent5](/Taller3/P1_UML/imagenes/kmeans_day2_temp_vent23_2.png) 

![zcmeans_day2_vent5](/Taller3/P1_UML/imagenes/zcmeans_day2_temp_vent23_2.png) 


## VENT 6 DATA
Day 1 
![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1_temp_vent6_1.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1_temp_vent6_1.png) 

Day 2 
![kmeans_day2_vent5](/Taller3/P1_UML/imagenes/kmeans_day2_temp_vent6_1.png) 

![zcmeans_day2_vent5](/Taller3/P1_UML/imagenes/zcmeans_day2_temp_vent6_1.png) 


As we can see each graph is easy to interpretate knoing that we can 5 sections and a representation of posible anomalies in each graph represented by the color ``orange``, with this we can discriminate clusters sections that my have anomalies and decide with is more important for our case of study by day.


# Task 2: two variable

## VENT 5 - 22 - co2 DATA

Day 1

![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1_multivariable.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1_multivariable.png) 

Day 2 

![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day2_multivariable.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day2_multivariable.png) 


## VENT 23 - 6 - temperature DATA

Day 1 

![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day1_multivariable_temperature.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day1_multivariable_temperature.png) 

Day 2

![kmeans_day1_vent5](/Taller3/P1_UML/imagenes/kmeans_day2_multivariable_temperature.png) 

![zcmeans_day1_vent5](/Taller3/P1_UML/imagenes/zcmeans_day2_multivariable_temperature.png) 

As we can see for temperature data, the approach of 5 cluster for the fit and predict using ``kmeans`` ``zcmeans`` is not enough, because the see a lot of anomalies each day. We can consider to add more clusters to analaize more patterns by day and get a better fit for out data.


## Conclusions
1. Boxplot shows how the 8 labor hours explains the significant increase of CO2 ppm at the both sides of the building.The building temperature raises and keep the thermal energy, as well as the sun reaches its peak brilliance at noon, its the point of the average high temperature.

1. The experiment hour per hour for single-variable shows that the hour correlation just indicates CO2 increase during the day and the deacrese as long as the people leave the building, some atypical values are shown but unsignificant for the analyses. Temperatures values vs hours shows the raising temperatures at 25° degrees for each.

1. The KMeans and Fuzzy C-means clustering algorithms provide different perspectives on the data. KMeans provides a hard clustering where each data point is assigned to one cluster, resulting in a wider spread of clusters. On the other hand, Fuzzy C-means allows for soft clustering where data points can belong to multiple clusters with varying degrees of membership, often resulting in tighter clusters. This difference is clearly visible in the scatter plots.

1. The scatter plots provide a useful way to visualize the results of the clustering algorithms. Each point in the scatter plot represents a single data point (a row in the DataFrame), with its position determined by its index and its variable value. The centroids of each cluster are also plotted, providing a visual representation of the "center" of each cluster. This visualization can help in understanding the distribution of data within each cluster and the differences between clusters.

1. Using Isolation forest give us the posibilitiy of visualize and detect anomalies in cases where there is a high dimensionality in the data. 

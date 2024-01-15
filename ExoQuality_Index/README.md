## ExoQuality Index External Operation: 

In our publication, we developed a statistical metric called the ExoQuality Index (EQI) that measures extracellular vesicle homogeneity when given a dataframe containing experimental characterization. To use the EQI calculation externally, please do the following:
```
1. Download this folder
```
```
2. Put your data into this folder as a CSV file
  a. Your data structure should be samples (rows) by parameters (columns)
     with an additional isolation identifier column
  b. a toy example has been provided in this folder as an example
```
```
3. Run the python script using python EQI.py
  a. We will check library dependencies for the following:
      1. matplotlib.pyplot
      2. seaborn
      3. numpy
      4. pandas
      5. scipy
      6. sklearn

  b. If the dependencies are less than the required version, we will stop the EQI calculation
     until resolved. We will leave it up to the user to resolve the issue
     (i.e conda or install w/ pip). 
```
## Please submit a ticket with any issues 

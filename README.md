# DataScribe

Natural Language Generation from 2D Data
- Get insights on the trends and anomalies in data as a part of a narration.


## Dependencies
- Python 3.1 or above
- matplotlib
- numpy

## Instructions:
Refer to 'sample_narration.py' for full implementation of module.

### Accessing the library:
Import the library from a python script running on the same directory
```from datascribe import *```

### Importing data from .CSV
Create a processed data object from the Process_CSV module
```data = Process_CSV('filename.csv')```

### Setting Attributes:

- Set the labels_row attribute to *True* if the first row in the CSV contains the column labels and *False* otherwise.

          ```data.labels_row = False/True```

- If there is a column with only the labels to each data object, specify it using *.variable_col*
  - Example: If the first column contains labels, Set ```data.variable_col = 0```


- Set X and Y axes using the *.set_axis* with parameters:

  1. ```"x"``` or ```"y"``` (to define the axis being set)
  2. *columnID* (The column index which the axis refers to)
  3. *DataType* (Integer/Float/Datetime)
  4. Additional formatting if the data is of type Datetime.
  - Example:
    - If X axis is column:1 of type *datetime*:      ```data.set_axis("x",1,'datetime','%b %d %Y')```
    - If Y axis is column:2 of type *float*:         ```data.set_axis("y",2,'float', None)```
        

### Analysing Data:

After setting the necessary attributes, execute the following for analysing the data:
```Narration_Data = data.transform()```

#### Accessing the Narrations:
- The output of *.transform()* is a list with each element referring to each label if there are more than one labels
- To access the narrations in a graphical interface, execute:       ```GUI(Narration_Data[0])``` for viewing the narration of the first label; 
  - Change the index for viewing subsequent narrations of other labels




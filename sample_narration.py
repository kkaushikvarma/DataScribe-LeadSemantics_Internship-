


from datascribe import *

data = Process_CSV('datasets/stocks.csv')
data.labels_row = False
data.set_axis("x",1,'datetime','%b %d %Y')
data.set_axis("y",2,'float', None)
data.variable_col = 0
data = data.transform()
i = data[0]
GUI(i)

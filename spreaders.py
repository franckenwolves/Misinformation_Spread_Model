import pandas as pd
import csv


df = pd.read_csv('infected_by.csv', delimiter=',')

with open('infection_spreaders.csv', 'w') as s:
    
    values = df.iloc[:, 2].value_counts()
    print(values)
    s.write('node, number of other nodes infected by node\n')
    s.write(str(values))

    values = df.iloc[:, 6].value_counts()
    print(values)
    s.write('node, number of other nodes infected by node\n')
    s.write(str(values))

    values = df.iloc[:, 10].value_counts()
    print(values)
    s.write('node, number of other nodes infected by node\n')
    s.write(str(values))

    values = df.iloc[:, 14].value_counts()
    print(values)
    s.write('node, number of other nodes infected by node\n')
    s.write(str(values))
    
    values = df.iloc[:, 18].value_counts()
    print(values)
    s.write('node, number of other nodes infected by node\n')
    s.write(str(values))



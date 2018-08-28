
import pyodbc
import pandas as pd
import numpy as np


def micro_access_open(path,data_section):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+path)
    cursor = conn.cursor()
    cursor.execute('select * from '+data_section)
    temp = cursor.fetchall()
    conn.close()
    table = pd.DataFrame(temp)
    df =pd.DataFrame(columns=table.index)
    for i, row in enumerate(table[0]):
        try:
            df[i] = list(row)
        except:
            print(row)
            break
    dfF = df.T
    return dfF



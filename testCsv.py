import os
import tkinter as tk
import tkinter.messagebox,tkinter.filedialog
import pandas as pd
import openpyxl as xl
import pandas_profiling as pdp

'''
root = tk.Tk()
root.withdraw()
fTyp = [('CSV File','*.csv')]
init_Dir = os.path.abspath(os.path.dirname(__file__))
file = tk.filedialog.askopenfilename(filetypes = fTyp,initialdir = init_Dir)
'''
file = '140-0385-01_TA-01-140.csv'
df = pd.read_csv(file,header=None)

df.columns = ['time','max_diam','min_diam','C','D','E','F','G','dist']
df = df.assign(sec_dist=0.0,dist_no=0)

is_first_dist = True
before_dist = 0.0
sec_dist = 0.0
now_dist_no = 0
sec_dist_value = 1000
for index, row in df.iterrows():
    if is_first_dist:
        before_dist = row.dist
        is_first_dist = False
    else:
        if now_dist_no != 0 & sec_dist_value != 3100:
            sec_dist_value = 3100

        sec_dist += row.dist - before_dist
        if sec_dist < sec_dist_value:
            row.sec_dist = sec_dist
            before_dist = row.dist
        else:
            now_dist_no += 1
            row.dist_no = now_dist_no
            sec_dist = row.dist - before_dist
            row.sec_dist = sec_dist
    df.iat[index,9] = sec_dist
    df.iat[index,10] = now_dist_no

file = file.replace('.csv','.xlsx')
book = pd.ExcelWriter(file)
df.to_excel(book,'test')
book.save()


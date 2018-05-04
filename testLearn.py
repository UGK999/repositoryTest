import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

from sklearn.datasets import load_boston
boston = load_boston()
'''
plt.scatter(boston.data[:,5], boston.target)
plt.xlabel('Price ($1,000)')
plt.ylabel('Number of rooms')
'''
boston_df = DataFrame(boston.data)
boston_df.columns = boston.feature_names
boston_df['Price'] = boston.target

sns.lmplot('RM', 'Price', data = boston_df)

X = boston_df.RM
X = np.vstack(boston_df.RM)
Y = boston_df.Price
X = np.array([[value, 1]for value in X])
a, b = np.linalg.lstsq(X,Y)[0]
plt.plot(boston_df.RM, boston_df.Price, 'o')
x = boston_df.RM
plt.plot(x, a*x+b,'r')
plt.show()


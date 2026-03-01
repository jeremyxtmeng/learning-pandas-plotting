import matplotlib.pyplot as plt

# Sample data
data = [1, 2, 2, 3, 4, 5, 5, 5, 6]

plt.hist(data, bins=6)
plt.title('Histogram Example')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()



import numpy as np

x = np.arange(0, 5, 0.1)
y = np.sin(x)
plt.plot(x, y)
plt.show()


import pandas as pd
import numpy as np

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [6, 7, 8, 9, 10]
}, index=['row1', 'row2', 'row3', 'row4', 'row5'])

import pandas as pd
import numpy as np

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [6, 7, 8, 9, 10]
}, index=['row1', 'row2', 'row3', 'row4', 'row5'])

a=df[['A','B']]
print(a.mean())
print(a.loc['row1'])

print(df[(df['A']>3) | (df['A']<5)])
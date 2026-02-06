import pandas as pd
from matplotlib import pyplot as plt

# external files can be imported before or after
from lib import elaborate

# importing the library is enough to generate all files 
import yprov4dv

df = pd.read_csv('./assets/knn.csv')
# Not necessary, it will be tracked anyways
yprov4dv.log_input('./assets/knn.csv')

df["x"] = elaborate(df["x"])

df.plot(
   x='x', 
   y='y', 
   kind='scatter'
)

plt.savefig("swx_example.png")

# Not necessary, it will be tracked anyways
yprov4dv.log_output('./assets/knn.csv')

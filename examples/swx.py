import pandas as pd
from matplotlib import pyplot as plt
import sys
sys.path.append("./examples")
sys.path.append(".")
import yprov4dv

df = pd.read_csv('./assets/knn.csv')
# yprov4dv.log_input('./assets/knn.csv')

df.plot(
   x='x', 
   y='y', 
   kind='scatter'
)

plt.savefig("swx_example.png")
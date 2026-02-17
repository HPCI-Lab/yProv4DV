import pandas as pd
from matplotlib import pyplot as plt

# external files can be imported before or after
from lib import elaborate

# importing the library is enough to generate all files 
import sys
sys.path.append(".")
import yprov4dv
yprov4dv.start_run(verbose=False, create_json_file=True, create_dot_file=True, create_svg_file=True)

# yprov4dv.untrack_file('./assets/large.csv')
df = pd.read_csv('./assets/results.csv')

df["x"] = elaborate(df["points"])

df.plot(
   x='x', 
   y='points', 
   kind='scatter'
)

plt.savefig("swx_example.png")

# Not necessary, it will be tracked anyways
yprov4dv.log_output('swx_example.png')

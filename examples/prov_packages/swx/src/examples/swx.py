from lib import elaborate

import sys
sys.path.append(".")
import yprov4dv

yprov4dv.start_run()
import pandas as pd
import matplotlib.pyplot as plt

# This is just to provide a reproducible script
import urllib.request
urllib.request.urlretrieve(
   "https://raw.githubusercontent.com/HPCI-Lab/yProv4DV/main/assets/results.csv",
   "results.csv"
)

data = pd.read_csv("results.csv")

# In this case this is not necessary,
# the file will be copied automatically
# yprov4dv.log_input("results.csv")

data["second_series"] = elaborate(data["points"])
data.plot()

plt.savefig("example.png")

# In this case this is not necessary, 
# the file will be copied automatically
# yprov4dv.log_output("example.png")
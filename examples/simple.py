import sys
sys.path.append("./examples")
sys.path.append(".")

import yprov4dv
import pandas as pd
import matplotlib.pyplot as plt

from lib import elaborate

yprov4dv.log_input("./assets/results.csv")

data = pd.read_csv("./assets/results.csv")

data["second_series"] = elaborate(data["points"].tolist())

data.plot()
plt.legend()
plt.savefig("tmp.png")

# yprov4dv.log_output("tmp.png")
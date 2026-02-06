import yprov4dv
import pandas as pd
import matplotlib.pyplot as plt

from lib import elaborate

data = pd.read_csv("./assets/results.csv")
yprov4dv.log_input("./assets/results.csv")

data["second_series"] = elaborate(data["points"])

data.plot()
plt.legend()
plt.savefig("tmp.png")

yprov4dv.log_output("tmp.png")
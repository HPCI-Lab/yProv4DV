import sys
sys.path.append("./examples")
sys.path.append(".")

import os
os.environ["YPROV4DS_PROVENANCE_DIRECTORY"] = "newdir"
os.environ["YPROV4DS_CREATE_JSON_FILE"] = "True"
os.environ["YPROV4DS_CREATE_DOT_FILE"] = "False"
os.environ["YPROV4DS_CREATE_SVG_FILE"] = "True"
os.environ["YPROV4DS_VERBOSE"] = "True"

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

yprov4dv.log_output("tmp.png")
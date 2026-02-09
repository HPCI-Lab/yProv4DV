import yprov4dv
yprov4dv.start_run(create_rocrate=False, create_json_file=True, create_dot_file=True, create_svg_file=True, skip_files_larger_than=23//(1024**2))
import pandas as pd
import matplotlib.pyplot as plt

from lib import elaborate

yprov4dv.log_input("./assets/results.csv")
data = pd.read_csv("./assets/results.csv")

data["second_series"] = elaborate(data["points"])

data.plot() # also supports data.plot.bar() etc...
plt.legend()
plt.savefig("tmp.png")
yprov4dv.log_output("tmp.png")
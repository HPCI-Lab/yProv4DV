import sys
sys.path.append(".")
import yprov4dv
yprov4dv.start_run(create_rocrate=False, create_json_file=True, create_dot_file=True, create_svg_file=True, skip_files_larger_than=23//(1024**2))
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lib import elaborate

data = pd.read_csv("./assets/results.csv")
# yprov4dv.log_input("./assets/results.csv")

data["second_series"] = elaborate(data["points"])

# plt.plot(data["points"], data["second_series"])
# plt.legend()
# plt.savefig("tmp1.png")

sns.lineplot(data,x="points", y="second_series")
plt.legend()
plt.savefig("tmp2.png")

# yprov4dv.log_output("tmp.png")
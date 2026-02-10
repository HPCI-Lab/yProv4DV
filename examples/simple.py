import yprov4dv
yprov4dv.start_run(create_json_file=True, create_dot_file=True, create_svg_file=True)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# This script will also be copied in the ro-crate
from lib import elaborate

data = pd.read_csv("./assets/results.csv")
# Not necessary in this case
yprov4dv.log_input("./assets/results.csv")

data["second_series"] = elaborate(data["points"])

sns.lineplot(data,x="points", y="second_series")
plt.legend()
plt.savefig("example.png")

# Not necessary in this case
yprov4dv.log_output("example.png")
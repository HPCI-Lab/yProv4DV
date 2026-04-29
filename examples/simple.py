import sys
sys.path.append(".")
import yprov4dv
yprov4dv.start_run(create_json_file=True, create_dot_file=True, create_svg_file=True)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# This script will also be copied in the ro-crate
from lib import elaborate

data = pd.read_csv("./assets/results.csv")[:31]
# Not necessary in this case
# yprov4dv.log_input("./assets/results.csv")

data["Revenue2"] = elaborate(data["Revenue"])

sns.lineplot(data,x="Revenue", y="Revenue2")
plt.savefig("example.png")

# Not necessary in this case
# yprov4dv.log_output("example.png")

# Not necessary in this case
# yprov4dv.end_run()
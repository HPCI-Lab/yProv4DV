
### Customized Example

<div style="display: flex; align-items: center; margin: 20px 0;">
    <hr style="flex-grow: 0.05; border: 2px solid #009B77; margin: 0;">
    <span style="background: white; padding: 0 10px; font-weight: bold; color: #009B77;">Example:</span>
    <hr style="flex-grow: 1; border: 2px solid #009B77; margin: 0;">
</div>


```python
# Call these before importing the yprov4dv library
import os
os.environ["YPROV4DV_PROVENANCE_DIRECTORY"] = "newdir"
os.environ["YPROV4DV_CREATE_JSON_FILE"] = "True"
os.environ["YPROV4DV_CREATE_DOT_FILE"] = "False"
os.environ["YPROV4DV_CREATE_SVG_FILE"] = "True"
os.environ["YPROV4DV_VERBOSE"] = "True"

import yprov4dv
import pandas as pd
import matplotlib.pyplot as plt

from lib import elaborate

yprov4dv.log_input("./assets/results.csv")
data = pd.read_csv("./assets/results.csv")

data["second_series"] = elaborate(data["points"])

data.plot()
plt.legend()
plt.savefig("tmp.png")
yprov4dv.log_output("tmp.png")
```


<hr style="border: 2px solid #009B77; margin: 20px 0;">



<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".readme.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

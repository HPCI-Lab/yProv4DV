
### Simple Example


<div style="display: flex; align-items: center; margin: 20px 0;">
    <hr style="flex-grow: 0.05; border: 2px solid #009B77; margin: 0;">
    <span style="background: white; padding: 0 10px; font-weight: bold; color: #009B77;">Example:</span>
    <hr style="flex-grow: 1; border: 2px solid #009B77; margin: 0;">
</div>


```python
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
```


<hr style="border: 2px solid #009B77; margin: 20px 0;">


![ExampleSimple](./assets/simple.png)

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".examples.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="example_custom.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

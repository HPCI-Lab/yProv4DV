
### Customized Example

<div style="display: flex; align-items: center; margin: 20px 0;">
    <hr style="flex-grow: 0.05; border: 2px solid #009B77; margin: 0;">
    <span style="background: white; padding: 0 10px; font-weight: bold; color: #009B77;">Example:</span>
    <hr style="flex-grow: 1; border: 2px solid #009B77; margin: 0;">
</div>


```python
import yprov4dv
yprov4dv.start_run(
    create_rocrate=False, 
    create_json_file=True, 
    create_dot_file=True, 
    create_svg_file=True, 
    save_input_files_subset=True, # Take only the data plotted
    skip_files_larger_than=1 # Larger than 1 Mb
)

import pandas as pd
import matplotlib.pyplot as plt

data_path = "assets/large.csv"
# This log is not necessary, the file will be tracked anyways
yprov4dv.log_input(data_path) 
data = pd.read_csv(data_path)

data['time'] = pd.to_datetime(data['time'])
data = data.set_index('time')

recent_data = data.tail(365).copy()
recent_data["Price_Smoothing"] = recent_data["PriceUSD"].rolling(window=30).mean()

# This will capture ONLY the last 365 days of data into your PROV log
# (both "PriceUSD", "Price_Smoothing")
ax = recent_data[["PriceUSD", "Price_Smoothing"]].plot(
    figsize=(10, 6), 
    title="Bitcoin Price Trend (Last Year)",
    color=['#1f77b4', '#ff7f0e'],
    linewidth=2
)

plt.ylabel("Price (USD)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(["Daily Price", "30-Day Average"])

# 5. Save and Log Output
output_path = "btc_analysis.png"
plt.savefig(output_path, dpi=300)
# Not necessary, the file will be tracked anyways
yprov4dv.log_output(output_path)
```


<hr style="border: 2px solid #009B77; margin: 20px 0;">



<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".readme.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

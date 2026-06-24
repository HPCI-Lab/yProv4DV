import sys
sys.path.append(".")

import yprov4dv
# Initialize tracking
yprov4dv.start_run(
    create_rocrate=False, 
    create_json_file=True, 
    create_dot_file=True, 
    create_svg_file=True, 
    save_input_files_subset=False, # Take only the data plotted
    skip_files_larger_than=0.1, # Larger than 100 Kb
    verbose=True, 
)

import pandas as pd
import matplotlib.pyplot as plt

data_path = "assets/results.csv"
yprov4dv.log_input(data_path) 
data = pd.read_csv(data_path)

# 2. Pre-processing (Make it look nice)
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')

# We only want the last 365 days for a "nicer" plot
recent_data = data.tail(365).copy()

# 3. Use your elaborate function (Simulating a transformation)
# Let's say we calculate a 30-day moving average
recent_data["Revenue_Smoothing"] = recent_data["Revenue"].rolling(window=30).mean()

# 4. Plotting (This triggers your Monkeypatch)
# This will capture ONLY the last 365 days of data into your PROV log
ax = recent_data[["Revenue", "Revenue_Smoothing"]].plot(
    figsize=(10, 6), 
    title="Revenue Trend (Last Year)",
    color=['#1f77b4', '#ff7f0e'],
    linewidth=2
)

plt.ylabel("Revenue (USD)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(["Daily Revenue", "30-Day Average"])

# 5. Save and Log Output
output_path = "result_analysis.png"
plt.savefig(output_path, dpi=300)
yprov4dv.log_output(output_path)

yprov4dv.end_run()
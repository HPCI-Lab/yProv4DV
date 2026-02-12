import pandas as pd
from matplotlib import pyplot as plt
import json

# external files can be imported before or after
from lib import elaborate

# importing the library is enough to generate all files 
import sys
sys.path.append(".")
import yprov4dv
yprov4dv.start_run()

def load_jsonl(filepath):
    """Load JSONL file and return DataFrame."""
    rows = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    if not rows:
        raise ValueError(f"No valid records found in {filepath}")
    
    return pd.DataFrame(rows)

df = pd.read_csv('./assets/large.csv')

# load_jsonl("pipeline_metrics.json")

# Not necessary, it will be tracked anyways
# yprov4dv.log_input('./assets/large.csv')

df["x"] = elaborate(df["AssetCompletionTime"])

df.plot(
   x='x', 
   y='AssetCompletionTime', 
   kind='scatter'
)

plt.savefig("swx_example.png")

# Not necessary, it will be tracked anyways
# yprov4dv.log_output('swx_example.png')

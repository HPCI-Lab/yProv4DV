import time
import os

TRIALS = 30

if __name__ == "__main__": 

    msm = []

    for _ in range(TRIALS): 
        start_time = time.time()

        os.system("python examples/utils.py")

        duration = time.time() - start_time
        msm.append(duration)
        # Small files: 
        # mean                  std dev.
        # 0.9188255977630615    0.02867362595134918
        # 2.625790309906006     0.020295469903413146

        # Large files: 
        # mean                  std dev.
        # 3.3047576427459715    0.03241254163068284
        # 3.119350226720174     0.019840807024840968
    import pandas as pd
    msm = pd.Series(msm)
    print(msm.mean(), msm.std())

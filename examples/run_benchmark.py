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

    import pandas as pd
    msm = pd.Series(msm)
    msm.to_csv("without.csv", sep=";")
    print(msm.mean(), msm.std())

    msm = []
    for _ in range(TRIALS): 
        start_time = time.time()

        os.system("python examples/utils.py -w")

        duration = time.time() - start_time
        msm.append(duration)

    import pandas as pd
    msm = pd.Series(msm)
    msm.to_csv("with.csv", sep=";")
    print(msm.mean(), msm.std())

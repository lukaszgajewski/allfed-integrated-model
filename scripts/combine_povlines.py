from os import listdir
from os.path import isfile, join

import pandas as pd

data_path = "data/poverty/"
data_files = [
    join(data_path, f)
    for f in listdir(data_path)
    if isfile(join(data_path, f)) and "combined" not in f
]
df = pd.concat([pd.read_csv(f, index_col=0) for f in data_files]).reset_index(drop=True)
df.to_csv("data/poverty/worldbank_pip_combined.csv")

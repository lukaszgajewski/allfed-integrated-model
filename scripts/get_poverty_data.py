from io import StringIO

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

year = "all"
country = "all"
povlines_list = np.arange(0.05, 10.05, 0.05)
for povline in tqdm(povlines_list, total=len(povlines_list)):
    url = f"https://api.worldbank.org/pip/v1/pip?country={country}&year={year}&povline={povline}&fill_gaps=false&welfare_type=all&reporting_level=all&additional_ind=false&ppp_version=2017&format=csv"
    ret = requests.get(url)
    if ret.status_code == 200:
        pd.read_csv(StringIO(ret.text), sep=",").to_csv(f"worldbank_pip_{povline}.csv")
    else:
        print(povline, ret.status_code)

# coding: utf-8

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

with open("./DB/TransparencyGains.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["Gauss2"])
dat["Gauss2"].keys()

sns.pointplot(x='Date', y='c1Mu',hue='Channel',data=pdf)
plt.show()

sns.barplot(x='Channel', y='c1Mu', estimator=np.mean,data=pdf)
plt.show()


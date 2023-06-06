import pandas as pd
import numpy as np

from AmericanOption import AmericanOption


# American Option Test cases
S = [50, 60]
sigma = 0.4
r = 0.1
T = 2
K = [40, 50, 70, 80]
N = 200
type = ["call", "put"]

columns = ["S", "sigma", "r", "T", "K", "N", "type", "price"]
data = []

for s in S:
    for k in K:
        for tp in type:
            option = AmericanOption(S=s, sigma=sigma, r=r, T=T, K=k, N=N, type=tp)
            optionPrice = option.get_price_binomial_tree()
            data.append([s, sigma, r, T, k, N, tp, optionPrice])

df = pd.DataFrame(np.array(data), columns=columns)
df.to_csv("tests/AmericanOption.csv", index=False)


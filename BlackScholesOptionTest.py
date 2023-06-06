import pandas as pd
import numpy as np

from BlackScholesOption import BlackScholesOption


# Black Scholes Option Test cases
S = [50, 60]
sigma = 0.4
r = 0.1
T = 2
K = [40, 50, 70, 80]
q = 0.05
type = ["call", "put"]

columns = ["S", "sigma", "r", "T", "K", "q", "type", "price"]
data = []

for s in S:
    for k in K:
        for tp in type:
            option = BlackScholesOption(S=s, K=k, T=T, sigma=sigma, r=r, q=q, cp_flag=tp)
            optionPrice = option.get_price_european()
            data.append([s, sigma, r, T, k, q, tp, optionPrice])

df = pd.DataFrame(np.array(data), columns=columns)
df.to_csv("tests/BlackScholesOption.csv", index=False)


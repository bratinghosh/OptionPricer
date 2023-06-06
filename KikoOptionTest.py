import pandas as pd
import numpy as np

from KikoOption import KikoOption


# Kiko Put Option Test cases
r = 0.05
sigma = [0.3, 0.4]
T = 3
S = 100
K = 100
L = 80
U = 125
N = [50, 100]
R = 1.5
M = 1e2

columns = ["r", "sigma", "T", "S", "K", "Lower Bound", "Upper Bound", "Number of Observations", "Rebate", "M", "price", "Lower Confidence Level", "Upper Confidence Level"]
data = []

for s in sigma:
    for n in N:
        option = KikoOption(S=S, sigma=s, r=r, T=T, K=K, L=L, U=U, n=n, R=R, type="put", M=M)
        optionPrice, (conf_L, conf_U) = option.get_price_quasi_monte_carlo()
        data.append([r, s, T, S, K, L, U, n, R, M, optionPrice, conf_L, conf_U])

df = pd.DataFrame(np.array(data), columns=columns)
df.to_csv("tests/KIKOPutOption.csv", index=False)
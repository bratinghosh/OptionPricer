import math
import numpy as np
import pandas as pd

from scipy.stats import norm, qmc


class KikoOption:
    def __init__(self, S=None, sigma=None, r=None, T=None, K=None, L=None, U=None, n=None, R=None, type="put", M=1e2) -> None:
        self.seed = 8000
        
        assert S != None
        self.S = S

        assert sigma != None
        self.sigma = sigma

        assert r != None
        self.r = r

        assert T != None
        self.T = T

        assert K != None
        self.K = K

        assert L != None
        self.L = L

        assert U != None
        self.U = U

        assert n != None
        self.n = n

        assert R != None
        self.R = R

        # assert type != None and (type == "call" or type == "put")
        assert type != None and (type == "put")
        self.type = type

        assert M != None
        self.M = int(M)


    def generate_simulated_stock_prices(self):
        np.random.seed(self.seed)

        dT = self.T/self.n

        sequencer = qmc.Sobol(d=self.n, seed=self.seed) # quasi random number generator
        X = np.array(sequencer.random(n=self.M))
        Z = norm.ppf(X)

        samples = (self.r-0.5*self.sigma*self.sigma)*dT + self.sigma*math.sqrt(dT)*Z
        df_samples = pd.DataFrame(samples)
        df_samples_cumsum = df_samples.cumsum(axis=1)
        df_stocks = self.S*np.exp(df_samples_cumsum) # simulated stock prices (Size: M*N)

        return df_stocks

    def get_price_quasi_monte_carlo(self):
        values = []
        dT = self.T/self.n
        df_stocks = self.generate_simulated_stock_prices() # simulated stock prices (Size: M*N)

        for ipath in df_stocks.index.to_list():
            ds_path_local = df_stocks.loc[ipath, :]
            price_max = ds_path_local.max()
            price_min = ds_path_local.min()
            if price_max >= self.U: # knock-out case
                knockout_time = ds_path_local[ds_path_local >= self.U].index.to_list()[0]
                payoff = self.R*np.exp(-knockout_time*self.r*dT)
                values.append(payoff)
            elif price_min <= self.L: # knock-in case
                final_price = ds_path_local.iloc[-1]
                payoff = np.exp(-self.r*self.T)*max(self.K-final_price, 0)
                values.append(payoff)
            else: # no knock-in, knock-out case
                values.append(0)
        
        value = np.mean(values) # average of KIKO payoff
        std = np.std(values) # standard deviation of KIKO payoff
        conf_interval_lower = value - 1.96 * std / math.sqrt(self.M)
        conf_interval_upper = value + 1.96 * std / math.sqrt(self.M)
        conf = [conf_interval_lower, conf_interval_upper] # 95% confidence interval of KIKO payoff

        return value, conf
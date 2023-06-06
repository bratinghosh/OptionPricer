import numpy as np


class AmericanOption:
    def __init__(self, S=None, sigma=None, r=None, T=None, K=None, N=None, type=None) -> None:
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

        assert N != None
        self.N = N

        assert type != None and (type == "call" or type == "put")
        self.type = type

    def get_price_binomial_tree(self):
        dT = float(self.T)/self.N # Time step size
        DF = np.exp(-self.r*dT) # Discount Factor
        u = np.exp(self.sigma*np.sqrt(dT)) # up movement
        d = (1/u) # down movement
        p = ((1/DF)-d)/(u-d) # Probability of up movement, (1-p) Probability of down movement

        # Calculate forward the stock prices at the leaf nodes
        stockPrices = np.asarray([(self.S*(d**j)*(u**(self.N-j))) for j in range(self.N+1)])

        if self.type == "call":
            optionPrices = np.maximum(stockPrices-self.K, 0)
        else:
            optionPrices = np.maximum(self.K-stockPrices, 0)
        
        # Calculate backward the option prices
        for _ in range(self.N):
            stockPrices = stockPrices[:-1]*d
            optionPrices = DF*((p)*optionPrices[:-1] + (1-p)*optionPrices[1:])

            if self.type == "call":
                optionPrices = np.maximum(stockPrices-self.K, optionPrices)
            else:
                optionPrices = np.maximum(self.K-stockPrices, optionPrices)
        
        optionPrice = optionPrices[0]

        return optionPrice
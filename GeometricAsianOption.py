
from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np


class GeometricAsianOption:
      def __init__(self, cp_flag=None, S=0, K=0, T=0, t=0, sigma=0, r=0, n=100):
        assert cp_flag=='call' or cp_flag=='put'
        self.S = S
        self.K = K
        self.T = T
        self.t = t
        self.sigma = sigma
        self.r = r
        self.n = n
        self.cp_flag= cp_flag

      def get_price_closed_form(self):
        cp_flag, S, K, T, t, sigma, r, n = self.cp_flag, self.S, self.K, self.T, self.t, self.sigma, self.r, self.n
        sigma_hat = sigma*sqrt(((n + 1)*(2*n + 1))/(6*n**2))
        u = (r - (1/2)*sigma**2)*((n+1)/(2*n))+(1/2)*sigma_hat**2   
        T = T-t
        d1 = (log(S/K) + (u + (1/2)*sigma_hat**2)*T)/(sigma_hat*sqrt(T))
        d2 = d1 - sigma_hat*sqrt(T)

        if cp_flag == 'call':
          price = S*exp(u*T)*exp(-r*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)  
        else:
          price = K*exp(-r*T)*norm.cdf(-d2)-S*exp(u*T)*exp(-r*T)*norm.cdf(-d1) 
        return price
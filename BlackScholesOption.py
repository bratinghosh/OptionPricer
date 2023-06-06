
from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np

class BlackScholesOption:
  
  def __init__(self, S, K, T, sigma, r, q, cp_flag=None, t=0):
    assert cp_flag == 'call' or cp_flag == 'put'
    self.cp_flag= cp_flag
    self.S = S
    self.K = K
    self.T = T
    self.t = t
    self.sigma = sigma
    self.r = r
    self.q = q

  def get_price_european(self):
    cp_flag, S, K, T, t, sigma, r, q = self.cp_flag, self.S, self.K, self.T, self.t, self.sigma, self.r, self.q
    d1 = (log(S/K) + (r-q+0.5*sigma*sigma)*(T-t)) / (sigma*sqrt(T-t))
    d2 = d1 - sigma*sqrt(T-t)
    if cp_flag == 'call':
      price = S*exp(-q*(T-t))*norm.cdf(d1)-K*exp(-r*(T-t))*norm.cdf(d2)  
    else:
      price = K*exp(-r*(T-t))*norm.cdf(-d2)-S*exp(-q*(T-t))*norm.cdf(-d1)
    return price


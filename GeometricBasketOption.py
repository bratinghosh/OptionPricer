
from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np


class GeometricBasketOption:
    def __init__(self, cp_flag=None, S=0, K=0, T=0, t=0, sigma=0, r=0, corr=0):
        assert cp_flag=='call' or cp_flag=='put'
        self.S = S
        self.K = K
        self.T = T
        self.t = t
        self.sigma = sigma
        self.r = r
        self.corr = corr
        self.cp_flag= cp_flag


    def get_price_closed_form(self):
        cp_flag, S, K, T, t, sigma, r, corr = self.cp_flag, self.S, self.K, self.T, self.t, self.sigma, self.r, self.corr
        T = T - t
        S, sigma = np.array(S), np.array(sigma)
        corr_matrix = np.array([1,corr])
        S_basket = exp((np.sum(np.log(S)))/len(S)) 
        corr_matrix = corr_matrix[np.abs(np.arange(corr_matrix.size) - np.arange(corr_matrix.size).reshape(corr_matrix.size,-1) )]
        basket_sigma = (1/len(S))*((np.matmul(np.matmul(sigma,corr_matrix),sigma))**0.5)
        u = r - 0.5*(1/len(S))*np.sum(np.square(sigma)) + 0.5*basket_sigma**2
        d1 = (log(S_basket/K) + (u + (1/2)*basket_sigma**2)*T)/(basket_sigma*sqrt(T))
        d2 = d1 - basket_sigma*sqrt(T)

        if cp_flag == 'call':
          price = S_basket*exp(u*T)*exp(-r*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)        
        else:
          price = K*exp(-r*T)*norm.cdf(-d2)-S_basket*exp(u*T)*exp(-r*T)*norm.cdf(-d1) 
        return price




from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np


class ArithmeticAsianOption:
      def __init__(self, cp_flag=None, S=0, K=0, T=0, t=0, sigma=0, r=0, n=100, M = 100000, control_variate=False):
        assert cp_flag=='call' or cp_flag=='put'
        assert control_variate==True or control_variate==False
        self.S = S
        self.K = K
        self.T = T
        self.t = t
        self.sigma = sigma
        self.r = r
        self.n = n
        self.M = M
        self.cp_flag= cp_flag
        self.control_variate =  control_variate

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

      def get_price_monte_carlo(self):
        cp_flag, S, K, T, t, sigma, r, n, M, control_variate = self.cp_flag, self.S, self.K, self.T, self.t, self.sigma, self.r, self.n, self.M, self.control_variate
        T = T - t
        np.random.seed(8000)
        drift = (r - 0.5*sigma**2)*(T/n)
        sPath = S* np.cumprod(np.exp(drift + ((sigma * np.sqrt(T/n))*(np.random.randn(M,n)))),axis=1) 

        if cp_flag=='call':
            arith_pnl = exp(-r*T)*np.maximum(np.subtract(np.mean(sPath,1),K), 0)
        else:
            arith_pnl = exp(-r*T)*np.maximum(np.subtract(K,np.mean(sPath,1)), 0)

        if not control_variate:
            Pmean = np.mean(arith_pnl) 
            Pstd = np.std(arith_pnl) 
            confmc = [Pmean-1.96*Pstd/sqrt(M), Pmean+1.96*Pstd/sqrt(M)] 
            return Pmean, confmc

        else:
            if cp_flag=='call':
                geo_pnl = exp(-r*T)*np.maximum(np.subtract(np.exp((1/n)*np.sum(np.log(sPath),1)),K), 0)
                geo_pnl = geo_pnl.reshape(geo_pnl.shape[0],1)

            else:
                geo_pnl = exp(-r*T)*np.maximum(np.subtract(K,np.exp((1/n)*np.sum(np.log(sPath),1))), 0)
                geo_pnl = geo_pnl.reshape(geo_pnl.shape[0],1)

            if np.var(geo_pnl) == 0:
                return 0,[0,0]

            arith_pnl = arith_pnl.reshape(arith_pnl.shape[0],1)
            covXY = np.mean(np.multiply(arith_pnl,geo_pnl)) - np.mean(arith_pnl)*np.mean(geo_pnl)
            theta = covXY/np.var(geo_pnl)

            Z = arith_pnl + theta * (self.get_price_closed_form() - geo_pnl) 
            Zmean = np.mean(Z) 
            Zstd = np.std(Z) 
            confcv = [Zmean-1.96*Zstd/sqrt(M), Zmean+1.96*Zstd/sqrt(M)] 
            return Zmean, confcv



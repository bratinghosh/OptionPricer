import numpy as np
from scipy.stats import norm

class ArithmeticBasketOption:
    def __init__(self, r, sigma1, sigma2, T, S10, S20, K, rho, M, option_type, control_variate):
        self.r = r
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.T = T
        self.S10 = S10
        self.S20 = S20
        self.K = K
        self.rho = rho
        self.M = int(M)
        self.option_type = option_type
        self.control_variate = control_variate

    
    def stock_path_simulations(self):
        np.random.seed(8000)
        factor1 = self.S10 * np.exp((self.r - 0.5 * self.sigma1 * self.sigma1) * self.T)
        factor2 = self.S20 * np.exp((self.r - 0.5 * self.sigma2 * self.sigma2) * self.T)
        std1 = self.sigma1 * np.sqrt(self.T)
        std2 = self.sigma2 * np.sqrt(self.T)
        Z1 = np.random.standard_normal(self.M)
        Z2 = Z1*self.rho + np.sqrt(1-self.rho**2) * np.random.standard_normal(self.M)
        factorArray1 = std1 * Z1
        factorArray2 = std2 * Z2
        sArray1 = factor1 * np.exp(factorArray1)
        sArray2 = factor2 * np.exp(factorArray2)
        return sArray1, sArray2

    def basket_options_payoffs(self):
        sArray1, sArray2 = self.stock_path_simulations()
        Ba = 0.5 * (sArray1 + sArray2)
        Bg = np.sqrt(sArray1*sArray2)
        VBg_call_p=np.exp(-self.r*self.T)*(np.maximum(Bg-self.K,0))
        VBg_put_p=np.exp(-self.r*self.T)*np.maximum(self.K-Bg,0) 
        VBa_call_p=np.exp(-self.r*self.T)*np.maximum(Ba-self.K,0)
        VBa_put_p=np.exp(-self.r*self.T)*np.maximum(self.K-Ba,0)
        return VBg_call_p, VBg_put_p, VBa_call_p, VBa_put_p
    
    def get_price_closed_form(self):
        Bg0 = np.sqrt(self.S10 * self.S20)
        sigma_B = np.sqrt((self.sigma1**2) + 2 * self.sigma1 * self.sigma2 * self.rho + self.sigma2**2)/2
        mu = self.r - (1/2) * ((self.sigma1**2 + self.sigma2**2)/2) + (1/2) * sigma_B**2
        d1 = (np.log(Bg0/self.K) + (mu + (1/2)*sigma_B**2)*self.T)/(sigma_B*np.sqrt(self.T))
        d2 = d1 - sigma_B*np.sqrt(self.T)
        VBg_call = np.exp(-(self.r*self.T))*(Bg0*np.exp(mu*self.T)*norm.cdf(d1) - self.K*norm.cdf(d2))
        VBg_put = np.exp(-(self.r*self.T))*(self.K*norm.cdf(-d2) - Bg0*np.exp(mu*self.T)*norm.cdf(-d1))
        return VBg_call, VBg_put

    def geometric_basket(self):
        sArray1, sArray2 = self.stock_path_simulations()
        Bg = np.sqrt(sArray1*sArray2)
        VBg_call_p, VBg_put_p, VBa_call_p, VBa_put_p = self.basket_options_payoffs()  
        if self.option_type == "call":
            VBgMC = np.mean(VBg_call_p)
        elif self.option_type == "put":
            VBgMC = np.mean(VBg_put_p)
        return VBgMC

    def get_price_monte_carlo(self):
        sArray1, sArray2 = self.stock_path_simulations()
        VBg_call,VBg_put = self.get_price_closed_form()
        VBg_call_p, VBg_put_p, VBa_call_p, VBa_put_p = self.basket_options_payoffs()
        if self.option_type == "call":
            if self.control_variate == True:
                cov = np.mean(VBa_call_p*VBg_call_p)-np.mean(VBg_call_p)*np.mean(VBa_call_p)
                theta = cov / np.var(VBg_call_p)
                VBa = VBa_call_p + theta * (VBg_call-VBg_call_p)
                VBaMC = np.mean(VBa)
                conf_int=[VBaMC - 1.96 * np.std(VBa) / np.sqrt(self.M), VBaMC + 1.96 * np.std(VBa) / np.sqrt(self.M)]
            else:
                VBaMC = np.mean(VBa_call_p)
                conf_int=[VBaMC - 1.96 * np.std(VBa_call_p) / np.sqrt(self.M), VBaMC + 1.96 * np.std(VBa_call_p) / np.sqrt(self.M)]
        elif self.option_type == "put":
            if self.control_variate == True:
                cov = np.mean(VBa_put_p*VBg_put_p)-np.mean(VBg_put_p)*np.mean(VBa_put_p)
                theta = cov / np.var(VBg_put_p)
                VBa = VBa_put_p + theta * (VBg_put-VBg_put_p)
                VBaMC = np.mean(VBa)
                conf_int=[VBaMC - 1.96 * np.std(VBa) / np.sqrt(self.M), VBaMC + 1.96 * np.std(VBa) / np.sqrt(self.M)]
            else:
                VBaMC = np.mean(VBa_put_p)
                conf_int=[VBaMC - 1.96 * np.std(VBa_call_p) / np.sqrt(self.M), VBaMC + 1.96 * np.std(VBa_call_p) / np.sqrt(self.M)]
        return VBaMC, conf_int


# b = ArithmeticBasketOption(0.05, 0.3, 0.3, 3, 100, 100, 100, 0.5, 100000, "call",True)
# a = b.get_price_monte_carlo()
# print(a)

        

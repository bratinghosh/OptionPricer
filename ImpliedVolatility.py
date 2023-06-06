import math
from scipy.stats import norm


def get_implied_volatility(S, r, q, T, K, V, option_type, guess=0.5):
    def d1(sigma):
        d1 = (math.log(S / K) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
        return d1

    def d2(sigma):
        d2 = d1(sigma) - sigma * math.sqrt(T)
        return d2

    def bs_price(sigma):
        if option_type == "call":
            bs_price = S * math.exp(-q * T) * norm.cdf(d1(sigma)) - K * math.exp(-r * T) * norm.cdf(d2(sigma))
        elif option_type == "put":
            bs_price = K * math.exp(-r * T) * norm.cdf(-d2(sigma)) - S * math.exp(-q * T) * norm.cdf(-d1(sigma))
        return bs_price

    def bs_vega(sigma):
        vega = S * math.exp(-q * T) * norm.pdf(d1(sigma)) * math.sqrt(T)
        return vega

    # Use Newton Raphson method to calculate implied volatility
    tolerance = 1e-6
    max_iterations = 100
    sigma = guess
    for i in range(max_iterations):
        price = bs_price(sigma)
        vega = bs_vega(sigma)
        diff = price - V
        if abs(diff) < tolerance:
            return sigma
        sigma = sigma - diff / vega
    return None

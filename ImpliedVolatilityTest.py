from ImpliedVolatility import get_implied_volatility

# Implied Volatility Test cases
S = 2
r = 0.03
q = 0.00
T = 3
K = 2
V = 0.48413599739115154
option_type = "call"

implied_vol = get_implied_volatility(S, r, q, T, K, V, option_type)
print(implied_vol)

import pandas as pd

from ArithmeticBasketOption import ArithmeticBasketOption
from GeometricBasketOption import GeometricBasketOption


# Basket Option Test cases
r = 0.05
T = 3 
S = 100
M = 10**5

test_datas = [[100, [0.3,0.3], 0.5],
            [100, [0.3,0.3], 0.9],
            [100, [0.1,0.3], 0.5],
            [80, [0.3, 0.3], 0.5],
            [120, [0.3,0.3], 0.5],
            [100, [0.5,0.5], 0.5]]

basket_data = pd.DataFrame(columns=['S1','S2','K','T', 'sigma1','sigma2', 'r', 'corr', 'type','M', 'Geometric', 'Arithmetic MC', 'MC Confidence Interval','Arithmetic Control Variate','Control Variate Confidence Interval'])
for test_data in test_datas:
    K = test_data[0]
    sigma = test_data[1]
    corr = test_data[2]
    for type in ['call','put']:
        basket_data.loc[len(basket_data)]=[S,S,K,T,sigma[0],sigma[1],r,corr,type,M,0,0,0,0,0]
        basket_geometric = GeometricBasketOption(S=[S,S],
                                                K=K,
                                                T=T,
                                                sigma=sigma,
                                                r=r,
                                                corr=corr,
                                                cp_flag=type).get_price_closed_form()
        basket_data.at[len(basket_data)-1,'Geometric']=basket_geometric
        for control_variate in [True,False]:
            basket_arithmetic = ArithmeticBasketOption(r=r,
                                                    sigma1=sigma[0],
                                                    sigma2=sigma[1],
                                                    T=T,
                                                    S10=S,
                                                    S20=S,
                                                    K=K,
                                                    rho=corr,
                                                    M=M,
                                                    option_type=type,
                                                    control_variate=control_variate).get_price_monte_carlo()
            if control_variate:
                basket_data.at[len(basket_data)-1,'Arithmetic Control Variate']=basket_arithmetic[0]
                basket_data.at[len(basket_data)-1,'Control Variate Confidence Interval']=str(basket_arithmetic[1])
            else:
                basket_data.at[len(basket_data)-1,'Arithmetic MC']=basket_arithmetic[0]
                basket_data.at[len(basket_data)-1,'MC Confidence Interval']=str(basket_arithmetic[1])
basket_data.to_csv('tests/BasketOption.csv', index=False)
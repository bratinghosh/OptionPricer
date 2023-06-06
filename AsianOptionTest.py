import pandas as pd

from ArithmeticAsianOption import ArithmeticAsianOption
from GeometricAsianOption import GeometricAsianOption


# Asian Option Test cases
r = 0.05
T = 3 
S = 100
M = 10**5

test_datas = [[100, 0.3 , 50],[100,0.3,100],[100,0.4,50]]

asian_data = pd.DataFrame(columns=['S','K','T', 'sigma', 'r', 'n', 'type','M', 'Geometric', 'Arithmetic MC','MC Confidence Interval', 'Arithmetic Control Variate','Control Variate Confidence Interval'])
for test_data in test_datas:
    K = test_data[0]
    sigma = test_data[1]
    n = test_data[2]
    for type in ['call','put']:
        asian_data.loc[len(asian_data)]=[S,K,T,sigma,r,n,type,M,0,0,0,0,0]
        asian_geometric = GeometricAsianOption(S=S,
                                    K=K,
                                    T=T,
                                    sigma=sigma,
                                    r=r,
                                    n=n,
                                    cp_flag=type).get_price_closed_form()
        asian_data.at[len(asian_data)-1,'Geometric'] = asian_geometric
        for control_variate in [True,False]:
            asian_arithmetic = ArithmeticAsianOption(S=S,
                                            K=K,
                                            T=T,
                                            sigma=sigma,
                                            r=r,
                                            n=n,
                                            M=int(M),
                                            control_variate=control_variate,
                                            cp_flag=type).get_price_monte_carlo()
            if control_variate:
                asian_data.at[len(asian_data)-1,'Arithmetic Control Variate'] = asian_arithmetic[0]
                asian_data.at[len(asian_data)-1,'Control Variate Confidence Interval'] = str(asian_arithmetic[1])
            else:
                asian_data.at[len(asian_data)-1,'Arithmetic MC'] = asian_arithmetic[0]
                asian_data.at[len(asian_data)-1,'MC Confidence Interval'] = str(asian_arithmetic[1])

asian_data.to_csv('tests/AsianOption.csv',index= False)

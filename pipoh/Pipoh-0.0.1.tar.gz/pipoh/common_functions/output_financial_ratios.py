import numpy as np
from abc import ABC, abstractmethod

@abstractmethod
def output_financial_ratios(ratios, returns, weights):
    # Save number of elements and number of assets
    n = max(returns.shape)
    MR = returns.mean()
    SR = MR/np.std(returns)

    CR = MR/ratios['MDD']

    (Q, N) = weights.shape
    turnover = (1/(Q-1))*(1/N) * sum(sum(abs(weights[2:, :]-weights[1:-1, :])))

    output_financial_ratios={}
    output_financial_ratios['MR'] = MR
    output_financial_ratios['SR'] = SR
    output_financial_ratios['CR'] = CR
    output_financial_ratios['Turnover'] = turnover

    return output_financial_ratios
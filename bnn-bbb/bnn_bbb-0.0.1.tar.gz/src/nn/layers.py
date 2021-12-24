import torch
from torch import nn
import torch.nn.functional as F
from distributions import norm_log_prob
from security import check
import numpy as np

class Linear_bnn(nn.Module):
    def __init__(self,
                 in_size,
                 out_size,
                 init_rho_post,
                 init_mu_post,
                 sigma_prior,
                 mu_prior,
                 N,
                 p,
                 init_type='fixed',
                 regime=0,
                 bias = False):
        super(Linear_bnn, self).__init__()
        self.N = N
        self.p = p
        self.regime = regime
        self.bias = bias

        self.weight_mu = self.init_parameter(init_mu_post, init_type, (out_size, in_size))
        self.weight_rho = self.init_parameter(init_rho_post, init_type, (out_size, in_size))

        if bias:
            self.bias_mu = self.init_parameter(init_mu_post, init_type, (out_size,))
            self.bias_rho = self.init_parameter(init_mu_post, init_type, (out_size,))

        self.mu_prior = mu_prior
        self.sigma_prior = sigma_prior

    def init_parameter(self, init_value, init_type, size):
        if init_type == 'fixed':
            return nn.Parameter(torch.ones(size) * init_value)
        elif init_type == 'normal':
            return nn.Parameter(torch.normal(init_value, 1., size=size))
        else:
            raise ValueError('To implement')

    def rho_to_std(self, rho):
        if self.regime == 0:
            value = torch.where(rho < 50, torch.log1p(torch.exp(rho)), rho)

        elif self.regime == 1:
            value = np.sqrt(self.N) * (1 + torch.tanh(rho / self.N)) + torch.exp(rho)
            #value = np.sqrt(self.N) + torch.log1p(torch.exp(rho))

        elif self.regime == 2:
            value = np.sqrt(self.N / self.p) + torch.log1p(torch.exp(rho))

        else:
            raise ValueError('To implement')
        check(value, items=(rho, self.N, self.p))
        return value

    def sample(self, mu, rho):
        eps = torch.normal(0., 1., size=mu.size())
        value = mu + self.rho_to_std(rho) * eps
        check(value)
        return value

    def forward(self, x):
        w = self.sample(self.weight_mu, self.weight_rho)
        log_var_post = norm_log_prob(w, self.weight_mu, self.rho_to_std(self.weight_rho))
        log_prior = norm_log_prob(w, self.mu_prior, self.sigma_prior)
        self.appro_kl = log_var_post - log_prior
        check(self.appro_kl)

        if self.bias:
            b = self.sample(self.bias_mu, self.bias_rho)
            log_var_post = norm_log_prob(b, self.bias_mu, self.rho_to_std(self.bias_rho))
            check(log_var_post)
            log_prior = norm_log_prob(b, self.mu_prior, self.sigma_prior)
            check(log_prior)
            self.appro_kl += log_var_post - log_prior
            check(self.appro_kl)
            out =  F.linear(x, w, b)
        else:
            out = F.linear(x, w, None)
        check(out)
        return out


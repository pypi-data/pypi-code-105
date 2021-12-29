import numpy as np


def selection_roulette_1(self):
    '''
    普通版本轮盘赌
    :param self:
    :return:
    '''
    FitV = self.FitV
    FitV = FitV - FitV.min() + 1e-10
    sel_prob = FitV / FitV.sum()
    # 有放回抽取,因为有放回，代表同一个染色体可以被抽到多次进行复制
    sel_index = np.random.choice(range(self.n_pop), size=self.n_pop, p=sel_prob)
    self.chrom = self.chrom[sel_index, :]
    return self.chrom


def selection_roulette_2(self):
    '''
    标准化那版本轮盘赌
    :param self:
    :return:
    '''
    FitV = self.FitV
    FitV = (FitV - FitV.min()) / (FitV.max() - FitV.min() + 1e-10) + 0.2
    # the worst one should still has a chance to be selected
    sel_prob = FitV / FitV.sum()
    # 有放回抽取
    sel_index = np.random.choice(range(self.n_pop), size=self.n_pop, p=sel_prob)
    self.chrom = self.chrom[sel_index, :]
    return self.chrom

import numpy as np


def mutation(self):
    '''
    mutation of 0/1 type chromosome
    faster than `self.Chrom = (mask + self.Chrom) % 2`
    :param self:
    :return:
    '''
    # 生成一个掩码染色体，然后异或之前的染色体
    mask = (np.random.rand(self.n_pop, self.len_chrom) < self.prob_mut)
    self.chrom ^= mask
    return self.chrom

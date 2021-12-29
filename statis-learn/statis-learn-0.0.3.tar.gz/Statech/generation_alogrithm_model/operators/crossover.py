import numpy as np


def crossover_1point(self):
    chrom, n_pop, len_chrom = self.chrom, self.n_pop, self.len_chrom
    # 每次前后两个染色体进行交叉
    for i in range(0, n_pop, 2):
        # 染色体长度中，随便选择一个点
        n = np.random.randint(0, self.len_chrom)
        # 交叉合并
        seg1, seg2 = self.chrom[i, n:].copy(), self.chrom[i + 1, n:].copy()
        self.chrom[i, n:], self.chrom[i + 1, n:] = seg2, seg1
    return self.chrom


def crossover_2point(self):
    chrom, n_pop, len_chrom = self.chrom, self.n_pop, self.len_chrom
    for i in range(0, n_pop, 2):
        # 两个点，
        n1, n2 = np.random.randint(0, self.len_chrom, 2)
        if n1 > n2:
            n1, n2 = n2, n1
        # 将两个点内的染色体交换
        seg1, seg2 = self.chrom[i, n1:n2].copy(), self.chrom[i + 1, n1:n2].copy()
        self.chrom[i, n1:n2], self.chrom[i + 1, n1:n2] = seg2, seg1
    return self.chrom

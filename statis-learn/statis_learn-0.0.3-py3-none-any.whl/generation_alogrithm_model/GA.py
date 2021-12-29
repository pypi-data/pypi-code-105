import numpy as np
from ._base import proBase
from abc import ABCMeta, abstractmethod
from .tool import func_transformer
from .operators import crossover, mutation, ranking, selection


class GeneticAlgorithmBase(proBase, metaclass=ABCMeta):
    def __init__(self,
                 fit_func,
                 n_feature,
                 n_pop=100,
                 n_gen=1000,
                 prob_mut=0.001):
        self.fit_func = func_transformer(fit_func)
        if isinstance(n_pop, int):
            self.n_pop = n_pop
        else:
            self.n_pop = round(n_pop)
        self.prob_mut = prob_mut
        self.n_gen = n_gen
        self.n_feature = n_feature

        self.chrom = None
        self.X = None  # 染色体
        self.Y_raw = None  # shape = (size_pop,) , value is f(x)
        self.Y = None  # 目标函数值
        self.fit_v = None  # shape = (size_pop,)

        self.generation_best_X = []
        self.generation_best_Y = []

        self.all_history_Y = []
        self.all_history_FitV = []

        self.best_x, self.best_y = None, None

    # 增加限制(目前暂不提供)
    def x2y(self):
        """
        1. 染色体进入目标函数运行
        2. 添加目标函数结果限制，
        :return:
        """
        self.Y_raw = self.fit_func(self.X)
        # if not self.has_constraint:
        self.Y = self.Y_raw
        # else:
        #     # constraint
        #     penalty_eq = np.array([np.sum(np.abs([c_i(x) for c_i in self.constraint_eq])) for x in self.X])
        #     penalty_ueq = np.array([np.sum(np.abs([max(0, c_i(x)) for c_i in self.constraint_ueq])) for x in self.X])
        #     self.Y = self.Y_raw + 1e5 * penalty_eq + 1e5 * penalty_ueq
        return self.Y

    @abstractmethod
    def chrom2x(self, chrom):
        pass

    @abstractmethod
    def ranking(self):
        pass

    @abstractmethod
    def selection(self):
        pass

    @abstractmethod
    def crossover(self):
        pass

    @abstractmethod
    def mutation(self):
        pass

    def run(self, n_gen=None):
        # 可以在run的时候重新设置存活代数
        self.n_gen = n_gen or self.n_gen
        for i in range(self.n_gen):
            # 二进制转实数
            self.X = self.chrom2x(self.chrom)
            # 目前没有限制条件,目标函数值
            self.Y = self.x2y()
            self.ranking()  # == self.Y
            self.selection()
            self.crossover()
            self.mutation()
            # 新一代的孩子染色体已经生成好，下面保存上一代的最好值
            # 当前这代最好目标函数的索引
            generation_best_index = self.FitV.argmax()
            # 当前这代最好的染色体实数
            self.generation_best_X.append(self.X[generation_best_index, :])
            # 当前这代最好的染色体目标函数值
            self.generation_best_Y.append(self.Y[generation_best_index])
            # 历史目标函数值
            self.all_history_Y.append(self.Y)
            # 历史繁殖了的染色体
            self.all_history_FitV.append(self.FitV)

        # 所有最好的目标函数中最小值的索引
        global_best_index = np.array(self.generation_best_Y).argmin()
        # 所有最好的目标函数中最小值的染色体
        self.best_x = self.generation_best_X[global_best_index]
        # 最小值染色体的目标函数值
        self.best_y = self.fit_func(np.array([self.best_x]))
        return self.best_x, self.best_y

    fit = run


class GA(GeneticAlgorithmBase):
    def __init__(self,
                 fit_func,
                 n_feature,
                 n_pop=100,
                 n_gen=1000,
                 prob_mut=0.001,
                 lb=[-1, -1, -1],
                 ub=[1, 1, 1],
                 precision=1e-7):
        """

        :param fit_func: 目标函数
        :param n_feature: 袋鼠特征个数
        :param n_pop: 每一代多少个袋鼠
        :param n_gen: 一个多少代
        :param prob_mut: 变异几率
        :param prob_cross: 交叉几率
        :param lb: 随机初始特征下限值
        :param ub: 随机初始特征上限值
        :param precision: func中每个变量的精度
        """
        super().__init__(fit_func, n_feature, n_pop, n_gen, prob_mut)

        self.lb = np.array(lb) if isinstance(lb, list) else lb
        self.ub = np.array(ub) if isinstance(ub, list) else ub
        # 二进制的精度
        # 精度
        self.precision = np.array(precision) * np.ones(n_feature)

        # 根据区间，生成染色体长
        # 精度：几位, 6位
        # (ub - lb) = ?
        # 2**(?-1) < ?*10^6 < 2**(?)
        # 两个方法都可以
        # Lind_raw = np.log2((self.ub - self.lb) * self.precision + 1)
        Lind_raw = np.log2((self.ub - self.lb) / self.precision + 1)
        self.Lind = np.ceil(Lind_raw).astype(int)

        # self.int_mode_ = (self.precision % 1 == 0) & (Lind_raw % 1 != 0)
        # self.int_mode = np.any(self.int_mode_)
        #
        # if self.int_mode:
        #     self.ub_extend = np.where(self.int_mode_
        #                               , self.lb + (np.exp2(self.Lind) - 1) * self.precision
        #                               , self.ub)

        # 染色体的长度 = 所有精度的总长度
        self.len_chrom = sum(self.Lind)

        self.creata_pop_chrom()

    def creata_pop_chrom(self):
        # 生成self.n_pop个二进制染色体，每个染色体长self.len_chrom
        self.chrom = np.random.randint(low=0, high=2, size=(self.n_pop, self.len_chrom))
        return self.chrom

    def gray2rv(self, gray_code):
        # 二进制转十进制
        _, len_gray_code = gray_code.shape
        b = gray_code.cumsum(axis=1) % 2
        mask = np.logspace(start=1, stop=len_gray_code, base=0.5, num=len_gray_code)
        return (b * mask).sum(axis=1) / mask.sum()

    def chrom2x(self, chrom):
        # 获取每个特征的长度
        cumsum_len_segment = self.Lind.cumsum()
        X = np.zeros((self.n_pop, self.n_feature))
        # 将第一个特征值先取出来
        chrom_temp = chrom[:, :cumsum_len_segment[0]]
        # 二进制转成实数
        X[:, 0] = self.gray2rv(chrom_temp)
        # 取出后续的值
        for feat in range(1, len(cumsum_len_segment)):
            chrom_temp = chrom[:, cumsum_len_segment[feat - 1]:cumsum_len_segment[feat]]
            X[:, feat] = self.gray2rv(chrom_temp)

        # if self.int_mode:
        #     X = self.lb + (self.ub_extend - self.lb) * X
        #     X = np.where(X > self.ub, self.ub, X)
        #     # the ub may not obey precision, which is ok.
        #     # for example, if precision=2, lb=0, ub=5, then x can be 5
        # else:
        # 将二进制设置在区内
        X = self.lb + (self.ub - self.lb) * X
        return X

    ranking = ranking.ranking
    selection = selection.selection_roulette_1
    crossover = crossover.crossover_1point
    mutation = mutation.mutation

from .Matrix import Matrix


class SparseMatrix(Matrix):
    """ Класс разряженной матрицы """

    def __init__(self, n, m):
        super(SparseMatrix, self).__init__(1, 1)
        del self.matrix
        self.n = n
        self.m = m
        self.values_dict = {}

    @staticmethod
    def get_diag_matrix(n, m, value):
        matrix = SparseMatrix(n, m)
        matrix.values_dict = {(i, i): value for i in range(matrix.n)}
        return matrix

    def set_values_dict(self, values_dict: dict):
        self.values_dict = values_dict

    def __len__(self):
        return self.n

    def __getitem__(self, item):
        item_ = item if item >= 0 else self.n - item
        if item >= self.n:
            raise StopIteration()
        return SparseMatrix.SparseVector(self.m, {k[1]: v for (k, v) in self.values_dict.items() if k[0] == item_})

    class SparseVector:
        def __init__(self, n, values_dict: dict):
            self.n = n
            self.values_dict = values_dict

        def __len__(self):
            return self.n

        def __getitem__(self, item):
            item_ = item if item >= 0 else self.n - item
            if item >= self.n:
                raise StopIteration()
            return self.values_dict.get(item_, 0)

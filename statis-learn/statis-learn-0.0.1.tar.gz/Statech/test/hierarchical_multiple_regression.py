# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import numpy as np
import pandas as pd
from Statech.linear_model import HierarchicalRegression


def main(X: pd.DataFrame, y: pd.Series, layers: list):
    reg = HierarchicalRegression()
    reg.fit(X, y, layers)
    print(reg.score(X, y, layers))


if __name__ == '__main__':
    data = pd.read_excel('../data/teenage.xlsx')
    main(data.iloc[:, 4:8], data.iloc[:, 1], [1, 1, 1, 1])

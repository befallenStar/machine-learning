# -*- encoding: utf-8 -*-
# numpy 1.15.4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# seaborn库是对matplotlib的封装，提供更加便捷的API用于数据可视化
# https://blog.csdn.net/fenfenxhf/article/details/82859620
import seaborn as sns


# 读取特征
def get_X(df):
    ones = pd.DataFrame({'ones': np.ones(len(df))})
    # 按列合并
    data = pd.concat([ones, df], axis=1)
    # 返回ndarray
    # as_matrix方法弃用
    # values属性不被推荐
    return data.iloc[:, :-1].to_numpy()


# 读取标签
def get_Y(df):
    return np.array(df.iloc[:, -1])


# 代价函数
def lr_cost(theta, X, Y):
    # 样本数
    m = X.shape[0]
    # @为矩阵点乘，相当于dot方法
    inner = X @ theta - Y
    square_sum = inner.T @ inner
    cost = square_sum / (2 * m)
    return cost


def main():
    # 读取数据并赋予列名
    # https://blog.csdn.net/zjyklwg/article/details/79556545
    # 返回值为DataFrame结构的数据，形象的看为一个二维表结构
    # 行为索引，列为标签
    # https://www.jianshu.com/p/2ef4f057fe0d
    df = pd.read_csv('ex1data1.txt', names=['population', 'profit'])

    # 展示数据基本信息，包含索引范围、各个列非空数据个数、数据类型、占用空间大小
    print("{0:*^50}".format("type of df"))
    df.info()
    print("{0:*^50}".format(''))

    # 展示数据表前5行数据
    print("{0:*^50}".format("first 5 lines of df"))
    print(df.head())
    print("{0:*^50}".format(''))

    # 将数据通过图表进行展示
    # 参数size在新版本中变为height
    sns.lmplot('population', 'profit', df, height=6, fit_reg=False)
    plt.show()

    # 查看数据维度
    print("{0:*^50}".format("dimension of data"))
    X = get_X(df)
    print('X: ', X.shape, type(X))
    Y = get_Y(df)
    print('Y: ', Y.shape, type(Y))
    print("{0:*^50}".format(''))

    print("{0:*^50}".format('cost with initial theta'))
    # 初始化参数列表
    theta = np.zeros(X.shape[1])
    # 计算损失函数
    print(lr_cost(theta, X, Y))
    print("{0:*^50}".format(''))


if __name__ == '__main__':
    main()

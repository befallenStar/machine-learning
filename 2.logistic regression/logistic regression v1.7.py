# -*- encoding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
import seaborn as sns
from sklearn.metrics import classification_report


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


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def cost(theta, X, Y):
    return np.mean(
        -Y * np.log(sigmoid(X @ theta)) - (1 - Y) * np.log(sigmoid(X @ theta)))


def gradient(theta, X, Y):
    return (1 / len(X)) * X.T @ (sigmoid(X @ theta) - Y)


def predict(X, theta):
    prob = sigmoid(X @ theta)
    # astype修改数据类型
    return (prob >= 0.5).astype(int)


# 特征映射
def feature_mapping(x, y, power, as_ndarray=False):
    data = {"f{}{}".format(i - p, p): np.power(x, i - p) * np.power(y, p)
            for i in np.arange(power + 1)
            for p in np.arange(i + 1)
            }

    if as_ndarray:
        return pd.DataFrame(data).to_numpy()
    else:
        return pd.DataFrame(data)


# 正则化代价函数
def regularized_cost(theta, X, Y, l=1):
    theta_j1_to_n = theta[1:]
    regularized_term = (l / (2 * len(X))) * np.power(theta_j1_to_n, 2).sum()
    return cost(theta, X, Y) + regularized_term


# 正则化下降
def regularized_gradient(theta, X, y, l=1):
    theta_j1_to_n = theta[1:]
    regularized_theta = (l / len(X)) * theta_j1_to_n
    regularized_term = np.concatenate([np.array([0]), regularized_theta])
    return gradient(theta, X, y) + regularized_term


def main():
    df = pd.read_csv("ex2data2.txt", names=['test1', 'test2', 'accepted'])

    # describe函数显示数据的情况，包括个数、平均数、标准差、最大最小值等
    # https://www.cnblogs.com/ffli/p/12201448.html
    print("{0:*^50}".format("basic infomation of data"))
    print(df.describe())
    print("{0:*^50}".format(""))

    # 画图查看数据分布
    sns.set(context="notebook", style="ticks",
            font_scale=1.5)
    sns.lmplot('test1', 'test2', hue='accepted', data=df,
               height=6,
               fit_reg=False,
               scatter_kws={"s": 50},
               legend_out=False
               )
    plt.title('Regularized Logistic Regression')
    plt.show()

    x1 = np.array(df.test1)
    x2 = np.array(df.test2)
    data = feature_mapping(x1, x2, power=6)
    theta = np.zeros(data.shape[1])
    X = feature_mapping(x1, x2, power=6, as_ndarray=True)
    print(X.shape)
    Y = get_Y(data)
    print(Y.shape)
    res = opt.minimize(fun=regularized_cost, x0=theta, args=(X, Y),
                       method='Newton-CG', jac=regularized_gradient)
    print(res)

    final_theta = res.x
    y_pred = predict(X, final_theta)
    print(classification_report(Y, y_pred))


if __name__ == '__main__':
    main()

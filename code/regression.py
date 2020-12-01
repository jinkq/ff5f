import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error # MSE均方误差
from sklearn.metrics import mean_absolute_error # MAEX
from sklearn.metrics import r2_score # R^2决定系数
from sklearn import preprocessing

import matplotlib.pyplot as plt

def regression_all(df):
    # print(df)
    df['Dependent Variable'] = df['Mretwd'] - df['Nrrmtdt']
    df.drop('Mretwd', axis=1, inplace=True)

    # 用14、15、16年数据回归，用17年数据验证
    df_14 = df[df.Trdmnt.str.contains('2014')]
    df_15 = df[df.Trdmnt.str.contains('2015')]
    df_16 = df[df.Trdmnt.str.contains('2016')]
    df_17 = df[df.Trdmnt.str.contains('2017')]
    train_size = len(df_14) + len(df_15) + len(df_16)
    test_size = len(df_17)

    # 数据min-max归一化
    minMaxScaler = preprocessing.MinMaxScaler()#feature_range=(-1, 1))
    
    scaler = preprocessing.MinMaxScaler()
    df = scaler.fit_transform(np.array(df.iloc[:, 3:]))
    # df = np.array(df.iloc[:, 3:])

    print(df)
    train_df = df[:train_size, :]
    test_df = df[train_size:, :]
    # train_df = scaler.fit_transform(np.array(train_df.iloc[:, 3:]))
    # test_df = scaler.fit_transform(np.array(test_df.iloc[:, 3:]))
    
    X_train = train_df[:,:-1]
    Y_train = train_df[:,-1:]
    X_test = test_df[:,:-1]
    Y_test = test_df[:,-1:]
    # print(X_train)
    
    # 用线性回归模型进行训练
    lr_model = LinearRegression()
    lr_model.fit(X_train, Y_train)

    # 预测测试集合的结果
    Y_pred_train = lr_model.predict(X_train)
    Y_pred = lr_model.predict(X_test)

    # Y_test = scaler.inverse_transform(Y_test)
    # Y_pred = scaler.inverse_transform(Y_pred)

    # # 回归评价
    print('train_R^2: ', r2_score(Y_train, Y_pred_train))
    print('R^2: ', r2_score(Y_test, Y_pred))
    print('MSE: ', mean_absolute_error(Y_test, Y_pred))
    print('MAEX: ', mean_squared_error(Y_test, Y_pred))

    plot(Y_test, Y_pred)

def plot(Y_test, Y_pred):
    # 画图
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(Y_test, color='red', label='Y_test')
    ax.plot(Y_pred, color='blue', label='Y_pred')
    plt.title('Y_test and Y_pred')
    plt.legend(loc=0,ncol=1)
    plt.savefig('../result/all.png')
    plt.show()

def plot_seperatly(Trdmnt_train, Trdmnt_test, Y_train, Y_pred_train, Y_test, Y_pred, portfolio):
    # 画图
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(Trdmnt_train, Y_train, color='red', label='Y_train')
    ax.plot(Trdmnt_train, Y_pred_train, color='blue', label='Y_pred_train')
    ax.plot(Trdmnt_test, Y_test, color='orange', label='Y_test')
    ax.plot(Trdmnt_test, Y_pred, color='gray', label='Y_pred')
    plt.title(portfolio+ ': Y_test and Y_pred')
    plt.legend(loc=0,ncol=1)
    plt.savefig('../result/' + portfolio + '.png')
    plt.show()

def regression_one_portfolio(df, portfolio):
    df = df[df['Portfolio'] == portfolio]
    # print(df)
    df['Dependent Variable'] = df['Mretwd'] - df['Nrrmtdt']
    df.drop('Mretwd', axis=1, inplace=True)

    # 用14、15、16年数据回归，用17年数据验证
    df_14 = df[df.Trdmnt.str.contains('2014')]
    df_15 = df[df.Trdmnt.str.contains('2015')]
    df_16 = df[df.Trdmnt.str.contains('2016')]
    df_17 = df[df.Trdmnt.str.contains('2017')]
    train_size = len(df_14) + len(df_15) + len(df_16)
    test_size = len(df_17)

    Trdmnt_train =  list(np.array(df)[:train_size, 0])
    Trdmnt_test = list(np.array(df)[train_size:, 0])

    # 数据min-max归一化
    minMaxScaler = preprocessing.MinMaxScaler()#feature_range=(-1, 1))
    
    scaler = preprocessing.MinMaxScaler()
    df = scaler.fit_transform(np.array(df.iloc[:, 3:]))
    # df = np.array(df.iloc[:, 3:])

    # print(df)
    train_df = df[:train_size, :]
    test_df = df[train_size:, :]
    
    X_train = train_df[:,:-1]
    Y_train = train_df[:,-1:]
    X_test = test_df[:,:-1]
    Y_test = test_df[:,-1:]

    # 用线性回归模型进行训练
    lr_model = LinearRegression()
    lr_model.fit(X_train, Y_train)

    # 预测测试集合的结果
    Y_pred_train = lr_model.predict(X_train)
    Y_pred = lr_model.predict(X_test)

    # # 回归评价
    print('2014-2016年回归数据的R^2: ', r2_score(Y_train, Y_pred_train))
    print('2017年预测数据的R^2: ', r2_score(Y_test, Y_pred))
    print('MSE: ', mean_absolute_error(Y_test, Y_pred))
    print('MAEX: ', mean_squared_error(Y_test, Y_pred))
    plot_seperatly(Trdmnt_train, Trdmnt_test, Y_train, Y_pred_train, Y_test, Y_pred, portfolio)

def regression(df):
    origin_df = pd.DataFrame(df) # 避免函数修改df
    
    # 对所有样本回归
    regression_all(df)
    
    # 对18个组合分别回归
    portfolio_list = ['SL', 'SN_BM', 'SH', 'BL', 'BN_BM', 'BH', 'SR', 'SN_OP', 'SW', 'BR',
    'BN_OP', 'BW', 'SC', 'SN_INV', 'SA', 'BC', 'BN_INV', 'BA']

    for portfolio in portfolio_list:
        regression_one_portfolio(origin_df, portfolio)

if __name__ == '__main__':
    df = pd.read_excel('../data/data_for_regression_portfolio_6.xlsx')
    regression(df)
    
    
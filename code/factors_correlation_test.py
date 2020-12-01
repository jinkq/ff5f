import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def factors_correlation_test(df):
    '''
    计算自变量之间的相关系数
    '''

    df = df[['SMB', 'HML', 'RMW', 'CMA', 'Rm-Rf']]
    print(df.corr())
    plt.rcParams['axes.unicode_minus']=False
    plt.subplots(figsize=(9, 9))
    sns.heatmap(df.corr(), annot=True, vmax=1, square=True, cmap="Blues")
    plt.savefig('../result/correlation/correlation.png')
    plt.show()

if __name__ == '__main__':
    df = pd.read_excel('../data/data_for_regression_portfolio_6.xlsx')
    factors_correlation_test(df)
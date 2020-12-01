from group import *
from regression import *


def get_rm_and_rf(year, month):
    df = pd.read_excel('../data/market/market.xlsx')
    
    df = df[df['Trdmnt'] == year + '-' + month]
    rm = df.iloc[0, 1]
    rf = df.iloc[0, 2]
    return rm, rf

def get_Mretwd(year, month):
    df = pd.read_excel('../data/stock/'+year+'-'+month+'.xlsx')
    
    df[['Stkcd']]= df[['Stkcd']].values.astype(str)
    df['Stkcd'] = df['Stkcd'].map(lambda x: (6-len(x))*'0' + x)
    df = df[df['Trdmnt'] == year + '-' + month]

    dict = {}
    for index,row in df.iterrows():
        dict[row['Stkcd']] = row['Mretwd']
    return dict

def get_portfolio_Mretwd(factor):
    dict = {}
    dict['SL'] = factor.R_SL
    dict['SN_BM'] = factor.R_SN_BM
    dict['SH'] = factor.R_SH
    dict['BL'] = factor.R_BL
    dict['BN_BM'] = factor.R_BN_BM
    dict['BH'] = factor.R_BH
    dict['SR'] = factor.R_SR
    dict['SN_OP'] = factor.R_SN_OP
    dict['SW'] = factor.R_SW
    dict['BR'] = factor.R_BR
    dict['BN_OP'] = factor.R_BN_OP
    dict['BW'] = factor.R_BW
    dict['SC'] = factor.R_SC
    dict['SN_INV'] = factor.R_SN_INV
    dict['SA'] = factor.R_SA
    dict['BC'] = factor.R_BC
    dict['BN_INV'] = factor.R_BN_INV
    dict['BA'] = factor.R_BA
    return dict


def main():
    df_for_regression = pd.DataFrame()
    factor = Factors()

    for year in ['2014', '2015', '2016', '2017']:
        # 数据时间区间为2014-06到2017-12
        low_bound = 1
        high_bound = 13
        if year == '2014':
            low_bound = 6
        # elif year == '2018':
        #     high_bound = 2

        for month in range(low_bound, high_bound): # 月度数据
            if month == 6: # 每年6月更新组合
                df = pd.read_excel('../data/metrics/'+year+'.xlsx')
                df['Stkcd'] = df['Stkcd'].astype(str)
                df['Stkcd'] = df['Stkcd'].map(lambda x: (6-len(x))*'0' + x)
                factor.update_df(df)
                factor.get_groups() # 年度确定组合

            if month < 10:
                month = '0' + str(month)
            else:
                month = str(month)
            Trdmnt = year + '-' +month
            rm, rf = get_rm_and_rf(year, month)
            Stkcd_Mretwd_dict = get_Mretwd(year, month)
            factor.update_df_Mretwd(year, month) # 更新股票的月度收益率
            # print(factor.df_SL)
            factor.get_factors() # 计算因子
            for Stkcd, Mretwd in Stkcd_Mretwd_dict.items():
                tmp = pd.DataFrame({'Trdmnt':Trdmnt, 'Stkcd':Stkcd, 'Nrrmtdt': rf, 'SMB':factor.SMB, 'HML':factor.HML, 'RMW':factor.RMW,
                 'CMA':factor.CMA, 'Rm-Rf': rm-rf, 'Mretwd':Mretwd}, index=[0])
                df_for_regression = pd.concat([df_for_regression, tmp])
            print('Finish ' + year + '-' + month)
    # print(df_for_regression)
    df_for_regression.dropna(inplace=True) # 去除缺失值
    df_for_regression.sort_values('Trdmnt', inplace=True)
    df_for_regression = df_for_regression[~df_for_regression['Mretwd'].isin([0, '0'])]
    df_for_regression.to_excel('../data/data_for_regression.xlsx', index=False)

    regression(df_for_regression) # 多元线性回归

def main_portfolio():
    df_for_regression = pd.DataFrame()
    factor = Factors()
    # portfolio_list = ['SL', 'SN_BM', 'SH', 'BL', 'BN_BM', 'BH', 'SR', 'SN_OP', 'SW', 'BR',
    # 'BN_OP', 'BW', 'SC', 'SN_INV', 'SA', 'BC', 'BN_INV', 'BA']

    for year in ['2014', '2015', '2016', '2017']:
        # 数据时间区间为2014-06到2017-12
        low_bound = 1
        high_bound = 13
        if year == '2014':
            low_bound = 6
        # elif year == '2018':
        #     high_bound = 2

        for month in range(low_bound, high_bound): # 月度数据
            if month == 6: # 每年6月更新组合
                df = pd.read_excel('../data/metrics_6/'+year+'.xlsx')
                df['Stkcd'] = df['Stkcd'].astype(str)
                df['Stkcd'] = df['Stkcd'].map(lambda x: (6-len(x))*'0' + x)
                factor.update_df(df)
                factor.get_groups() # 年度确定组合

            if month < 10:
                month = '0' + str(month)
            else:
                month = str(month)
            Trdmnt = year + '-' +month
            rm, rf = get_rm_and_rf(year, month)
            factor.update_df_Mretwd(year, month) # 更新股票组合的月度收益率
            portfolio_Mretwd_dict = get_portfolio_Mretwd(factor)
            # print(factor.df_SL)
            factor.get_factors() # 计算因子
            for portfolio, Mretwd in portfolio_Mretwd_dict.items():
                tmp = pd.DataFrame({'Trdmnt':Trdmnt, 'Portfolio':portfolio, 'Nrrmtdt': rf, 'SMB':factor.SMB, 'HML':factor.HML, 'RMW':factor.RMW,
                 'CMA':factor.CMA, 'Rm-Rf': rm-rf, 'Mretwd':Mretwd}, index=[0])
                df_for_regression = pd.concat([df_for_regression, tmp])
            print('Finish ' + year + '-' + month)
    # print(df_for_regression)
    df_for_regression.dropna(inplace=True) # 去除缺失值
    df_for_regression.sort_values('Trdmnt', inplace=True)
    df_for_regression = df_for_regression[~df_for_regression['Mretwd'].isin([0, '0'])]
    df_for_regression.to_excel('../data/data_for_regression_portfolio_6.xlsx', index=False)

    regression(df_for_regression) # 多元线性回归


if __name__ == '__main__':
    main_portfolio()
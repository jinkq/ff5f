# Fama－French 五因子模型

[toc]

## 文件夹目录

* code：代码
  * coding_index：计算指标市值Size、账面市值比BM、营运利润率OP、投资风格INV
  * factors_correlation_test：计算自变量之间的相关系数
  * group：每年划分组合及每月计算因子
  * main：数据处理+回归的主函数
  * preprocess：数据预处理
  * regression：回归
* data：处理过的数据
  * market：月度化无风险利率Nrrmtdt及考虑现金红利再投资的综合月市场回报率Cmretwdos
  * stock：各个月份A股个股的信息，包括字段：证券代码Stkcd、交易月份Trdmnt、月个股流通市值Msmvosd、考虑现金红利再投资的个股回报率Mretwd
  * metrics_6：个股各年度的市值Size、账面市值比BM、营运利润率OP、投资风格INV
  * data_for_regression_portfolio_6.xlsx：用于回归的数据
  * result：各股的财务报表数据
* ff5f_data：原始数据
* result：
  * correlation：自变量的相关系数图
  * regression：19个回归的拟合及预测曲线（1个全部样本回归+18个组合单独回归）
  * test.xlsx：回归统计检验结果

## 使用指南

* 若想从数据处理到回归走完整流程，则运行`main.py`
* 若只想进行回归部分，跳过数据处理，则运行`regression.py`

注：各个py文件均可单独运行进行测试，其中`preprocess.py`和`coding_index.py`的功能是预先生成Excel数据，只单独运行
import pandas as pd
import math
import numpy as np
from scipy.linalg import sqrtm
import matplotlib.pyplot as plt

df = pd.read_csv('THE CLIENT\'S MONTE CARLO SIMULATION OUTPUT FILE.csv')
question_1 = bool(input('Wanna know what outputs are accessible? Please answer \'True\' if you hope to, otherwise type in \'False\'.'))

if question_1:
    outputs = df.columns.to_list()
    print(outputs)
else:
    print("Let's get straight into the corporate credit yield martingale test!\n")

curr = input('Specify the currency (USD/HKD): \n')
rating = int(input('Specify the rating using number (1:AAA, 2:AA, 3:A, 4:BBB, 5:BB, 6:B, 7:C, 8:D): \n'))
term = int(input('Specify the term (from 1 to 100): \n'))
recovery_rate = float(input('Since the economic scenario generator assumes constant recovery rate, please specify the recovery rate (0~1): \n'))

df1 = df.copy()
df1['Year'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.year
df1['Year'] -= df1['Year'].iloc[0]

print("I am constructing Credit Constant Maturity Index (CMI) as the asset price.\n")

df1[f'{curr}_Corp_{rating}_{term}_CMI'] = 0.0
df1.loc[0, f'{curr}_Corp_{rating}_{term}_CMI'] = 1
df1[f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = 0.0
scenario_num = df1['ScenID'].max()
year_num = len(df1['Year'])
index_num = len(df1)
for j in range(1, scenario_num + 1):
    df1.loc[j, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_1_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_1_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_1_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_1_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_2_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_2_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_2_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_2_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_3_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_3_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_3_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_3_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_4_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_4_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_4_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_4_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_5_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_5_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_5_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_5_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_6_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_6_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_6_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_6_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Transition_Prob_{rating}_7_1'] * df1.loc[j, f'{curr}_Corp_Transition_Prob_{rating}_7_1']) * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_7_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_7_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[0, f'{curr}_Corp_Default_Prob_{rating}_1'] * df1.loc[j, f'{curr}_Corp_Default_Prob_{rating}_1']) * recovery_rate
    df1.loc[j, f'{curr}_Corp_{rating}_{term}_CMI'] = df1.loc[0, f'{curr}_Corp_{rating}_{term}_CMI'] * (df1.loc[j, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}']/math.exp(-(term + 0.5) * (df1.loc[0, f'{curr}_Corp_Credit_Yield_{rating}_{term}'] + df1.loc[0, f'{curr}_Corp_Credit_Yield_{rating}_{term + 1}']) / 2))
for i in range(scenario_num + 1, index_num):
    df1.loc[i, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_1_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_1_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_1_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_1_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_2_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_2_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_2_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_2_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_3_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_3_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_3_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_3_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_4_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_4_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_4_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_4_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_5_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_5_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_5_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_5_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_6_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_6_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_6_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_6_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Transition_Prob_{rating}_7_1'] * df1.loc[i, f'{curr}_Corp_Transition_Prob_{rating}_7_1']) * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_7_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_7_{term - 1}'])/2) + \
                                                                       math.sqrt(df1.loc[i - scenario_num, f'{curr}_Corp_Default_Prob_{rating}_1'] * df1.loc[i, f'{curr}_Corp_Default_Prob_{rating}_1']) * recovery_rate
    df1.loc[i, f'{curr}_Corp_{rating}_{term}_CMI'] = df1.loc[i - scenario_num, f'{curr}_Corp_{rating}_{term}_CMI'] * (df1.loc[i, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}']/math.exp(-(term + 0.5) * (df1.loc[i - scenario_num, f'{curr}_Corp_Credit_Yield_{rating}_{term}'] + df1.loc[i - scenario_num, f'{curr}_Corp_Credit_Yield_{rating}_{term + 1}']) / 2))
print("Constructing CMI complete. The following are the samples for your inspection: \n")
print(df1[f'{curr}_Corp_{rating}_{term}_CMI'].head())

print("Now, I am deflating CMIs because deflated asset price is a martingale under risk-neutral measure.\n")
df1[f'{curr}_Corp_{rating}_{term}_CMI_Deflated'] = df1[f'{curr}_Corp_{rating}_{term}_CMI'] * df1[f'{curr}_RiskFree_Deflator']
summary_1 = df1.groupby('Year')[f'{curr}_Corp_{rating}_{term}_CMI_Deflated'].mean().to_frame()
print("Deflation complete. Now I will draw the deflated CMI's time-series graph.\n")
ax = summary_1.plot(figsize=(12,4))
ax.axhline(y=1, color = 'red', linestyle = '--', linewidth = 1, label = 'Martingale Benchmark')
ax.legend()
ax.set_ylim(0.5, 1.5)
print("Drawing complete.\n")
plt.show()
print("Notice that previously when deriving the realized transition proportion, we used a geometric average of rating transition probabilities of the last timepoitn and the current timepoint.\n")
print("Now, we would like to conduct another martingale test where the realized transition proportion will be derived by calculating the absolute value of the multiplication of the last transition matrix and the current transition matrix.\n")

print("First, let's define helper functions: trans_mat & real_mat!\n")

def trans_mat(curr : str, SubRisks : pd.DataFrame, sim: int = 0) -> np.array:
    Max_State = 8
    Matrix = np.zeros((Max_State, Max_State))
    Matrix[Max_State - 1, Max_State - 1] = 1
    for col in range(Max_State - 1):
        for row in range(Max_State):
            Matrix[row, col] = SubRisks.loc[sim, f'{curr}_Corp_Transition_Prob_{col+1}_{row+1}_1' if row < 7 else f'{curr}_Corp_Default_Prob_{col+1}_1']
    return Matrix

def real_mat(init_mat : np.array, curr_mat : np.array) -> np.array:
    mul_mat = np.matmul(curr_mat, init_mat)
    real = sqrtm(mul_mat)
    return real
print("Now, we have the necessary toolkit!\n")

df2 = df.copy()
df2['Year'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.year
df2['Year'] -= df2['Year'].iloc[0]

print("I am constructing Credit Constant Maturity Index (CMI) as the asset price.\n")

df2[f'{curr}_Corp_{rating}_{term}_CMI'] = 0.0
df2.loc[0, f'{curr}_Corp_{rating}_{term}_CMI'] = 1
df2[f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = 0.0
scenario_num = df2['ScenID'].max()
year_num = len(df2['Year'])
index_num = len(df2)
Trans_Matrices = []
for idx in range(index_num):
    Trans_Matrices.append(trans_mat(curr,df2, idx))

print("Transition matrices construction complete.\n")
print("Then, let's constructed the realized transition proportion matrix from year 1!\n")

Realized_Matrices = []
for j in range(1, scenario_num + 1):
    Realized_Matrices.append(real_mat(Trans_Matrices[0], Trans_Matrices[j]))
for i in range(scenario_num + 1, index_num):
    Realized_Matrices.append(real_mat(Trans_Matrices[i - scenario_num], Trans_Matrices[i]))
print("Realized transition proportion matrices construction complete.\n")

for j in range(1, scenario_num + 1):
    df2.loc[j, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = Realized_Matrices[j-1][0][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_1_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_1_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][1][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_2_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_2_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][2][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_3_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_3_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][3][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_4_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_4_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][4][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_5_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_5_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][5][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_6_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_6_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][6][rating - 1] * math.exp(-(term - 0.5) * (df.loc[j, f'{curr}_Corp_Credit_Yield_7_{term}'] + df.loc[j, f'{curr}_Corp_Credit_Yield_7_{term - 1}'])/2) + \
                                                                       Realized_Matrices[j-1][7][rating - 1] * recovery_rate
    df2.loc[j, f'{curr}_Corp_{rating}_{term}_CMI'] = df2.loc[0, f'{curr}_Corp_{rating}_{term}_CMI'] * (df2.loc[j, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}']/math.exp(-(term + 0.5) * (df2.loc[0, f'{curr}_Corp_Credit_Yield_{rating}_{term}'] + df2.loc[0, f'{curr}_Corp_Credit_Yield_{rating}_{term + 1}']) / 2))
for i in range(scenario_num + 1, index_num):
    df2.loc[i, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}'] = Realized_Matrices[i-1][0][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_1_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_1_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][1][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_2_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_2_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][2][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_3_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_3_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][3][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_4_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_4_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][4][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_5_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_5_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][5][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_6_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_6_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][6][rating - 1] * math.exp(-(term - 0.5) * (df.loc[i, f'{curr}_Corp_Credit_Yield_7_{term}'] + df.loc[i, f'{curr}_Corp_Credit_Yield_7_{term - 1}'])/2) + \
                                                                       Realized_Matrices[i-1][7][rating - 1] * recovery_rate
    df2.loc[i, f'{curr}_Corp_{rating}_{term}_CMI'] = df2.loc[i - scenario_num, f'{curr}_Corp_{rating}_{term}_CMI'] * (df2.loc[i, f'{curr}_Corp_Value_{rating}_{term + 1}_to_*_{term}']/math.exp(-(term + 0.5) * (df2.loc[i - scenario_num, f'{curr}_Corp_Credit_Yield_{rating}_{term}'] + df2.loc[i - scenario_num, f'{curr}_Corp_Credit_Yield_{rating}_{term + 1}']) / 2))
print("Constructing CMI complete. The following are the samples for your inspection: \n")
print(df2[f'{curr}_Corp_{rating}_{term}_CMI'].head())

print("Now, I am deflating CMIs because deflated asset price is a martingale under risk-neutral measure.\n")
df2[f'{curr}_Corp_{rating}_{term}_CMI_Deflated'] = df2[f'{curr}_Corp_{rating}_{term}_CMI'] * df2[f'{curr}_RiskFree_Deflator']
summary_1 = df2.groupby('Year')[f'{curr}_Corp_{rating}_{term}_CMI_Deflated'].mean().to_frame()
print("Deflation complete. Now I will draw the deflated CMI's time-series graph.")
ax = summary_1.plot(figsize=(12,4))
ax.axhline(y=1, color = 'red', linestyle = '--', linewidth = 1, label = 'Martingale Benchmark')
ax.legend()
ax.set_ylim(0.5, 1.5)
print("Drawing complete.\n")
plt.show()

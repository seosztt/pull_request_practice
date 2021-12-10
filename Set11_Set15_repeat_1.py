# -*- coding: utf-8 -*-
"""
Created on 2021

@author: Administrator
"""

#%%

# =============================================================================
# =============================================================================
# # 문제 11 유형(DataSet_11.csv 이용)

# 구분자 : comma(“,”), 470 Rows, 4 Columns, UTF-8 인코딩

# 세계 각국의 행복지수를 비롯한 여러 정보를 조사한 DS리서치는
# 취합된 자료의 현황 파악 및 간단한 통계분석을 실시하고자 한다.

# 컬 럼 / 정 의 / Type
# Country / 국가명 / String
# Happiness_Rank / 당해 행복점수 순위 / Double
# Happiness_Score / 행복점수 / Double
# year / 년도 / Double
# =============================================================================
# =============================================================================

import pandas as pd

data11 = pd.read_csv('Dataset_11.csv')
data11.info()
#%%

# =============================================================================
# 1.분석을 위해 3년 연속 행복지수가 기록된 국가의 데이터를 사용하고자 한다. 
# 3년 연속 데이터가 기록되지 않은 국가의 개수는?
# - 국가명 표기가 한 글자라도 다른 경우 다른 국가로 처리하시오.
# - 3년 연속 데이터가 기록되지 않은 국가 데이터는 제외하고 이를 향후 분석에서
# 활용하시오.(답안 예시) 1
# =============================================================================

data11.columns
len(data11.Country.unique())

data11.year.unique()

q1=data11.copy()
q1_out = q1.Country.value_counts()

len(q1_out[q1_out == 3])
len(data11.Country.unique()) - len(q1_out[q1_out == 3])
# 답: 20

#%%

# =============================================================================
# 2.(1번 산출물을 활용하여) 2017년 행복지수와 2015년 행복지수를 활용하여 국가별
# 행복지수 증감률을 산출하고 행복지수 증감률이 가장 높은 3개 국가를 행복지수가
# 높은 순서대로 차례대로 기술하시오.
# 증감률 = (2017년행복지수−2015년행복지수)/2
# 
# - 연도는 년월(YEAR_MONTH) 변수로부터 추출하며, 연도별 매출금액합계는 1월부터
# 12월까지의 매출 총액을 의미한다. (답안 예시) Korea, Japan, China
# =============================================================================

q1_out = q1_out[q1_out == 3]
q1_out.index

q2=data11[data11.Country.isin(q1_out.index)]
q2=pd.pivot_table(q2, index='Country', columns='year', values='Happiness_Score')

q2['ratio'] = (q2[2017] - q2[2015]) / 2

q2.sort_values(by='ratio')
q2.nlargest(3, 'ratio')

# 답: Latvia, Romania, Togo
#%%

# =============================================================================
# 3.(1번 산출물을 활용하여) 년도별 행복지수 평균이 유의미하게 차이가 나는지
# 알아보고자 한다. 
# 이와 관련하여 적절한 검정을 사용하고 검정통계량을 기술하시오.
# - 해당 검정의 검정통계량은 자유도가 2인 F 분포를 따른다.
# - 검정통계량은 소수점 넷째 자리까지 기술한다. (답안 예시) 0.1234
# =============================================================================

# (참고)
# from statsmodels.formula.api import ols
# from statsmodels.stats.anova import anova_lm

from scipy.stats import f_oneway
from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

basetable=data11[data11.Country.isin(q1_out.index)]
q3=pd.pivot_table(basetable, index='Country', columns='year', values='Happiness_Score')

f_oneway(q3[2015], q3[2016], q3[2017])
# F_onewayResult(statistic=0.004276725037689305, pvalue=0.9957324489944479)

ols1 = ols('Happiness_Score ~ C(year)', basetable).fit()
anova_lm(ols1)

# 답: 0.0042

comp_out=\
 pairwise_tukeyhsd(basetable['Happiness_Score'],
                   basetable['year'])

print(comp_out)

#%%

# =============================================================================
# =============================================================================
# # 문제 12 유형(DataSet_12.csv 이용)

# 구분자 : comma(“,”), 5000 Rows, 7 Columns, UTF-8 인코딩

# 직장인의 독서 실태를 분석하기 위해서 수도권 거주자 5000명을
# 대상으로 간단한 인적 사항과 연간 독서량 정보를 취합하였다.

# 컬 럼 / 정 의 / Type
# Age / 나이 / String
# Gender / 성별(M: 남성) / String
# Dependent_Count / 부양가족 수 / Double
# Education_Level / 교육 수준 / String
# is_Married / 결혼 여부(1: 결혼) / Double
# Read_Book_per_Year / 연간 독서량(권) / Double
# Income_Range / 소득 수준에 따른 구간(A < B < C < D < E)이며 X는
# 정보 누락 / String
# =============================================================================
# =============================================================================

data12=pd.read_csv('DataSet_12.csv')
data12.info()

#%%

# =============================================================================
# 1.수치형 변수를 대상으로 피어슨 상관분석을 실시하고 연간 독서량과 가장
# 상관관계가 강한 변수의 상관계수를 기술하시오
# - 상관계수는 반올림하여 소수점 셋째 자리까지 기술하시오. (답안 예시) 0.123
# =============================================================================

data12.corr()


# 답: 0.797



#%%

# =============================================================================
# 2.석사 이상(석사 및 박사) 여부에 따라서 연간 독서량 평균이 유의미하게 다른지 가설
# 검정을 활용하여 알아보고자 한다. 독립 2표본 t검정을 실시했을 때 
# 유의 확률(pvalue)의 값을 기술하시오.
# - 등분산 가정 하에서 검정을 실시한다.
# - 유의 확률은 반올림하여 소수점 셋째 자리까지 기술한다. (답안 예시) 0.123
# =============================================================================

data12.Education_Level.unique()

q2=data12.copy()
from scipy.stats import ttest_ind
import numpy as np

q2['edu_gr']=np.where(q2.Education_Level.isin(['석사','박사']), 1 ,0)

# q2['group']=q2['Education_Level'].isin(['석사', '박사'])+0

g1=q2[q2.edu_gr==1]['Read_Book_per_Year']
g0=q2[q2.edu_gr==0]['Read_Book_per_Year']
ttest_ind(g1, g0, equal_var=True)

# 답: 0.269


#%%

# =============================================================================
# 3.독서량과 다른 수치형 변수의 관계를 다중선형회귀분석을 활용하여 알아보고자 한다. 
# 연간 독서량을 종속변수, 나머지 수치형 자료를 독립변수로 한다. 이렇게 생성한
# 선형회귀 모델을 기준으로 다른 독립변수가 고정이면서 나이만 다를 때, 40살은 30살
# 보다 독서량이 얼마나 많은가?
# - 학사 이상이면서 소득 구간 정보가 있는 데이터만 사용하여 분석을 실시하시오.
# - 결과값은 반올림하여 정수로 표기하시오. (답안 예시) 1
# =============================================================================

# (참고)
# from statsmodels.formula.api import ols


q3=data12.copy()
q3['Income_Range']

q3=q3[~(q3.Education_Level == '고졸')]
q3=q3[~(q3.Income_Range == 'X')]
# 수치형 변수: Age, Dependent_Count

from statsmodels.formula.api import ols

ols12=ols('Read_Book_per_Year~Age+Dependent_Count', q3).fit()

ols12.summary()


# 답: 8






#%%

# =============================================================================
# =============================================================================
# # 문제 13 유형(DataSet13_train.csv / DataSet13_test.csv  이용)

# 구분자 : 
#     comma(“,”), 1500 Rows, 10 Columns, UTF-8 인코딩 / 
#     comma(“,”), 500 Rows, 10 Columns, UTF-8 인코딩

# 전국의 데이터 분석가 2000명을 대상으로 이직 관련 설문조사를 실시하였다. 
# 설문 대상자의 특성 및 이직 의사와 관련 인자를 면밀히 살펴보기 위해 다양한
# 분석을 실시하고자 한다.

# 컬 럼 / 정 의 / Type
# city_development_index / 거주 도시 개발 지수 / Double
# gender / 성별 / String
# relevent_experience / 관련 직무 경험 여부(1 : 유경험) / Integer
# enrolled_university / 대학 등록 형태(1 : 풀타임/파트타임) / Integer
# education_level / 교육 수준 / String
# major_discipline / 전공 / String
# experience / 경력 / Double
# last_new_job / 현 직장 직전 직무 공백 기간 / Double
# training_hours / 관련 직무 교육 이수 시간 / Double
# target / 이직 의사 여부(1 : 의사 있음) / Integer
# =============================================================================
# =============================================================================

import pandas as pd
train=pd.read_csv('DataSet_13_train.csv')
test=pd.read_csv('DataSet_13_test.csv')
train.info()
#%%

# =============================================================================
# 1.(Dataset_13_train.csv를 활용하여) 경력과 최근 이직시 공백기간의 상관관계를 보고자
# 한다. 남여별 피어슨 상관계수를 각각 산출하고 더 높은 상관계수를 기술하시오.
# - 상관계수는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# =============================================================================


train[['experience', 'last_new_job']][train.gender=='Male'].corr()
train[['experience', 'last_new_job']][train.gender=='Female'].corr()

# 답: 0.45

#%%

# =============================================================================
# 2.(Dataset_13_train.csv를 활용하여) 기존 데이터 분석 관련 직무 경험과 이직 의사가 서로
# 관련이 있는지 알아보고자 한다. 이를 위해 독립성 검정을 실시하고 해당 검정의 p-value를 기술하시오.
# - 검정은 STEM 전공자를 대상으로 한다.
# - 검정은 충분히 발달된 도시(도시 개발 지수가 제 85 백분위수 초과)에 거주하는 사람을
# 대상으로 한다.
# - 이직 의사 여부(target)은 문자열로 변경 후 사용한다.
# - p-value는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# =============================================================================

train.major_discipline.unique()
q2_train=train[train.major_discipline=='STEM']
train.city_development_index.max()

np.percentile(train.city_development_index, [85], interpolation='lower')

sum(train.city_development_index == 0.92)

q2_train=q2_train[train.city_development_index > 0.92]

from scipy.stats import chi2_contingency

chi2, p, *_ = chi2_contingency(pd.crosstab(q2_train.relevent_experience, q2_train.target))
p

# 답: 0.64
#%%


# =============================================================================
# 3.(Dataset_13_train.csv를 활용하여) 인사팀에서는 어떤 직원이 이직 의사를 가지고 있을지
# 사전에 파악하고 1:1 면담 등 집중 케어를 하고자 한다. 이를 위해 의사결정 나무를
# 활용하여 모델을 생성하고 그 정확도를 확인하시오.
# - target을 종속변수로 하고 나머지 변수 중 String이 아닌 변수를 독립변수로 한다.
# - 학습은 전부 기본값으로 실시한다.
# - 평가는 "Dataset_13_test.csv" 데이터로 실시한다.
# - 정확도는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# 
# =============================================================================

# (참고)
# from sklearn.tree import DecisionTreeClassifier
# random_state = 123
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

train.info()
X_list=['city_development_index', 'relevent_experience', 'enrolled_university',
        'experience', 'last_new_job', 'training_hours']

dtc=DecisionTreeClassifier(random_state=123)

dtc.fit(train[X_list], train.target)
pred=dtc.predict(test[X_list])

accuracy_score(test.target, pred)

dtc.score(test[X_list], test.target)

# 답: 0.67



#%%

# =============================================================================
# =============================================================================
# # 문제 14 유형(DataSet_14.csv 이용)
#
# 구분자 : comma(“,”), 2000 Rows, 9 Columns, UTF-8 인코딩
#
# 온라인 교육업체 싱글캠퍼스에서 런칭한 교육 플랫폼을 보다
# 체계적으로 운영하기 위해 2014년부터 2016년 동안 개설된 강좌
# 2000개를 대상으로 강좌 실적 및 고객의 서비스 분석을 실시하려고
# 한다. 관련 데이터는 다음과 같다.
#
# 컬 럼 / 정 의 / Type
# id / 강좌 일련번호 / Double
# published / 강과 개설일 / String
# subject / 강좌 대주제 / String
# level / 난이도 / String
# price / 가격(만원) / Double
# subscribers / 구독자 수(결제 인원) / Double
# reviews / 리뷰 개수 / Double
# lectures / 강좌 영상 수 / Double
# duration / 강좌 총 길이(시간) / Double
# =============================================================================
# =============================================================================

data14=pd.read_csv('DataSet_14.csv')
data14.info()
#%%

# =============================================================================
# 1.결제 금액이 1억 이상이면서 구독자의 리뷰 작성 비율이 10% 이상인 교육의 수는?
# - 결제 금액은 강좌 가격에 구독자 수를 곱한 값이다.
# - 리뷰 작성 비율은 리뷰 개수에 구독자 수를 나눈 값이다. (답안 예시) 1
# =============================================================================

q1=data14.copy()

q1['total_price']=q1['price'] * q1['subscribers']
q1['reviewed_rate'] = q1['reviews']/q1['subscribers']
q1[(q1.total_price >= 10000) & (q1.reviewed_rate >= 0.1)]


# 답: 59


#%%

# =============================================================================
# 2.강좌 가격이 비쌀수록 구독자 숫자는 줄어든다는 가설을 확인하기 위해 상관분석을
# 실시하고자 한다. 2016년 개설된 Web Development 강좌를 대상으로 강좌 가격과
# 구독자 수의 피어슨 상관관계를 기술하시오.
# - 상관계수는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# =============================================================================

data14.info()
data14.subject.unique()
data14.published.unique()

q2=data14.copy()
q2['published']=pd.to_datetime(q2['published'])
q2['year']=q2['published'].dt.year

q2[(q2.year==2016) & (q2.subject=='Web Development')].corr()

# 답: 0.03
#%%

# =============================================================================
# 3.유저가 서비스 사용에 익숙해지고 컨텐츠의 좋은 내용을 서로 공유하려는 경향이
# 전반적으로 증가하는 추세라고 한다. 이를 위해 먼저 강좌 개설 년도별 구독자의 리뷰
# 작성 비율의 평균이 강좌 개설 년도별로 차이가 있는지 일원 분산 분석을 통해서
# 알아보고자 한다. 이 때 검정통계량을 기술하시오.
# - 검정통계량은 반올림하여 소수점 첫째 자리까지 기술하시오. (답안 예시) 0.1
#
# (참고)
# from statsmodels.formula.api import ols
# from statsmodels.stats.anova import anova_lm
# =============================================================================

q3=q2.copy()

q3['total_price']=q3['price'] * q3['subscribers']
q3['reviewed_rate'] = q3['reviews']/q3['subscribers']
from statsmodels.formula.api import ols
ols14=ols('reviewed_rate ~ C(year)',q3).fit()

from statsmodels.stats.anova import anova_lm
anova_lm(ols14)


# 답: 18.5




#%%


# =============================================================================
# =============================================================================
# # 문제 05 유형(Dataset_05_Mart_POS.csv /  이용)
#
# =============================================================================
# Dataset_05_Mart_POS.csv 
# 구분자 : comma(“,”), 20488 Rows, 3 Columns, UTF-8 인코딩
# =============================================================================
#
# 원룸촌에 위치한 A마트는 데이터 분석을 통해 보다 체계적인 재고관리와
# 운영을 하고자 한다. 이를 위해 다음의 두 데이터 세트를 준비하였다.
#
# 컬 럼 / 정 의 / Type
# Member_number / 고객 고유 번호 / Double
# Date / 구매일 / String
# itemDescription / 상품명 / String

# =============================================================================
# Dataset_05_item_list.csv 
# 구분자 : comma(“,”), 167 Rows, 4 Columns, UTF-8 인코
# =============================================================================
#
# 컬 럼 / 정 의 / Type
# prod_id / 상품 고유 번호 / Double
# prod_nm / 상품명 / String
# alcohol / 주류 상품 여부(1 : 주류) / Integer
# frozen / 냉동 상품 여부(1 : 냉동) / Integer
# =============================================================================
# =============================================================================

pos=pd.read_csv('Dataset_15_Mart_POS.csv')
item=pd.read_csv('Dataset_15_item_list.csv')


#%%

# =============================================================================
# 1.(Dataset_05_Mart_POS.csv를 활용하여) 가장 많은 제품이 팔린 날짜에 가장 많이 팔린
# 제품의 판매 개수는? (답안 예시) 1
# =============================================================================

pos.info()

pos.groupby('Date').count().idxmax()

pos[pos.Date == '2015-01-21'].groupby('itemDescription').count()['Member_number'].nlargest(1)





# 답: 7


#%%

# =============================================================================
# 2. (Dataset_05_Mart_POS.csv, Dataset_05_item_list.csv를 활용하여) 고객이 주류 제품을
# 구매하는 요일이 다른 요일에 비해 금요일과 토요일이 많을 것이라는 가설을 세웠다. 
# 이를 확인하기 위해 금요일과 토요일의 일별 주류제품 구매 제품 수 평균과 다른
# 요일의 일별 주류제품 구매 제품 수 평균이 서로 다른지 비교하기 위해 독립 2표본
# t검정을 실시하시오. 
# 해당 검정의 p-value를 기술하시오.
# - 1분기(1월 ~ 3월) 데이터만 사용하여 분석을 실시하시오.
# - 등분산 가정을 만족하지 않는다는 조건 하에 분석을 실시하시오.
# - p-value는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# =============================================================================

q2=pos.copy()

q2['month']=pd.to_datetime(q2.Date).dt.month

import locale
locale.locale_alias
q2['day'] = pd.to_datetime(q2.Date).dt.day_name(locale='ko_kr')
q2['fri_sat']=q2.day.isin(['금요일', '토요일'])+0

merge15=pd.merge(q2, item, left_on='itemDescription', right_on='prod_nm', how='left')
merge15=merge15[merge15.month.isin([1,2,3])]


q2_tab=pd.pivot_table(merge15, values='alcohol', index='Date', columns='fri_sat', aggfunc='sum')

g0=q2_tab[0].dropna()
g1=q2_tab[1].dropna()

from scipy.stats import ttest_ind
ttest_ind(g0, g1,equal_var=False)

# 답: 0.02
#%%

# =============================================================================
# 3.(Dataset_05_Mart_POS.csv를 활용하여) 1년 동안 가장 많이 판매된 10개 상품을 주력
# 상품으로 설정하고 특정 요일에 프로모션을 진행할지 말지 결정하고자 한다. 먼저
# 요일을 선정하기 전에 일원 분산 분석을 통하여 요일별 주력 상품의 판매 개수의
# 평균이 유의미하게 차이가 나는지 알아보고자 한다. 이와 관련하여 일원 분산 분석을
# 실시하고 p-value를 기술하시오.
# - p-value는 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 0.12
# 
# (참고)
# from statsmodels.formula.api import ols
# from statsmodels.stats.anova import anova_lm
# =============================================================================

pos.groupby('itemDescription').count()['Date'].nlargest(10).index

top10_list=['whole milk', 'other vegetables', 'rolls/buns', 'sausage', 'soda',
       'yogurt', 'tropical fruit', 'root vegetables', 'citrus fruit',
       'frankfurter']

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

q3=pos.copy()

q3['month']=pd.to_datetime(q3.Date).dt.month

import locale
locale.locale_alias
q3['day'] = pd.to_datetime(q3.Date).dt.day_name(locale='ko_kr')
q3['fri_sat']=q3.day.isin(['금요일', '토요일'])+0

merge15_3=pd.merge(q3, item, left_on='itemDescription', right_on='prod_nm', how='left')


merge15_3.columns

merge15_3.day
top10_dataset=merge15_3[merge15_3.itemDescription.isin(top10_list)]

q3_tab=top10_dataset.groupby('Date').count()[['itemDescription', 'day']]


q3_tab['day']=pd.to_datetime(q3_tab.index).day_name(locale='ko_kr')

aov=ols('itemDescription~C(day)', q3_tab).fit()
anova_lm(aov)

# 답: 0.52


q3_tab=pd.pivot_table(top10_dataset, index=['Date', 'day'], values='itemDescription', aggfunc='count')
q3_tab.reset_index()

aov=ols('itemDescription~C(day)', q3_tab.reset_index()).fit()
anova_lm(aov)





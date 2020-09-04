import pandas as pd
import numpy as np
import matplotlib.pylab as plt


def linear_regression(Read_value, x, y, x_compare, y_compare):

    # .csv 파일을 읽어옴
    x_regressor = Read_value[x]
    y_response = Read_value[y]

    # x, y값의 평균
    x_avg = np.mean(x_regressor)
    y_avg = np.mean(y_response)

    # x,y의 편차의 제곱의 합
    Sxx = np.sum((x_regressor-x_avg)**2)
    Syy = np.sum((y_response-y_avg)**2)

    #  x,y 편차 곱의 합
    Sxy = np.sum((x_regressor-x_avg) * (y_response-y_avg))

    # 기울기, y절편 계산, 공식 이용
    m = Sxy/Sxx
    b = y_avg - x_avg * m

    if y_compare >= x_compare * m + b:
        # print("당신의 소득 수준은 높습니다.")
        return 1
    else:
        # print("당신의 소득 수준은 낮습니다.")
        return 0


"""
상품 추천용 선형회귀 로직(매개변수:테스트 케이스 담은 테이블, 나이, 돈, 신용등급, ???, 유저나이, 유저돈, 유저신용등급)
    #사실 나이 돈 신용등급은 나중에 테이블 행 이름 바뀔수도 있을까봐 매개변수로 뒀다.ex) 모르고 Age를 age로 쓸것을 대비하여...
    Age에 테이블 모든 age 값을 20으로 나누고 이 값으로 1을 나눈 다음에 Age에 할당한다
    Money에 테이블 모든 money 값을 1000000000으로 나눠 할당한다.
    Credit_Level에 테이블 모든 값으로 1을 나눠 할당한다.
    x_regressor에 위에 3가지 값을 더해 할당한다.
    y_regressor에 테이블의 모든 grade 값을 할당한다. (grade가 상품추천용 등급에 해당한다.)
    plt.plot은 위에 regressor 값들로 빨간 점을 찍는다
    plt.xlabel은 그래프 x축 이름을 정하는 것이다.
    plt.ylabel은 그래프 y축 이름을 정하는 것이다.
    
    x_avg에 넘파이의 mean()함수를 사용해 x_regressor의 평균을 저장한다.
    y_avg에 넘파이의 mean()함수를 사용해 y_regressor의 평균을 저장한다. 
    
    Sxx에 넘파이의 sum()함수를 사용해 x_regressor에 x_regressor의 평균을 뺀 것을 제곱한 것들의 총합을 저장한다.
    Syy에 넘파이의 sum()함수를 사용해 y_regressor에 y_regressor의 평균을 뺀 것을 제곱한 것들의 총합을 저장한다.
    
    Sxy에 넘파이의 sum()함수를 사용해 x_regressor에 x_regressor의 평균을 뺀 것과 y_regressor에 y_regressor의 평균을 뺀것 끼리 곱한다.
    
    m은 기울기로 Sxy를 Sxx로 나눈다.
    b는 y절편으로 y평균에 x평균과 기울기를 곱한 것을 뺀다.
    
    usersum에 유저 나이와 유저 돈, 유저 신용등급을 0-1로 바꿔 더한 뒤 할당한다.
    
    식에 y 값에 해당하는 usersum * 기울기 + y절편을 반환한다.
    
    plt.plot으로 그래프에 1차식 선을 그린다.
    
    plt.show로 완성된 그래프를 출력한다.
"""


def linear_regression_suggest(full_reg_Table, age, money, credit_level, grade,
                              userage, usermoney, usercredit_level):  # 앞 글자가 소문자인건 매개변수
    Age = 1/(full_reg_Table[age]/20)  # 나이 20-80세를 0-1로 바꾼 것
    Money = full_reg_Table[money]/1000000000  # 돈 10만원부터 10억까지를 0-1로 바꿈
    Credit_Level = 1/full_reg_Table[credit_level]  # 신용등급 1-8등급 까지를 0-1로 바꿈
    x_regressor = Age + Money + Credit_Level
    y_regressor = full_reg_Table[grade]
    plt.plot(x_regressor, y_regressor, 'ro')
    plt.xlabel("sum(Age,Money,Credit_Level)")
    plt.ylabel("grade")

    x_avg = np.mean(x_regressor)
    y_avg = np.mean(y_regressor)

    Sxx = np.sum((x_regressor - x_avg) ** 2)
    Syy = np.sum((y_regressor - y_avg) ** 2)

    Sxy = np.sum((x_regressor - x_avg) * (y_regressor - y_avg))

    m = Sxy / Sxx
    b = y_avg - x_avg * m
    # print(round(usercredit_level))
    usersum = (1/(userage/20)) + (usermoney/1000000000) + (1/usercredit_level)
    # 여기서 usersum은 3가지 항목을 0-1까지로 표현한 값들을 더한
    return usersum * m + b
    # 유저 값 * 기울기 + y절편을 반환하여 y값을 atm.py에 반환한다.
    plt.plot(x_regressor, m * x_regressor + b)

    plt.show()

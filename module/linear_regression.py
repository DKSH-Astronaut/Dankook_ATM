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


def linear_regression_suggest(full_reg_Table, age, money, credit_level, grade,
                              userage, usermoney, usercredit_level):  # 앞 글자가 소문자인건 매개변수
    print("처리 중")
    Age = 1/(full_reg_Table[age]/20)
    Money = full_reg_Table[money]/1000000000
    Credit_Level = 1/full_reg_Table[credit_level]
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

    usersum = (1/(userage/20)) + (usermoney/1000000000) + (1/usercredit_level)

    return usersum * m + b

    plt.plot(x_regressor, m * x_regressor + b)

    plt.show()

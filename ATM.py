###############################################
# import required module
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time

from module.LRUCache import *
from module.astro_secret import Encoding, Decoding, PWEncoding
import module.linear_regression as lin
###############################################

loginCache = LRUCache(1)
countCache = LRUCache(2)

prev_user = ""
userID = []
userDB = {}

userTable = pd.read_csv('DB/userTable.csv')
full_reg_Table = pd.read_csv('DB/full_reg_table.csv')

loginCount = 0
loginAction = False   # 로그인을 했는지 안했는지 알려주는 변수, 값이 False이면 로그인을 안했다는 뜻
loginedLine = -1  # 로그인한 계정이 몇번째 줄에 있는지 알려주는 변수, 값이 -1이면 로그인 안함

# 회원가입 폼


class SignUpForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astro - SignUp")
        self.resize(300, 500)

        layout = QGridLayout()
        label_name = QLabel("ID")
        self.lineEdit_ID = QLineEdit()
        self.lineEdit_ID.setPlaceholderText("아이디를 입력하세요.")
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_ID, 0, 1)

        label_password = QLabel("Password")
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("패스워드를 입력하세요.")
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        label_password_check = QLabel("Password 확인")
        self.lineEdit_password_check = QLineEdit()
        self.lineEdit_password_check.setPlaceholderText("패스워드를 다시 입력하세요.")
        layout.addWidget(label_password_check, 2, 0)
        layout.addWidget(self.lineEdit_password_check, 2, 1)

        label_age = QLabel("나이")
        self.lineEdit_age = QLineEdit()
        self.lineEdit_age.setPlaceholderText("나이를 입력하세요.")
        layout.addWidget(label_age, 3, 0)
        layout.addWidget(self.lineEdit_age, 3, 1)

        button_signup = QPushButton("회원가입")
        button_signup.clicked.connect(self.signup)
        layout.addWidget(button_signup, 4, 1)
        layout.setRowMinimumHeight(4, 40)

        self.setLayout(layout)

    """
    # 회원가입 시스템

    로직:
        만약 ID 또는 Password를 입력하지 않고 회원가입 버튼을 눌렀다면
            "정보를 모두 입력해주세요"(이)라고 출력
        만약 ID 또는 Password를 입력하고 회원가입 버튼을 눌렀다면
            만약 입력한 ID값이 userTable에 'Name'(이)라는 열에 있다면
                "이미 있는 아이디입니다"(이)라고 출력
            만약 입력한 PW값과 입력한 re_PW값이 같지 않다면
                "두 비밀번호가 일치하지 않습니다."(이)라고 출력
            만약 입력한 ID값이 userTable에 'Name'(이)라는 열에 없다면
                입력한 나이값을 int형으로 형변환 하는 과정에서 문제가 발생하지 않았을 때
                    새로운 계좌번호를 저장할 newAccli를 선언
                    무한 반복
                        0부터 18까지 반복
                            만약 i가 4 또는 9 또는 14일 경우
                                newAccli에 "-" 추가
                            만약 i가 4 또는 9 또는 14가 아닐 경우
                                newAccli에 1부터 9까지의 랜덤 숫자 저장

                입력한 나이값을 int형으로 형변환 하는 과정에서 문제가 발생했을 때
                    "나이를 잘못 입력하셨습니다"(이)라고 출력
                만약 newAccli가 userTable에 'accNum'(이)라는 열에 없다면
                    ID라는 변수에 입력한 ID값을 인코딩
                    이때 발생한 key값과 value값을 각각 keyID, valueID로 저장
                    PW라는 변수에 입력한 PW값을 인코딩
                    이때 발생한 key값과 value값을 각각 keyPW, valuePW로 저장
                    userinformation이라는 변수 판다스 데이터프레임 함수를 이용하여 'Name' 열에는 valueID를, 'PW' 열에는 valuePW를, 'Money' 열에는 0을, 'Age' 열에는 입력한 나이값을, 'accNum' 열에는 newAccli를, 'keyID' 열에는 keyID를, 'keyPW' 열에는 keyPW을 저장
                    무한 반복문 종료
                "회원가입에 성공했습니다."(이)라고 출력
    """

    def signup(self):
        msg = QMessageBox()
        global userTable

        if not self.lineEdit_ID.text() or not self.lineEdit_password.text() or not self.lineEdit_password_check.text() or not self.lineEdit_age.text():
            msg.setText('정보를 모두 입력해주세요')
            msg.exec_()
        else:
            if self.lineEdit_ID.text() in str(userTable['Name']):
                msg.setText('이미 있는 아이디입니다.')
                msg.exec_()
                return
            if self.lineEdit_password.text() != self.lineEdit_password_check.text():
                msg.setText('두 비밀번호가 일치하지 않습니다.')
                msg.exec_()
                return
            elif self.lineEdit_ID.text() not in userID:
                try:
                    lineEdit_age = int(self.lineEdit_age.text())
                except:
                    msg.setText('나이를 잘못 입력하셨습니다')
                    msg.exec_()
                    return
                newAccli = ""
                while True:
                    for i in range(19):
                        if i == 4 or i == 9 or i == 14:
                            newAccli += "-"
                        else:
                            newAccli += str(random.randrange(1, 10))
                    if newAccli not in str(userTable['accNum']):
                        ID = Encoding(self.lineEdit_ID.text())
                        PW = PWEncoding(self.lineEdit_password.text())
                        money = Encoding("0")
                        userinformation = pd.DataFrame(
                            [{'Name': ID[1], 'Pw': PW, 'Money': money[1], 'Age': lineEdit_age, 'accNum': newAccli, 'keyID': ID[0], 'keyMoney': money[0]}])
                        userTable = pd.concat(
                            [userTable, userinformation], ignore_index=True)
                        break
                print(userTable)
                msg.setText('회원가입에 성공했습니다.')
                msg.exec_()

# 로그인 폼


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astro - ATM")
        self.resize(180, 500)

        layout = QGridLayout()
        label_name = QLabel("ID")
        self.lineEdit_ID = QLineEdit()
        self.lineEdit_ID.setPlaceholderText("아이디를 입력해주세요.")
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_ID, 0, 1)

        label_password = QLabel("Password")
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("패스워드를 입력해주세요.")
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        # 조우식 잡다한버튼
        button_login = QPushButton("로그인")
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 2, 0)
        layout.setRowMinimumHeight(2, 40)

        button_register = QPushButton("회원가입")
        button_register.setMaximumWidth(80)
        button_register.clicked.connect(self.register)
        layout.addWidget(button_register, 2, 1)
        layout.setRowMinimumHeight(2, 40)

        button_in = QPushButton("입금")
        button_in.setMaximumWidth(80)
        button_in.clicked.connect(self.inMoney)
        layout.addWidget(button_in, 3, 0)
        layout.setRowMinimumHeight(2, 40)

        button_out = QPushButton("출금")
        button_out.setMaximumWidth(80)
        button_out.clicked.connect(self.outMoney)
        layout.addWidget(button_out, 3, 1)
        layout.setRowMinimumHeight(2, 40)

        button_borrow = QPushButton("대출")
        button_borrow.setMaximumWidth(80)
        button_borrow.clicked.connect(self.loanMoney)
        layout.addWidget(button_borrow, 4, 0)
        layout.setRowMinimumHeight(2, 40)

        button_trans = QPushButton("이체")
        button_trans.setMaximumWidth(80)
        button_trans.clicked.connect(self.trans)
        layout.addWidget(button_trans, 4, 1)
        layout.setRowMinimumHeight(2, 40)

        button_count = QPushButton("잔액조회")
        button_count.setMaximumWidth(80)
        button_count.clicked.connect(self.count)
        layout.addWidget(button_count, 5, 0)
        layout.setRowMinimumHeight(2, 40)

        button_creditrating = QPushButton("신용 조회")
        button_creditrating.setMaximumWidth(80)
        button_creditrating.clicked.connect(self.creditrating)
        layout.addWidget(button_creditrating, 5, 1)
        layout.setRowMinimumHeight(2, 40)

        button_suggest = QPushButton("AD")
        button_suggest.setMaximumHeight(80)
        button_suggest.clicked.connect(self.suggest)
        layout.addWidget(button_suggest, 6, 0)
        layout.setRowMinimumHeight(2, 40)

        self.setLayout(layout)

    """
    # LRU Cache를 이용한 로그인 시스템

    로직:
        만약 잘못된 로그인 횟수가 5회 이상일 때
            1초 딜레이
        만약 ID 또는 Password를 입력하지 않고 로그인 버튼을 눌렀을 때
            "ID 또는 PW를 입력해주세요."(이)라고 출력
        만약 ID 또는 Password를 입력하고 로그인 버튼을 눌렀을 때
            만약 loginCache.nodeMap에 입력한 ID값이라는 캐시에 카운트가 3 이상이라면
                만약 userName과 입력한 ID값이 같다면
                    만약 loginCache.nodeMap에 userName이라는 key에 value값이 입력한 PW값을 해싱한 값과 같다면
                        loginAction을 True로 설정, loginCout를 0으로 설정
                        loginCache에 key는 입력한 ID값, value는 입력한 PW값을 해싱한 값 저장
                        '로그인에 성공했습니다.'(이)라고 출력
                    만약 loginCache.nodeMap에 userName이라는 key에 value값이 입력한 PW값을 해싱한 값과 다르면
                        '로그인에 실패했습니다.'(이)라고 출력
            만약 loginCache.nodeMap에 입력한 ID값이라는 캐시에 카운트가 3 미만이라면
                userTable에 index만큼 반복
                enc_ID(이)라는 변수에 입력한 ID값을 암호화
                enc_PW(이)라는 변수에 입력한 PW값을 해싱
                만약 enc_ID[0](keyID) enc_ID[1](valueID)로 디코딩한 값이 userTable에 'keyID'(이)라는 열, i번째 행 데이터와 'Name'(이)라는 열, i번째 행 데이터로 디코딩한 값과 같다면
                    만약 enc_PW값이 입력한 PW값을 해싱한 값과 같다면
                        loginAction을 True로 설정, loginLine을 i로 설정과 함께 "로그인에 성공했습니다"(이)라고 출력
                    만약 enc_PW값이 입력한 PW값을 해싱한 값과 다르다면
                        '로그인에 실패했습니다.'(이)라고 출력
    """

    def check_password(self):
        msg = QMessageBox()
        start = time.time()
        global prev_user, loginCount, loginAction, loginedLine

        if loginCount >= 5:
            time.sleep(1)

        if not self.lineEdit_ID.text() or not self.lineEdit_password.text():
            loginCount += 1
            msg.setText('ID 또는 PW를 입력해주세요.')
            msg.exec_()
        else:

            # Cache Login
            if loginCache.nodeMap.get(self.lineEdit_ID.text(), [-1, 0])[1] >= 3:
                if prev_user == self.lineEdit_ID.text():
                    if loginCache.nodeMap.get(prev_user, [-1, 0])[0] == PWEncoding(self.lineEdit_password.text()):
                        loginAction = True
                        loginCount = 0
                        loginCache.put(self.lineEdit_ID.text(),
                                       PWEncoding(self.lineEdit_password.text()))
                        print("Cache Login time :", time.time() - start)
                        msg.setText('로그인에 성공했습니다.')
                        msg.exec_()
                    else:
                        loginCount += 1
                        msg.setText('로그인에 실패했습니다.')
                        msg.exec_()

            # Default Login
            else:
                for i in range(len(userTable.index)):
                    enc_ID = Encoding(self.lineEdit_ID.text())
                    enc_PW = PWEncoding(self.lineEdit_password.text())
                    if Decoding(enc_ID[0], enc_ID[1]) == Decoding(userTable['keyID'].iloc[i], userTable['Name'].iloc[i]):
                        if enc_PW == userTable['Pw'].iloc[i]:
                            loginAction = True
                            loginedLine = i
                            prev_user = Decoding(
                                userTable['keyID'].iloc[i], userTable['Name'].iloc[i])
                            loginCache.put(prev_user, userTable['Pw'].iloc[i])
                            loginCount = 0
                            print("Login time :", time.time() - start)
                            msg.setText('로그인에 성공했습니다.')
                            msg.exec_()
                        else:
                            loginCount += 1
                            msg.setText('로그인에 실패했습니다.')
                            msg.exec_()
                            break

    # 회원가입 시스템
    def register(self):
        msg = QMessageBox()
        self.signup = SignUpForm()  # 팝업 회원가입 폼
        self.signup.setGeometry(QRect(100, 100, 400, 200))  # 팝업
        self.signup.show()  # 회원가입 폼 표시

    """
    # 이체 시스템

    로직:
        만약 로그인이 안되어 있으면
            로그인이 필요하다고 출력
        만약 로그인이 되어 있으면
            user는 inputAccNum에 상대방 계좌번호 입력
            만약 inputAccNum이 userTable에 'accNum'(이)라는 열에 있다면
                보낼 금액을 transMoney에 저장
                transMoney가 int형으로 형변환 하는 과정에서 아무 문제도 발생하지 않았을 때
                    만약 transMoney가 user가 가진 금액보다 크다면
                        잔액이 부족하다고 출력
                    만약 transMoney가 이체 가능한 최소 비용보다 작다면
                        보내지 못한다고 출력
                    아무 문제가 없다면
                        userTable에 index만큼 반복
                            만약 inputAccNum이 userTable에 'accNum'(이)라는 열에 i번째 행 데이터와 같다면
                                반복문 탈출
                        userTable에 'Money'라는 열에 loginedLine번째 행 데이터를 userTable에 'Money'라는 열에 loginedLine번째 행 데이터 - transMoney로 저장
                        userTable에 'Money'라는 열에 i번째 행 데이터를 userTable에 'Money'라는 열에 i번째 행 데이터 + transMoney로 저장
                        DB폴더에 trans.log 파일을 만들고 이 파일을 file(이)라는 변수로 저장
                            이체할 때마다 돈을 보낸 사람 -> 돈을 받은 사람 : 금액 형식으로 저장
                            ex) 6852-2588-5453-1555->9532-6723-8939-7668:1233
                        "inputAccNum번호로 transMoney원 이체 완료했습니다."라고 출력
                transMoney가 int형으로 형변환 하는 과정에서 valueError가 발생했을 때
                    "정확한 금액을 입력해주세요"(이)라고 출력
            만약 inputAccNum이 userTable에 'accNum'(이)라는 열에 없다면
                "해당 계좌는 존재하지 않습니다."(이)라고 출력
    """

    def trans(self):
        msg = QMessageBox()
        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            inputAccNum, dialog = QInputDialog.getText(
                self, 'Input Dialog', '보낼 사람의 계좌를 입력해주세요. :')

            if inputAccNum in str(userTable['accNum']):
                transMoney, dialog1 = QInputDialog.getText(
                    self, 'Input Dialog', '얼마를 보내시겠습니까? :')
                try:
                    transMoney = int(transMoney)
                except:
                    msg.setText("이체할 금액을 정확히 입력해 주세요")
                    msg.exec_()
                    return
                if transMoney > int(Decoding(userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])):
                    msg.setText("잔액이 부족합니다.")
                    msg.exec_()
                elif transMoney < 100:
                    msg.setText("이체 가능한 최소 비용은 100원입니다.")
                    msg.exec_()
                else:
                    for i in range(len(userTable.index)):
                        if inputAccNum == userTable['accNum'].iloc[i]:
                            break
                    userTable['Money'].iloc[loginedLine] = Encoding(str(int(Decoding(
                        userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) - transMoney))[1]
                    userTable['keyMoney'].iloc[loginedLine] = Encoding(str(int(Decoding(
                        userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) - transMoney))[0]
                    userTable['Money'].iloc[i] = Encoding(str(int(Decoding(
                        userTable['keyMoney'].iloc[i], userTable['Money'].iloc[i])) + transMoney))[1]
                    userTable['keyMoney'].iloc[i] = Encoding(str(int(Decoding(
                        userTable['keyMoney'].iloc[i], userTable['Money'].iloc[i])) + transMoney))[0]
                    with open("DB/trans.log", "a", encoding="UTF8") as file:
                        file.write(
                            f"{userTable['accNum'].iloc[loginedLine]}->{inputAccNum}:{Encoding(str(transMoney))}\n")
                    msg.setText(
                        f"{inputAccNum}번호로 {transMoney}원 이체 완료했습니다.")
                    msg.exec_()
            else:
                msg.setText("해당 계좌는 존재하지 않습니다.")
                msg.exec_()

    """
    # LRU Cache를 이용한 잔액조회 시스템

    로직:
        만약 로그인이 안되어 있으면
            로그인이 필요하다고 출력
        만약 로그인이 되어 있으면
            userName을 userTable에 'Name'(이)라는 열, loginedLine번째 행 데이터를 저장
            userMoney를 userTable에 'Money'(이)라는 열, loginedLine번째 행 데이터를 저장
            만약 countCache.nodeMap에 userName이라는 key에 카운트가 3 이상이라면
                countCache에 저장되어 있던 userName이라는 key에 value값을 출력
            만약 countCache.nodeMap에 userName이라는 key에 카운트가 3 이상이 아니라면
                userMoney 출력
                countCache에 key가 userName이고, value가 userMoney인 값을 저장
    """

    def count(self):
        msg = QMessageBox()
        start = time.time()
        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            userName = userTable['Name'].iloc[loginedLine]
            countCache.put(userName, Decoding(
                userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine]))
            if countCache.nodeMap.get(userName, [-1, 0])[1] >= 3:
                msg.setText(
                    f"{str(countCache.get(userName))}원 있습니다.")
                print("Cache Count time :", time.time() - start)
                msg.exec_()
                # 대부분 0.0 ~ 0.001 정도
            else:
                time.sleep(1)
                msg.setText(
                    f"{Decoding(userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])}원 있습니다.")
                print("Count time :", time.time() - start)
                msg.exec_()
                # 대부분 1.0 ~ 1.0009 정도

    """
    # 출금 시스템
    # 주석 추가 부탁
    """

    def outMoney(self):
        global userTable, loginedLine
        msg = QMessageBox()

        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            try:
                outMoney, dialog = QInputDialog.getText(
                    self, 'Input Dialog', '출금할 금액 :')
                if int(outMoney) > int(Decoding(userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])):
                    msg.setText("잔액이 부족합니다.")
                    msg.exec_()
                else:
                    # 왜 오류?
                    enco = Encoding(str(int(Decoding(
                        userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) - int(outMoney)))
                    userTable['Money'].iloc[loginedLine] = enco[1]
                    userTable['keyMoney'].iloc[loginedLine] = enco[0]
                    msg.setText(f"{outMoney}원을 입금 완료했습니다.")
                    msg.exec_()
            except ValueError:
                msg.setText("정확한 금액을 입력해주세요")
                msg.exec_()

    """
    # 입금 시스템

    로직:
        만약 로그인이 안되어 있으면
            로그인이 필요하다고 출력
        만약 로그인이 되어 있으면
            inMoney에 입금할 금액 저장
            inMoney를 int형으로 형변환 하는 과정에서 아무 문제도 발생하지 않았을 때
                userTable에 'Money'열, loginedLine번째 행 데이터에서 inMoney값을 더함
                "입금 완료"(이)라고 출력
            inMoney를 int형으로 형변환 하는 과정에서 valueError가 발생했을 때
                "정확한 금액을 입력해주세요"(이)라고 출력
    """

    def inMoney(self):
        global userTable, loginedLine
        msg = QMessageBox()

        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            try:
                inMoney, dialog = QInputDialog.getText(
                    self, 'Input Dialog', '입금할 금액 :')
                enco = Encoding(str(int(Decoding(
                    userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) + int(inMoney)))
                userTable['Money'].iloc[loginedLine] = enco[1]
                userTable['keyMoney'].iloc[loginedLine] = enco[0]
                msg.setText(inMoney + "원을 입금 완료했습니다.")
                msg.exec_()
            except ValueError:
                msg.setText("정확한 금액을 입력해주세요")
                msg.exec_()

    """
    # 대출 시스템
    # 주석 추가 부탁
    """

    def loanMoney(self):
        msg = QMessageBox()

        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            try:
                loan, dialog = QInputDialog.getText(
                    self, 'Input Dialog', '대출 금액 :')
                #userTable['Money'].iloc[loginedLine] += int(loan)
                userTable['Money'].iloc[loginedLine] = Encoding(str(int(Decoding(
                    userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) + int(loan)))[1]
                userTable['keyMoney'].iloc[loginedLine] = Encoding(str(int(Decoding(
                    userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])) + int(loan)))[0]
                msg.setText(loan+"원 대출완료")
                msg.exec_()
                msg.setText("당신의 금리: %f" % userTable['Rate'].iloc[loginedLine])
                msg.exec_()
            except ValueError:
                msg.setText("정확한 금액을 입력해주세요")
                msg.exec_()

    """
    # 선형 회귀를 이용한 신용 등급 조회 시스템
    # 주석 추가 부탁
    """

    def creditrating(self):
        msg = QMessageBox()

        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            try:
                if lin.linear_regression(userTable, 'Age', 'Money', userTable['Age'].iloc[loginedLine], userTable['Money'].iloc[loginedLine]) == 1:
                    userTable['Rate'].iloc[loginedLine] = 2.8
                    msg.setText("당신의 신용등급은 높습니다.")
                    msg.exec_()
                else:
                    userTable['Rate'].iloc[loginedLine] = 4.8
                    msg.setText("당신의 신용등급은 낮습니다.")
                    msg.exec_()
            except ValueError:
                pass

    def suggest(self):
        msg = QMessageBox()

        if loginAction == False:
            msg.setText("로그인이 필요합니다.")
            msg.exec_()
        else:
            usersum = lin.linear_regression_suggest(full_reg_Table, 'Age', 'Money', 'Credit_level', 'Grade',
                                                    userTable['Age'].iloc[loginedLine],
                                                    int(Decoding(
                                                        userTable['keyMoney'].iloc[loginedLine], userTable['Money'].iloc[loginedLine])),
                                                    userTable['Rate'].iloc[loginedLine])
            if round(usersum) <= 1:
                msg.setText("햇살론")
            elif 1 < round(usersum) <= 2:
                msg.setText("금리 4% 인생핀다론")
            elif 2 < round(usersum) <= 3:
                msg.setText("우리자유적금")
            elif 3 < round(usersum) <= 4:
                msg.setText("우리적금")
            elif 4 < round(usersum) <= 5:
                msg.setText("우리큐브")
            elif 5 < round(usersum):
                msg.setText("두루두루정기예금")
            msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())

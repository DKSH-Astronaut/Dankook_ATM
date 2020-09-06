def to10(a):  # 2진수를 10진수로 바꾸는 함수
    ans = 0  # 10진수 저장 변수
    i = 1  # 현재 idx의 가중치
    while a:
        ans += a % 10 * i  # 첫째 자리 수를 10진수로 바꿔서 ans에 더해줌
        a = a // 10  # 더해준 앞자리를 제거
        i *= 2  # 가중치 업데이트
    return ans


def To2(a):  # 10진수를 2진수로 바꾸는 함수
    res = []
    while a:
        # 마지막 자리부터 2진수로 값을 구함, 따라서 1의 자리수 부터 2, 4의 자리로 거꾸로 나오게 됨
        res.append(a % 2)
        a = a // 2  # 앞자리 저장 후 2로 나눔
    ans = ''
    for i in range(len(res) - 1, -1, -1):
        ans += str(res[i])  # res reverse하여 ans에 저장

    return ans


def base64(k):  # 코드를 문자로 변경
    A = 0  # base64 'A'의 코드
    a = 26  # base64 'a'의 코드
    num = 52  # base64 '0'의 코드
    plus = 62  # base64 '+'의 코드

    temp = to10(k)  # 들어온 2진 숫자를 10진수로 변환하여 temp 에 저장
    if temp >= A and temp < a:  # 만약 temp에 해당하는 값이 대문자라면 (base64 기준)
        return chr(ord('A') + temp)  # 아스키 코드 값을 이용하여 문자 return
    elif temp >= a and temp < num:  # 만약 temp에 해당하는 값이 소문자라면 (base64기준)
        # 아스키 코드 기준 소문자이므로, 'a'에서 temp - a(temp는 26+a 임 따라서 -a를 한 후 a에 추가)를 더해줌
        return chr(ord('a') + temp - a)
    elif temp >= num and temp < plus:  # 만약 temp에 해당하는 값이 숫자라면 (base64기준)
        return str(temp - num)  # temp에서 num에 해당하는 값을 빼주어 그 숫자를 문자로 변환하여 return
    elif temp == plus:  # temp에 해당하는 값이 '+' 라면
        return '+'  # + return
    return '/'  # 위 경우에 해당하지 않으므로 남은 '/' 리턴


def toBaseCode(k):  # base64 문자를 10진수로 변환
    a = 26  # base64의 'a' 코드

    temp = ord(k)  # 문자를 숫자 형태로 변환 (문자의 아스키 코드값)
    if temp >= ord('A') and temp <= ord('Z'):  # 대문자라면
        return temp - ord('A')  # base64에 해당하는 대문자 코드로 변환
    elif temp >= ord('a') and temp <= ord('z'):  # 소문자라면
        # base64에 해당하는 소문자 코드로 변환(이 때 소문자는 a 부터 시작이므로 a를 더해줌)
        return temp - ord('a') + a
    elif temp >= ord('0') and temp <= ord('9'):  # 숫자라면
        return temp + 4  # 아스키코드에서 4를 더해주면 숫자가 나옴
    elif temp == ord('+'):  # '+'라면
        return 52  # base 64에서 +에 해당하는 값은 52임
    return 63  # 모든 경우가 아니면 '/'임, 따라서 해당하는 값은 63


def EncodeBase64(a):  # encode main 함수
    to2 = ''  # 문자를 아스키 코드로 변환
    plusE = 3 - len(a) % 3  # 맞지 않는 문자의 개수? ex) 3 -> 4 인데 비는 자리 수
    if plusE == 3:  # plusE가 3이면 자리가 정확히 맞는다는 의미, 따라서 0으로 값 수정
        plusE = 0
    for i in a:  # 각 문자별로 2진수로 변환하여 연결
        temp = To2(ord(i))
        to2 += (8 - len(temp)) * '0'  # 8자리이므로 빈 자리는 0으로 채워줌
        to2 += temp  # 채워준값 추가

    if len(to2) % 6 != 0:  # 계산하기 위에 뒤에 빈 자리를 0으로 채워줌
        to2 += (6 - len(to2) % 6) * '0'

    res = ''  # 최종 변경 값
    size = len(to2) // 6  # 2진수값의 길이(숫자개수) / 6 (6개가 문자 하나 이므로)
    for i in range(0, size):
        temp = to2[i*6:i*6+6]  # 6개를 끊어 temp에 임시저장
        res += base64(int(temp))  # temp를 int로 바꾸어 base64함수를 통해 문자로 변경

    res += plusE * '='  # 맞지 않는 문자의 개수만큼 '=' 채워줌

    return res


def DecodeBase64(a):  # decode main 함수
    to2 = ''  # base64 2진수화 저장변수
    for i in a:
        if i == '=':  # 나중에 추가한 문자이므로 처리하지 않음
            break
        temp = To2(toBaseCode(i))  # toBaseCode에서 10진수로 변환하고, 그 값을 다시 2진수로 변환
        to2 += (6 - len(temp)) * '0'  # 6자리가 않되면 계산을 위에 앞을 0으로 채워줌
        to2 += temp

    res = ''  # 최종 출력 변수
    size = len(to2) // 8  # 8개씩 끊어 저장할 것이므로 (길이 / 8) 만큼 돌 것임
    for i in range(0, size):
        temp = to2[i*8:i*8+8]  # 8개씩 끊어 temp에 임시저장
        res += chr(to10(int(temp)))  # 10진수로 바꾼 후, chr() 함수를 통해 아스키코드화

    return res


def uniqueEncode(sender, recipient, key, value):
    tmp = '{"sender":'+sender+'"recipient":' + \
        recipient+'"key":' + key+'"value":'+value+'}'
    res = EncodeBase64(tmp).split('=')
    return res[0]


# 암호화 : EncodeBase64(argument)
# 복호화 : DecodeBase64(argument)
# created by sheenjiwon
#####################################

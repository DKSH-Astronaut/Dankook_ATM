"""

인코딩 : Encoding(value) -> value is String
디코딩 : Decoding(key, value) -> key, value is String

"""

import module.astro_base64 as base64
from random import choice
from string import ascii_uppercase
import hashlib


def Decoding(key, value):  # 복호화할 문자열과 키, 리턴값은 decoding 값
    value = base64.DecodeBase64(value)  # 일단 a문자열을 복호화한다.

    if key[0] == "-":  # 이전에 값을 줄였다는 의미
        value += key[1:]  # 따라서 원래 문자열로 복원
    else:  # 이전에 값을 늘렸다는 의미
        aLen = 18 - len(key)  # 뒤에 있는 길이만큼 분리
        value = value[0:aLen]

    value = base64.DecodeBase64(value)  # 원래 문자열로 복호화

    return value


def Encoding(value):  # 암호화할 문자열, 리턴값으로 encoding 한 문자열과 salt(key) 값 반환 예정
    value = base64.EncodeBase64(value)  # 일단 base64로 encoding한다

    value = value.split(sep="=")[0]  # 맨 뒤의 '='을 제거한다.

    # 변경 후 24자리를 만들기 위해 18자리를 할당한다. (한 번 더 base64로 인코딩 할 예정)
    plusLen = 18 - len(value)
    if plusLen >= 0:  # 24자리를 맞추기 위해 문자열을 추가해야 한다는 의미
        # key에 빈 자리를 랜덤 문자열로 채워준다.
        key = ''.join(choice(ascii_uppercase) for i in range(plusLen))
        value += key  # 암호화 전 18자리를 맞춰준다. 암호화 완료 시 24자리 예정
    else:  # 24자리를 맞추기 위해 문자열을 삭제해야 한다는 의미
        key = '-' + value[18:]  # 삭제할 부분
        value = value[0:18]  # 실제로 부분 삭제

    value = base64.EncodeBase64(value)  # 다시 base64 인코딩
    # print("key = " + key) # key(salt)
    # print("암호 = " + a) # 최종 문자열

    return key, value


def PWEncoding(value):
    value = value.encode('utf-8')
    sha = hashlib.new('sha256')
    sha.update(value)
    return sha.hexdigest()


def uniqueEncode(sender, recipient, key, value):
    tmp = '{"sender":'+sender+'"recipient":' + \
        recipient+'"key":' + key+'"value":'+value+'}'
    res = base64.EncodeBase64(tmp).split('=')
    return res[0]

# 참고링크 : http://bitly.kr/jkQeVklmmsU
# created by sheenjiwon
# assist by Song Kitae

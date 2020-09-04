import jwt

encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
decoded = jwt.decode(encoded, 'secret', algorithms='HS256')

print(encoded)
print(decoded)

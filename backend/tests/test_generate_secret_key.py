import secrets
import string

# 定义字符集：包含大写字母、小写字母、数字
charset = string.ascii_letters + string.digits


# 生成一个指定长度的密钥，确保包含大写字母、小写字母和数字
def generate_secure_key(length=32):
    # 确保至少包含一个大写字母、一个小写字母和一个数字
    while True:
        key = ''.join(secrets.choice(charset) for _ in range(length))
        if (any(c.islower() for c in key) and
                any(c.isupper() for c in key) and
                any(c.isdigit() for c in key)):
            return key


def test_generate_secure_key():
    # 生成一个32字符长度的安全密钥
    secure_key = generate_secure_key(64)
    print()
    print(secure_key)


def test_generate_password():
    secure_key = generate_secure_key(32)
    print()
    print(secure_key)

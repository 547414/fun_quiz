from cryptography.fernet import Fernet


def test_encryption_and_decryption():
    # 生成密钥（只需生成一次，后续存储在安全位置）
    key = Fernet.generate_key()
    print()
    print(f"密钥: {key}")
    cipher_suite = Fernet(key)

    # 加密
    token = "your_access_token"
    encrypted_token = cipher_suite.encrypt(token.encode('utf-8'))  # 加密并转换为字节
    encrypted_token_str = encrypted_token.decode('utf-8')  # 将加密后的字节转为字符串，方便存储
    print(f"加密后的 Token: {encrypted_token_str}")

    # 解密
    encrypted_token_bytes = encrypted_token_str.encode('utf-8')  # 将字符串转回字节以解密
    decrypted_token = cipher_suite.decrypt(encrypted_token_bytes)  # 解密得到字节
    decrypted_token_str = decrypted_token.decode('utf-8')  # 转为字符串
    print(f"解密后的 Token: {decrypted_token_str}")

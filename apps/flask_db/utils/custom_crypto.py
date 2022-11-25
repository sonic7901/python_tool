import sys
import base64
# pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def aes_enc(input_str, input_key):
    # 0. init setting
    temp_result = ""
    # 1. input check
    try:
        input_str = str(input_str)
        input_key = str(input_key)
        if len(input_key) < 16:
            input_key = input_key.zfill(16)
        elif len(input_key) > 256:
            input_key = input_key[:256]
    # 2. encode
        cipher = AES.new(input_key.encode('utf-8'), AES.MODE_ECB)
        pad_pkcs7 = pad(input_str.encode('utf-8'), AES.block_size, style='pkcs7')
        encrypt_aes = cipher.encrypt(pad_pkcs7)
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        temp_result = encrypted_text.replace("\n", "")
    except Exception as ex:
        print(ex)
    return temp_result


def aes_dec(input_str, input_key):
    # 0. init setting
    temp_result = ""
    # 1. input check
    try:
        input_str = str(input_str)
        input_key = str(input_key)
        if len(input_key) < 16:
            input_key = input_key.zfill(16)
        elif len(input_key) > 256:
            input_key = input_key[:256]
    # 2. decode
        res = base64.decodebytes(input_str.encode('utf8'))
        cipher = AES.new(input_key.encode('utf-8'), AES.MODE_ECB)
        msg = cipher.decrypt(res).decode("utf8")
        temp_result = msg[0:-ord(msg[-1])]
    except Exception as ex:
        print(ex)
    return temp_result


# unit test
if __name__ == "__main__":
    test_key = "1235"
    test_json = "test"
    test_e = aes_enc(test_json, test_key)
    print("enc:" + test_e)
    test_d = aes_dec(test_e, test_key)
    print("dev:" + test_d)
    if test_d == test_json:
        print("unit test(custom_crypto.py): pass")
        sys.exit(0)
    else:
        print("unit test(custom_crypto.py): fail")
        sys.exit(1)

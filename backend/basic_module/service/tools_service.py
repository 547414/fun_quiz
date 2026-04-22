import json
import secrets
import string
import time
from typing import Dict

import requests


class ToolsService:
    def __init__(
            self,
    ):
        self.__charset = string.ascii_letters + string.digits

    # 生成一个指定长度的密钥，确保包含大写字母、小写字母和数字
    def generate_secure_key(self, length=32):
        while True:
            key = ''.join(secrets.choice(self.__charset) for _ in range(length))
            if (any(c.islower() for c in key) and
                    any(c.isupper() for c in key) and
                    any(c.isdigit() for c in key)):
                return key

    @staticmethod
    def get_department_name(access_token, department_id):
        department_url = f"https://qyapi.weixin.qq.com/cgi-bin/department/get?access_token={access_token}&id={department_id}"
        response = requests.get(department_url).json()
        if response['errcode'] == 0:
            if response['department']:
                return response['department']['name']
            else:
                return None
        else:
            raise Exception(f"Error getting department info: {response['errmsg']}")

    @staticmethod
    def load_access_token(token_file):
        try:
            with open(token_file, 'r') as f:
                data = json.load(f)
                if time.time() < data['expires_at']:
                    return data['access_token']
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            pass
        return None

    @staticmethod
    def save_access_token(token_file, access_token, expires_in):
        expires_at = time.time() + expires_in
        data = {
            'access_token': access_token,
            'expires_at': expires_at
        }
        with open(token_file, 'w') as f:
            json.dump(data, f)

    def get_wecom_access_token(self, token_file, config: Dict):
        access_token = self.load_access_token(token_file)
        if access_token:
            return access_token
        corp_id = config.get('corp_id')
        agent_secret = config.get('agent_secret')
        token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={agent_secret}"
        response = requests.get(token_url).json()

        if response['errcode'] == 0:
            access_token = response['access_token']
            expires_in = response['expires_in']
            self.save_access_token(token_file, access_token, expires_in)
            return access_token
        else:
            raise Exception(f"Error getting access token: {response['errmsg']}")

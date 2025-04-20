from dataclasses import dataclass
from config import user_info  # 导入用户信息模块

@dataclass
class User:
    username: str = user_info.USER_INFO['username']
    password: str = user_info.USER_INFO['password']
    last_4: str = user_info.USER_INFO['last_4']  # 身份证后4位
    
from pathlib import Path

class Settings:
    # 浏览器配置
    BROWSER_CONFIG = {
        'headless': False,
        'timeout': 30,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'executable_path': 'msedgedriver.exe'
    }

    # 12306网站URL
    URLS = {
        'login': 'https://kyfw.12306.cn/otn/resources/login.html',
        'query': 'https://kyfw.12306.cn/otn/leftTicket/init',
        'index': 'https://www.12306.cn/index/index.html',
        'cookie': Path('./data/12306_cookies.pkl' ),
        'last_login': Path('./data/last_login.txt')  # 最后登录时间文件
    }

    # 定义页面元素定位器字典
    LOCATORS = {
        # 用户名输入框定位器
        'username': ['//input[@id="J-userName"]'],
        # 密码输入框定位器
        'password': ['//input[@id="J-password"]'],
        # 登录按钮定位器
        'login': ['//a[@id="J-login"]'],
        # 身份证后四位输入框定位器
        'last_4': ['//input[@id="id_card"]'],
        # 验证码输入框定位器
        'verify_code': ['//input[@id="code"]'],
        # 获取验证码按钮定位器
        'verify_code_submit': ['//a[@id="verification_code"]'],
        # 确定按钮定位器
        'sureClick': ['//a[@id="sureClick"]'],
        'index' : ['//*[@id="J-index"]/a']
    }

    # 查询参数默认值
    DEFAULT_QUERY_PARAMS = {
        'train_types': ['G', 'D'],  # 默认高铁和动车
        'seat_types': ['二等座', '一等座']
    }

    PATH = './data/' # 数据存储路径

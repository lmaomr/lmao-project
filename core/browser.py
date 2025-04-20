from selenium.webdriver.edge.options import Options  # Edge浏览器配置选项
from selenium import webdriver  # 主库，用于浏览器自动化
from util.logger import setup_logger  # 导入日志配置模块
import random  # 随机数模块

class BrowserManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
        # 创建浏览器配置对象
        self._configure_browser_options()
        self._initialized = True
        self.driver = webdriver.Edge(options=self.options)
        # 删除自动化特征
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        })
        self.logger = self.get_logger("browser")
        self.logger.debug("浏览器调试端口已开启")
        
    def get_logger(self, name):
        """获取日志记录器"""
        return setup_logger(name)

    def get_web(self, url):
        """获取网页内容"""
        self.driver.get(url)
        self.logger.info(f'正在访问网站{url}')

    # 浏览器配置方法
    def _configure_browser_options(self):
        """配置浏览器选项以优化自动化体验"""    
        self.options = Options()   
        # 设置浏览器日志级别为只显示致命错误(3)
        self.options.add_argument('--log-level=3')
        
        # 禁用浏览器日志输出
        self.options.add_argument('--disable-logging')
        
        # 忽略SSL证书错误
        self.options.add_argument('--ignore-certificate-errors')
        
        # 忽略SSL错误
        self.options.add_argument('--ignore-ssl-errors')
        
        # 禁用同源策略
        self.options.add_argument('--disable-web-security')
        
        # 允许不安全的本地主机连接
        self.options.add_argument('--allow-insecure-localhost')
        
        # 禁用浏览器扩展
        self.options.add_argument('--disable-extensions')

        # Edge新版无头模式
        # self.options.add_argument('--headless=new')  

        # # 禁用GPU加速
        # self.options.add_argument('--disable-gpu')
        
        # # 以无沙盒模式运行
        # self.options.add_argument('--no-sandbox')
        
        # 排除"启用自动化"开关
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        # 禁用自动化扩展
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # 设置接受不安全证书的能力
        self.options.set_capability('acceptInsecureCerts', True)
        
        # 设置自动接受弹窗的行为
        self.options.set_capability('unhandledPromptBehavior', 'accept')

        # 修改浏览器指纹（关键！）
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 随机用户代理
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # 添加常见请求头
        self.options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        self.options.add_argument("--accept-language=zh-CN,zh;q=0.9,en;q=0.8")
        self.options.add_argument("--accept-encoding=gzip, deflate, br")
        self.options.add_argument("--referer=https://www.12306.cn/")
        self.options.add_argument("--sec-ch-ua=\"Google Chrome\";v=\"120\", \"Chromium\";v=\"120\", \"Not?A_Brand\";v=\"24\"")
        self.options.add_argument("--sec-ch-ua-mobile=?0")
        self.options.add_argument("--sec-ch-ua-platform=\"Windows\"")
        self.options.add_argument("--sec-fetch-dest=document")
        self.options.add_argument("--sec-fetch-mode=navigate")
        self.options.add_argument("--sec-fetch-site=same-origin")
        self.options.add_argument("--sec-fetch-user=?1")
        self.options.add_argument("--upgrade-insecure-requests=1")
        
        # 禁用自动化特征
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

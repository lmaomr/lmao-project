from core.browser import BrowserManager  # 导入浏览器管理模块
from config.settings import Settings as settings  # 导入配置模块
from util import helper  # 导入辅助函数模块
from model.user import User as user # 导入用户模型
from util.logger import setup_logger  # 导入日志配置模块

from selenium.webdriver.support.ui import WebDriverWait  # 显式等待
from selenium.webdriver.support import expected_conditions as EC  # 等待条件
from selenium.common.exceptions import TimeoutException  # 超时异常
from selenium.webdriver.common.keys import Keys  # 键盘按键常量
import time  # 时间模块

class Login:
    def __init__(self):
        self.browser = BrowserManager()  # 获取浏览器单例
        self.driver = self.browser.driver  # 获取浏览器驱动
        self.logger = setup_logger("login")  # 设置登录日志记录器
        self.logger.info("开始登录初始化...")

    # 登录方法
    def login(self):
        """执行完整的登录流程"""
        # 先尝试复用已有会话
        self.logger.info("先尝试复用已有会话")
        if helper.try_reuse_session(self.browser):
            return True
        try:
            # 打印登录开始信息
            self.logger.info("正在重新登录...")
            
            # 导航到登录页面
            self.browser.get_web(settings.URLS['login'])
            
            # 等待页面完全加载完成
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        
            # 查找用户名输入框元素
            username_input = helper._find_element(self.driver,settings.LOCATORS['username'], "用户名输入框")
            
            # 模拟人工输入用户名
            helper.slow_type(username_input, user.username)
            
            # 查找密码输入框元素
            password_input = helper._find_element(self.driver,settings.LOCATORS['password'], "密码输入框")
            
            
            # 模拟人工输入密码
            helper.slow_type(password_input, user.password)
            
            # 查找登录按钮元素（非必须）
            login_button = helper._find_element(self.driver, 'J-login', 'id')  # 查找登录按钮
            
            # 如果找到登录按钮则点击
            if login_button:
                login_button.click()
            else:
                # 否则通过回车键提交表单
                password_input.send_keys(Keys.RETURN)

            # 等待2秒让页面处理
            time.sleep(1)
            
            # 查找身份证后四位输入框
            last_4_input = helper._find_element(self.driver,settings.LOCATORS['last_4'], "身份证后四位输入框")
            
            # 输入身份证后4位（确保只取最后4位）
            helper.slow_type(last_4_input, user.last_4)

            # 查找获取验证码按钮
            verify_code_button = helper._find_element(self.driver,settings.LOCATORS['verify_code_submit'], "验证码按钮")
            
            # 如果找到验证码按钮则点击
            if verify_code_button:
                verify_code_button.click()
            else:
                # 否则通过回车键触发
                last_4_input.send_keys(Keys.RETURN)

            # 提示用户输入收到的短信验证码
            verify_code = input("请输入收到的短信验证码: ")

            # 查找验证码输入框
            verify_code_input = helper._find_element(self.driver,settings.LOCATORS['verify_code'], "验证码输入框")
            
            # 输入验证码（确保只取最后6位）   
            helper.slow_type(verify_code_input, verify_code[-6:])

            # 查找确定按钮（非必须）
            sure_button = helper._find_element(self.driver,settings.LOCATORS['sureClick'], "确定按钮")
            
            # 如果找到确定按钮则点击
            if sure_button:
                sure_button.click()
            else:
                # 否则通过回车键提交
                password_input.send_keys(Keys.RETURN)
            self.logger.info("正在登录，请稍等...")
            # 等待直到URL中不再包含login/signin，最多30秒
            # 先等待页面基本加载完成
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # 然后检查是否已跳转出登录页或首页元素已加载
            WebDriverWait(self.driver, 30).until(
                lambda d: ("login" not in d.current_url.lower() and 
                         "signin" not in d.current_url.lower()) or
                helper._find_element(d, settings.LOCATORS['index'], "首页元素", required=False) is not None  # 首页元素
            )

            # 打印登录成功信息
            self.logger.info("登录成功！")
            
            helper.save_cookies(self.driver)  # 保存Cookies
            return True
            
        except Exception as e:
            # 登录失败时保存错误截图
            self.driver.save_screenshot(settings.PATH + "login_error.png")
            
            # 打印错误信息
            if isinstance(e, TimeoutException):
                self.logger.error("登录超时，请检查网络连接或手动登录")
                return False
            self.logger.error(f"登录失败: {str(e)}")
            return False

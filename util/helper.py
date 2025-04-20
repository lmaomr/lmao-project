import time
import pickle
from datetime import datetime, timedelta
from pathlib import Path

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By  # 元素定位方式
from selenium.webdriver.support.ui import WebDriverWait  # 显式等待
from selenium.webdriver.support import expected_conditions as EC  # 等待条件

from config.settings import Settings as settings  # 导入配置模块
from core.browser import BrowserManager  # 导入浏览器管理模块

logger = BrowserManager().get_logger("helper")  # 设置辅助函数日志记录器

def slow_type(element: WebElement, text: str, delay: float = 0.1) -> None:
    """模拟人工输入"""
    logger.info(f"正在输入文本: {text}")
    element.clear()  # 清空输入框
    # 模拟逐个字符输入
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# 元素查找辅助方法
def _find_element(driver, locators, element_name, required=True) -> WebElement:
    try:
        if element_name == 'id':
            # 等待元素出现，最多5秒
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, locators))
            )
            return driver.find_element(By.ID, locators)
        elif element_name == 'class':
            # 等待元素出现，最多5秒
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, locators))
            )
            return driver.find_element(By.CLASS_NAME, locators)
        elif element_name == 'link_text':
            # 等待元素出现，最多5秒
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, locators))
            )
            return driver.find_element(By.LINK_TEXT, locators)
        elif element_name == 'css_selector':
            # 等待元素出现，最多5秒
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locators))
            )
            return driver.find_element(By.CSS_SELECTOR, locators)
        else:
            # 等待元素出现，最多5秒
            for locator in locators:
                try:
                    # 等待元素出现，最多5秒
                    locator = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    return locator
                except:
                    continue  
            raise Exception(f"无法定位{element_name}")
    except:
        if required:
            raise Exception(f"无法定位{element_name}")
        return None
    
def try_reuse_session(browser) -> bool:
        """尝试复用已有会话"""
        if not load_cookies(browser):
            return False
            
        # 访问首页验证是否仍登录
        browser.get_web(settings.URLS['index'])
        time.sleep(2)
        
        try:
            # 检查登录状态元素
            WebDriverWait(browser.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "我的12306"))
            )
            logger.info("会话有效，复用成功")
            return True
        except:
            clear_session()
            logger.info("会话无效，尝试重新登录")
            return False
        
def load_cookies(browser) -> bool:
    """从文件加载Cookies"""
    if not settings.URLS['cookie'].exists():
        return False
    
    # 检查Cookies是否过期
    if settings.URLS['last_login'].exists():
        try:
            with open(settings.URLS['last_login'], 'r') as f:
                last_login = datetime.fromisoformat(f.read().strip())
                if datetime.now() - last_login > timedelta(hours=4):
                    clear_session()
                    return False
            if f.closed: logger.info("文件已自动关闭")
            else:
                logger.info("文件未关闭,准备手动关闭")
                f.close()
        except (ValueError, TypeError):
            clear_session()
            return False
    
    # 加载Cookies
    with open(settings.URLS['cookie'], 'rb') as f:
        cookies = pickle.load(f)
        # 先访问主域名以确保domain匹配
        browser.get_web(settings.URLS['index'])
        browser.driver.delete_all_cookies()  # 清除现有cookies
        
        for cookie in cookies:
            try:
                # 删除可能导致问题的属性
                for attr in ['expiry', 'domain', 'sameSite']:
                    if attr in cookie:
                        del cookie[attr]
                browser.driver.add_cookie(cookie)
            except Exception as e:
                logger.warning(f"添加cookie失败: {str(e)}")
                continue
    if f.closed: logger.info("文件已自动关闭")   
    else:
        logger.info("文件未关闭,准备手动关闭")
        f.close()  
    return len(browser.driver.get_cookies()) > 0  # 检查是否成功添加了cookie

def save_cookies(driver, file_path: Path = settings.URLS['cookie']) -> None:
    """保存Cookies到文件"""
    with open(file_path, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
    if f.closed: logger.info("文件已自动关闭")
    else:
        logger.info("文件未关闭,准备手动关闭")
        f.close()
    logger.info(f"Cookies已保存到 {file_path}")

    # 记录最后登录时间
    with open(settings.URLS['last_login'], 'w') as f:
        f.write(datetime.now().isoformat())
    if f.closed: logger.info("文件已自动关闭")
    else:
        logger.info("文件未关闭,准备手动关闭")
        f.close()

def clear_session() -> None:
    """清除会话数据"""
    for file_path in [settings.URLS['cookie'], settings.URLS['last_login']]:
        if file_path.exists():
            file_path.unlink()
    logger.info("会话数据已清除")

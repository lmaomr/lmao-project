import os
from dataclasses import dataclass

@dataclass
class BrowserConfig:
    headless: bool = False
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    timeout: int = 30
    log_level: int = 3  # Only fatal errors

@dataclass
class UserConfig:
    username: str
    password: str
    id_last_four: str

@dataclass
class PathConfig:
    cookie_file: str = "12306_cookies.pkl"
    last_login_file: str = "last_login.txt"
    screenshot_dir: str = "screenshots"

def ensure_dirs():
    """确保必要的目录存在"""
    os.makedirs(PathConfig.screenshot_dir, exist_ok=True)
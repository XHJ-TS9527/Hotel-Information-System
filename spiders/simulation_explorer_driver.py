#导入包
from selenium import webdriver #模拟浏览器
from tkinter import messagebox
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import exception_classes as excp_cls

class consult_webdriver():
    def __init__(self,load_image=False,headless=True):
        #模拟浏览器设置并打开无GUI界面的浏览器
        chrome_option=webdriver.ChromeOptions()
        if not load_image:
            preference={'profile.managed_default_content_settings.images': 2}
            chrome_option.add_experimental_option('prefs',preference)
        if headless:
            chrome_option.add_argument('headless')
            chrome_option.add_argument("window-size=1920,1080")
            chrome_option.add_argument("start-maximized")
            chrome_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
        chrome_option.binary_location=gm.get_global('chrome_path')
        chrome_option.add_argument('disable-infobars')
        chrome_option.add_argument('disable-gpu') #谷歌文档说用于防止bug
        chrome_option.add_experimental_option('excludeSwitches',['enable-automation']) #伪装webdriver
        try: #打开浏览器
            self.driver=webdriver.Chrome(executable_path=gm.get_global('driver_path'),options=chrome_option)
        except:
            messagebox.showerror('内部错误','查询器不能打开,请检查:\n 1.您安装了正确版本的Chrome浏览器\n 2.您安装了对应版本的chrome webdriver\n 3.您正确设置了Chrome浏览器及其webdriver路径')
            raise excp_cls.webdriver_error
        
    #访问浏览器
    def visit_driver(self):
        return self.driver

    #关闭浏览器
    def close_driver(self):
        self.driver.quit()
    
    #关闭浏览器
    def __del__(self):
        self.driver.quit()      
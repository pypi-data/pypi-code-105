import os
import sys

class SeleniumCommonSetting(object):
    """ Selenium-webdriver常用的ChromeOptions配置

    对常用的Selenium-webdriver的ChromeOptions进行配置，默认必填项为webdriver。
    
    Attributes:
        options: 根据设置的参数所返回的chrome_options。

    Usage:
        SetChromeOptions(webdriver).options: 返回最基础的设置项。
        SetChromeOptions(webdriver,localdata_path = 'default').options: 返回使用默认本地文件地址的设置项。
        SetChromeOptions(webdriverm, extension_dir = <extension_dir>).options: 返回使用crx插件的设置项。
    """
    options = None
    def __init__(self,webdriver,
                localdata_path: str='default',
                extension_dir: str=None,
                headless: bool=False,
                pic: bool=True,
                js: bool=True,
                css: bool=True,
                chromium_path: str=None):
        """ 常用的chrome_options配置

        Args:
            localdata_path: 浏览器本地文件的地址，默认为default，导入本地文件的默认地址。
            extension_dir: 存放浏览器插件的【文件夹地址】，默认为None，插件必须为打包好的crx格式，【不能】与无窗口模式同时使用。
            headless: 无窗口模式，默认为False。
            pic: 无图模式，默认为False。
            js: 加载Javascript，默认为False。
            css: 加载CSS，默认为False。
            chromnium_path: chromnium的chrome.exe地址，默认为None
        
        Raises:
            ExtError: 如果打开了无窗口模式，extension_path不为None则报错，因为Chrome不支持无窗口模式下使用插件。
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')  #禁用GPU渲染
        chrome_options.add_argument('--no-sandbox')   
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-position=120,120')   #设置窗口启动位置（左上角坐标）
        chrome_options.add_argument('window-size=800,600')   #设置窗口尺寸
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])   #规避爬虫检测
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])    #禁用USB挂起报错
        # headless
        if headless == True:
            chrome_options.add_argument('--headless')
        # localdata
        if localdata_path != None:
            if localdata_path == 'default':
                if chromium_path == None:
                    localdata_path = os.environ['USERPROFILE'] + '\\AppData\\Local\\Google\\Chrome\\User Data'
                else:
                    localdata_path = os.environ['USERPROFILE'] + '\\AppData\\Local\\Chromium\\User Data'
            chrome_options.add_argument('--user-data-dir=' + localdata_path)
        # extension
        if extension_dir != None:
            if headless == True:
                sys.exit('ExtError: Chrome不支持无窗口模式下使用插件，'
                '请将headless删除or设置为False，或将extension_path删除or设置为None')
            else:
                for e in os.listdir(extension_dir):
                    path = (extension_dir + '\\' + e).replace('\\','/')
                    chrome_options.add_extension(path)
        # preferences
        prefs = {'profile.default_content_setting_values':{
            'images': 1,
            'javascript': 1,
            'permissions.default.stylesheet':1,
            }
            }
        chrome_options.add_experimental_option('prefs',prefs)
        # pic
        if pic == False:
            prefs['profile.default_content_setting_values']['images'] = 2
            chrome_options.add_experimental_option('prefs',prefs)
        else:
            prefs['profile.default_content_setting_values']['images'] = 1
            chrome_options.add_experimental_option('prefs',prefs)
        # js
        if js == False:
            prefs['profile.default_content_setting_values']['javascript'] = 2
            chrome_options.add_experimental_option('prefs',prefs)
        else:
            prefs['profile.default_content_setting_values']['javascript'] = 1
            chrome_options.add_experimental_option('prefs',prefs)
        # css
        if css == False:
            prefs['profile.default_content_setting_values']['permissions.default.stylesheet'] = 2
            chrome_options.add_experimental_option('prefs',prefs)
        else:
            prefs['profile.default_content_setting_values']['permissions.default.stylesheet'] = 1
            chrome_options.add_experimental_option('prefs',prefs)
        # chromnium
        if chromium_path != None:
            chrome_options.binary_location = chromium_path
        self.options = chrome_options
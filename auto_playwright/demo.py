import time
import json
# 使用playwright同步API
from playwright.sync_api import sync_playwright


# 自动登录，保存Cookies到文件。
def saveCookies():
    with sync_playwright() as p:
        # 显示浏览器，每步操作等待50毫秒
        browser = p.firefox.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        #读取登录账户信息
        userf = open('login_account.txt', 'r').readlines()
        #对账号进行枚举
        for count, user in enumerate(userf):
            user = user.split(',')
            # 用户名及密码
            usrname = user[0]
            passwd = user[1]
            # 登录操作,打开登录页面，输入账号
            page.goto('你的网址')
            page.locator('//*[@id="email"]').fill(usrname)
            page.locator('//*[@id="passwd"]').fill(passwd)
            page.locator('//*[@id="login"]').click()
            #等待，用户需要输入验证码等手工处理
            str = 'y'
            while str == 'y':
                str = input('等待中，是否继续等待？y/n。请输入：')  # 控制休眠时间
            # time.sleep(2)  # 等待页面跳转后，再获取cookies
            # 获取网站cookies
            cookies = context.cookies()
            print(page.title())
            #两个账号，循环登录，保存cookies到不同文件
            if count == 0:
                f = open('cookies163.txt', 'w')
            else:
                f = open('cookiesqq.txt', 'w')
            json.dump(cookies, f)
            print('已获取cookies')
            f.close()
            time.sleep(3)
        browser.close()


# 加载已保存的cookies
def loadCookies(cookief):
    # 从保存文件中提取cookies,进行免登陆
    cookiefile = open(cookief, 'r')
    cookie_list = json.load(cookiefile)  # json读取cookies
    cookiefile.close()
    return cookie_list


# 使用cookies自动登录，然后进行签到
def signIn():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        cookiefiles = ['cookies163.txt', 'cookiesqq.txt']
        for cookiefile in cookiefiles:
            context.add_cookies(loadCookies(cookiefile))  # 加载已保存的cookies，免登陆
            page = context.new_page()
            page.goto('你的签到网页', timeout=50000)
            time.sleep(1)  # 等待页面加载
            # 点击签到按钮
            button = page.locator('//html/body/div/div/section[2]/div[2]/div[3]/div/div[2]/p[2]/button')
            button.click()
            #等待，用户需要输入验证码等手工处理
            str = 'y'
            while str == 'y':
                str = input('等待中，是否继续等待？y/n。请输入：')  # 控制休眠时间
            page.close()
        browser.close()


saveCookies()
signIn()


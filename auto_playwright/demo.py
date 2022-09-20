import time
import json
# ʹ��playwrightͬ��API
from playwright.sync_api import sync_playwright


# �Զ���¼������Cookies���ļ���
def saveCookies():
    with sync_playwright() as p:
        # ��ʾ�������ÿ�������ȴ�50����
        browser = p.firefox.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        #��ȡ��¼�˻���Ϣ
        userf = open('login_account.txt', 'r').readlines()
        #���˺Ž���ö��
        for count, user in enumerate(userf):
            user = user.split(',')
            # �û���������
            usrname = user[0]
            passwd = user[1]
            # ��¼����,�򿪵�¼ҳ�棬�����˺�
            page.goto('�����ַ')
            page.locator('//*[@id="email"]').fill(usrname)
            page.locator('//*[@id="passwd"]').fill(passwd)
            page.locator('//*[@id="login"]').click()
            #�ȴ����û���Ҫ������֤����ֹ�����
            str = 'y'
            while str == 'y':
                str = input('�ȴ��У��Ƿ�����ȴ���y/n�������룺')  # ��������ʱ��
            # time.sleep(2)  # �ȴ�ҳ����ת���ٻ�ȡcookies
            # ��ȡ��վcookies
            cookies = context.cookies()
            print(page.title())
            #�����˺ţ�ѭ����¼������cookies����ͬ�ļ�
            if count == 0:
                f = open('cookies163.txt', 'w')
            else:
                f = open('cookiesqq.txt', 'w')
            json.dump(cookies, f)
            print('�ѻ�ȡcookies')
            f.close()
            time.sleep(3)
        browser.close()


# �����ѱ����cookies
def loadCookies(cookief):
    # �ӱ����ļ�����ȡcookies,�������½
    cookiefile = open(cookief, 'r')
    cookie_list = json.load(cookiefile)  # json��ȡcookies
    cookiefile.close()
    return cookie_list


# ʹ��cookies�Զ���¼��Ȼ�����ǩ��
def signIn():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        cookiefiles = ['cookies163.txt', 'cookiesqq.txt']
        for cookiefile in cookiefiles:
            context.add_cookies(loadCookies(cookiefile))  # �����ѱ����cookies�����½
            page = context.new_page()
            page.goto('���ǩ����ҳ', timeout=50000)
            time.sleep(1)  # �ȴ�ҳ�����
            # ���ǩ����ť
            button = page.locator('//html/body/div/div/section[2]/div[2]/div[3]/div/div[2]/p[2]/button')
            button.click()
            #�ȴ����û���Ҫ������֤����ֹ�����
            str = 'y'
            while str == 'y':
                str = input('�ȴ��У��Ƿ�����ȴ���y/n�������룺')  # ��������ʱ��
            page.close()
        browser.close()


saveCookies()
signIn()


import hashlib
import re
import requests

# 账号密码
username = ""
password = ""
# Server酱推送SCKEY
SCKEY = ""

headers = {
    "Accept": "",
    "Referer": "https://www.93hsy.com/plugin.php?id=k_misign:sign",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.93hsy.com",
    "DNT": "1"
}
session = requests.session()


def ServerChanPush():
    if len(SCKEY) > 0:
        serverchan_url = "http://sc.ftqq.com/" + SCKEY + ".send"
        # 推送标题
        text = '93hsy.com'
        # 推送内容
        desp = '已签到'
        requests.get(url=serverchan_url, params={'text': text,
                                                 'desp': desp})


# 签到
def checkin():
    # 获取签到页面的formhash
    r = session.get(url='https://www.93hsy.com/plugin.php?id=k_misign:sign').text
    formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', r).group(1).encode('ascii')

    # 执行签到
    url = "https://www.93hsy.com/plugin.php"
    params = {'id': "k_misign:sign",
              'operation': 'qiandao',
              'formhash': formhash,
              'format': 'empty',
              'inajax': 1,
              'ajaxtarget': 'JD_sign'}
    checkin = session.get(url=url, params=params, headers=headers)
    if checkin.status_code == 200:
        print("签到成功")
        ServerChanPush()


# 登录
def loginin(url, username, password):
    post_data = {
        "fastloginfield": 'username',
        "username": username,
        "password": password,
        "quickforward": 'yes',
        "handlekey": 'ls'
    }

    # 执行登录
    a = session.post(url, params={'mod': 'logging',
                                  'action': 'login',
                                  'loginsubmit': 'yes',
                                  'infloat': 'yes',
                                  'lssubmit': 'yes',
                                  'inajax': 1}, data=post_data, headers=headers)
    # 执行签到
    checkin()


# 加密密码
def passwordHex(password):
    return hashlib.md5(password.encode("utf-8")).hexdigest()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://www.93hsy.com/member.php"
    loginin(url, username, passwordHex(password))

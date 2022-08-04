# -*- coding: utf8 -*-
import requests
import hashlib
import json
import time
import random
requests.packages.urllib3.disable_warnings
def md5(code):
    res=hashlib.md5()
    res.update(code.encode("utf8"))
    return res.hexdigest()

def get_information(mobile,password):
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G9500 Build/PPR1.180610.011)"
    }
    url="https://sports.lifesense.com/sessions_service/login?version=4.5&systemType=2"
    datas = {
        "appType":6,
        "clientId":'8e844e28db7245eb81823132464835eb',
        "loginName":str(mobile),
        "password":md5(str(password)),
        "roleType":0
        }
    response =requests.post(url,headers=header,data=json.dumps(datas))
    return response.text

def update_step(step,information):
    step =int(step)
    url="https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?version=4.5&systemType=2"
    accessToken=json.loads(information)["data"]["accessToken"]
    userId=json.loads(information)["data"]["userId"]
    #print(json.loads(information))
    #print(accessToken)
    #print(userId)
    #获取当前时间和日期
    timeStamp=time.time()
    localTime = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    print(strTime)
    measureTime=strTime+","+str(int(timeStamp))

    header = {
    'Cookie': 'accessToken='+accessToken,
    'Content-Type': 'application/json; charset=utf-8',
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G9500 Build/PPR1.180610.011)"
    }
    sport_datas = {
        "list": [
            {
                 "DataSource":2,
                #"active":0,
                 "calories":str(int(step/4)),
                #"dataSource":4,
                 "deviceId":"M_NULL",
                 "distance":str(int(step/3)),
                 "exerciseTime":0,
                 "isUpload":0,
                 "measurementTime":measureTime,
                #"priority":0,
                 "step": str(step),
                 "type":2,
                 "updated":str(int(time.time()*1000)),
                 "userId":str(userId)
                }]
                }
    result=requests.post(url,headers=header,data=json.dumps(sport_datas))
    # print(result.text)
    return result.text

def bind(information):
    
    accessToken = json.loads(information)["data"]["accessToken"]
    userId = json.loads(information)["data"]["userId"]
    header = {
        'Cookie': 'accessToken=' + accessToken,
        'Content-Type': 'application/json; charset=utf-8',
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G9500 Build/PPR1.180610.011)"
    }
    
def server_send(msg):
    if sckey == '':
        return
    server_url = "https://sc.ftqq.com/" + str(sckey) + ".send"
    data = {
            'text': msg,
            'desp': msg
        }
    requests.post(server_url, data=data)

def kt_send(msg):
    if ktkey == '':
        return
    kt_url = 'https://push.xuthus.cc/send/'+str(ktkey)
    data = ('步数刷取完成，请查看详细信息~\n'+str(msg)).encode("utf-8")
    requests.post(kt_url, data=data)

def execute_walk(phone,password,step):
    information=get_information(phone,password)
    bind(information)
    update_result=update_step(step,information)
    result=json.loads(update_result)["msg"]
    if result == '成功':
        msg = "刷新步数成功！此次刷取" + str(step) + "步。"
        print(msg)
        server_send(msg)
        kt_send(msg)
    else:
        msg = "刷新步数失败！请查看云函数日志。"
        print(msg)
        server_send(msg)
        kt_send(msg)

def main():
    if phone and password and step != '':
        execute_walk(phone, password, step)
    else:
        print("参数不全,请指定参数。或者在调用中直接指定参数")

# -- 配置 --
# ------------------------------
phone = '你的账号'  # 登陆账号
password = '你的密码'  # 密码
step = random.randint(19000,20000)  # 随机19000-20000步数
sckey = ''  # server酱key(可空)
ktkey = ''  # 酷推key(可空)
# ------------------------------

def main_handler(event, context):
    return main()

if __name__ == '__main__':
    main()

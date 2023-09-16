import pandas as pd
from uiautomation import WindowControl, MenuControl
import pyautogui
import random
import requests
import json

API_KEY = " "
SECRET_KEY = " "

# 绑定微信主界面
wx = WindowControl(Name='微信')
wx.SwitchToThisWindow()

# 寻找会话控件绑定
hw = wx.ListControl(Name='会话')

# 通过pd读取数据
df = pd.read_csv('积分统计.csv', encoding='utf-8')
print(df)

x, y = pyautogui.size()  # 您需要根据实际情况获取坐标位置
pyautogui.click(x / 2, y / 2, button='left')


def chat():
    pyautogui.click(x / 2, y / 2, button='left')
    # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token()
    payload_dict = {
        "messages": [
            {
                "role": "user",
                "content": "你是谁"
            },
            {
                "role": "assistant",
                "content": "您好，我是你的小猫,名字是reclin。我每次说完话都会加上喵~"
            },
            {
                "role": "user",
                "content": "再次确认你是谁!"
            },
            {
                "role": "assistant",
                "content": "您好!我是你的小猫,名字是reclin!我每次说完话都会加上喵~"
            }
        ]
    }
    chat_init = payload_dict
    while True:
        while not we.Exists(0):
            pass
        if we.Name:
            we.Click(simulateMove=False)
            # 读取最后一条消息
            question = wx.ListControl(Name='消息').GetChildren()[-1].Name
            print(question)
            new_item = {
                "role": "user",
                "content": question
            }
            if 'seclin' not in question:
                if question == "没你事儿了一边玩去吧":
                    wx.SendKeys('牛子硬了, 告辞')
                    return
                elif question == "初始化对话模式":
                    payload_dict = chat_init
                    wx.SendKeys('初始化已完成')
                    wx.SendKeys('{Enter}', waitTime=0)
                    pyautogui.click(x / 2, y / 2, button='left')
                    continue
                else:
                    pyautogui.click(x / 2, y / 2, button='left')
                    continue
            payload_dict["messages"].append(new_item)
            payload = json.dumps(payload_dict)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            a = json.loads(response.text)
            newResult = a['result']
            print(newResult)
            wx.SendKeys(newResult, waitTime=1)
            new_item = {
                "role": "assistant",
                "content": newResult
            }
            payload_dict["messages"].append(new_item)
            wx.SendKeys('{Enter}', waitTime=0)
            pyautogui.click(x / 2, y / 2, button='left')


# def get_access_token():
#     """
#     使用 AK，SK 生成鉴权签名（Access Token）
#     :return: access_token，或是None(如果错误)
#     """
#     url = "https://aip.baidubce.com/oauth/2.0/token"
#     params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
#     return str(requests.post(url, params=params).json().get("access_token"))


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[API Key]&client_secret=[Secret Key]"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# 随机取出励志语
def fighting():
    fight = pd.read_csv('励志语.csv', encoding='utf-8')
    random_number = random.randint(0, 29)
    wx.SendKeys('{Shift}{Enter}', waitTime=0)
    wx.SendKeys(fight.iloc[random_number, 1], waitTime=0)
    wx.SendKeys('{Shift}{Enter}', waitTime=0)
    wx.SendKeys(fight.iloc[random_number, 2], waitTime=0)


# 查询积分榜
def ShowScore():
    dff = pd.read_csv('积分统计.csv', encoding='utf-8')
    df_sorted = dff.sort_values('积分', ascending=False)
    df_sorted.to_csv('积分统计.csv', index=False)
    dff = pd.read_csv('积分统计.csv', encoding='utf-8')
    for j in range(3):
        wx.SendKeys(dff.iloc[j, 2], waitTime=0)
        wx.SendKeys(':   ', waitTime=0)
        wx.SendKeys(str(int(dff.iloc[j, 3])), waitTime=0)
        wx.SendKeys('{Shift}{Enter}', waitTime=0)


while True:
    we = hw.TextControl(searchDepth=3)
    while not we.Exists(0):
        pass
    if we.Name:
        we.Click(simulateMove=False)
        # 读取最后一条消息
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        print(last_msg)
        for index, row in df.iterrows():
            if row['关键词'] in last_msg:
                if row['关键词'] == df.iloc[4, 1]:
                    ShowScore()
                elif row['关键词'] == df.iloc[3, 1]:
                    for i in range(3):
                        df.loc[i, '积分'] = 0
                    df.to_csv('积分统计.csv', index=False)
                    wx.SendKeys('积分已归零', waitTime=0)
                    wx.SendKeys('{Shift}{Enter}', waitTime=0)
                    ShowScore()
                elif row['关键词'] == df.iloc[5, 1]:
                    wx.SendKeys(row['回复内容'], waitTime=0)
                    wx.SendKeys(row['回复内容'], waitTime=0)
                    wx.SendKeys('{Enter}', waitTime=0)
                    chat()
                else:
                    try:
                        day = int(last_msg[4:])
                    except ValueError:
                        continue
                    if day != 0:
                        wx.SendKeys(row['回复内容'], waitTime=0)
                        wx.SendKeys('{Shift}{Enter}', waitTime=0)
                        wx.SendKeys('打卡成功, 积分加1, 目前的积分榜单是', waitTime=0)
                        wx.SendKeys('{Shift}{Enter}', waitTime=0)
                        df.loc[row['序号'] - 1, '积分'] += 1
                        df.to_csv('积分统计.csv', index=False)
                        ShowScore()
                    elif day == 0:
                        wx.SendKeys(row['回复内容'], waitTime=0)
                        wx.SendKeys('{Shift}{Enter}', waitTime=0)
                        wx.SendKeys('打卡成功, 积分减4, 你目前的积分是', waitTime=0)
                        df.loc[row['序号'] - 1, '积分'] -= 4
                        df.to_csv('积分统计.csv', index=False)
                        ShowScore()
                fighting()
                wx.SendKeys('{Enter}', waitTime=0)
        # 模拟鼠标左键点击空白处
        pyautogui.click(x / 2, y / 2, button='left')

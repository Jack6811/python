from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
import base64
import hashlib
import requests
import json
import urllib
import sqlite3
import time
import re

def md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

def getSecret():
    pass

def aes_decrypt(encrypt: str, key: str) -> str:
    encrypt = base64.b64decode(encrypt)
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypt)
    return unpad(decrypted, AES.block_size).decode('utf-8')

def aes_encrypt(source: str, key: str):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_data = pad(source.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode()

def getdata(articleId,sign,key):
    getDataKey = '{"articleId":"'+ articleId + '"}'
    encryptData = aes_encrypt(getDataKey,key)
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'identity': 'h5',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'encryptUserId': '0',
        'Accept': 'application/json, text/plain, */*',
        'note_version': '5.7.24',
        'sign': sign,
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://zwzt-h5.zuowenzhitiao.com/web/longPaper?articleId=' + articleId,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    url = "https://zwzt-h5.zuowenzhitiao.com/longApi/content/article/content/detail?encryptData=" + urllib.parse.quote(encryptData)
    response = requests.get(url,headers=headers)#,verify=False
    if response.status_code == 200:
        data = response.json()
        if data["status"] != 200:
            print("请求失败，状态码：", data["status"], data["msg"])
            return data["status"]
        else:
            date = data.get("data")
            return date
    else:
        print("请求失败，状态码：", response.status_code)

def get_sign(articleId,key):
    getDataKey = '{"articleId":"'+ articleId + '"}'
    salt = 'kOe&ac%YD5grq4Tk'
    encryptData = aes_encrypt(getDataKey,key)
    sign = md5(encryptData + salt)
    return sign

def get_articleId(id):
    articleId = base64.b64encode(id.encode())
    articleId = base64.b64encode(articleId)
    return articleId.decode()

def save_database(data):
    data = json.loads(data)
    # 检查数据库中是否已存在相同ID的数据
    cursor.execute("SELECT * FROM longArticle WHERE id=?", (data['id'],))
    result = cursor.fetchone()
    if not result:
        title = data['title']
        publictime = time.localtime(int(data['date'] / 1000))
        StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", publictime)
        cursor.execute("INSERT INTO longArticle (id, articleSecondaryCategory, title, subtitle, articlePrimaryCategory, time, content) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['id'], str(data['articleSecondaryCategory']), title , data['subtitle'], str(data['articlePrimaryCategory']),StyleTime,data['content']))
        conn.commit()

def getfile(id):
    id = str(id)
    # 检查数据库中是否已存在相同ID的数据
    cursor.execute("SELECT * FROM longArticle WHERE id=?", (id,))
    result = cursor.fetchone()
    if not result:
        key = getSecret() #"108fb118037661484f3ea04042eb5e08"
        articleId = get_articleId(id) #"TVRrMk5UYw"
        sign = get_sign(articleId,key)
        print(sign)
        data = str(getdata(articleId,sign,key))
        #Encode = '1d46/4ALoXes2G4XPcjiydhOKEeyBjlj6N9lyIe7ipk='
        if data != "400": 
            decode = aes_decrypt(data,key)
            articaldata = json.loads(decode)
            #print(articaldata)
            if str(articaldata["articlePrimaryCategory"]) == "[]":
                print("广告：" + id + articaldata['title'])
                save_database(decode)
            else:
                save_database(decode)
                title = articaldata['title']
                content = articaldata['content']
                print("文章： " + id + " " + articaldata['title'])
        time.sleep(2)
    else:
        print ("文件已存在")

if __name__ == '__main__':
    conn = sqlite3.connect('zwzt.db',check_same_thread=False)
    cursor = conn.cursor()
    for i in range(20600,20900):#下一文件id：7754
        print("下一文件id：" + str(i))
        getfile(i)
    cursor.close()
    conn.close()

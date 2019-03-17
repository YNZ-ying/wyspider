import json
import pymysql
import requests

headers ={
    "Host": "music.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

def get_conents(page):
    url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_573384240?limir=20&offset='+ str(page)
    response = requests.get(url,headers=headers)
    response = json.loads(response.text)
    items = response['comments']
    for item in items:
        username = str(item['user']['nickname'])
        userid = str(item['user']['userId'])
        user_message = get_user(userid)
        usergender = user_message['gender']
        usercity = user_message['city']
        comment = str(item['content'].strip())
        open_sql(username,comment)

def get_user(id):
    data = {}
    url = 'https://music.163.com/api/v1/user/detail/' + id
    response = requests.get(url=url,headers=headers)
    response = json.loads(response.text)
    if response['code'] == 200:
        data['gender'] = response['profile']['gender']
        data['city'] = response['profile']['city']
    else:
        data['gender'] = '无'
        data['city'] = "无"
    return data


def open_sql(username,comment):
    dbparts = {
        'host':'127.0.0.1',
        'port':3306,
        'user':'root',
        'database':'manhua',
        'password':'root',
        'charset':'utf8mb4',
    }

    db = pymysql.connect(**dbparts)
    cur = db.cursor()
    sql_insert = """insert into ryez (id,username,comment) values (null ,%s,%s)"""
    cur.execute(sql_insert,(username,comment))
    db.commit()

def main():
    # get_conents()
    for i in range(0,25000,20):
        print('----------------第'+str(i//20+1)+ '页-----------')
        get_conents(i)

if  __name__ == '__main__':
    main()
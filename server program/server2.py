import http.server
import socketserver
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from flask import Flask, request
import sqlite3

import threading

app = Flask(__name__)
# 定义 SQLite 数据库名称
DB_NAME = 'serverdatabase.db'

# 创建数据库连接
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Numbers (
             id INTEGER PRIMARY KEY,
             number INTEGER,
             PCip_address TEXT,
             PHip_address TEXT

             )''')
c.execute('''CREATE TABLE IF NOT EXISTS serverrecords (
                    id INTEGER PRIMARY KEY,
                    source TEXT,
                    time TEXT,
                    mp4base64 TEXT,
                    PCip_address  TEXT
                )''')

# 创建数据表

"""
# 创建数据表
c.execute('''CREATE TABLE IF NOT EXISTS UserMatching (
             id INTEGER PRIMARY KEY,
             number INTEGER
             PCip_address TEXT
             PHip_address TEXT

             )''')"""

server_db_conn = sqlite3.connect('serverdatabase.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT id FROM serverrecords")
records = client_db_cursor.fetchall()
"""
# 遍历记录并更新到服务器数据库
aabc="100.86.59.179"
idkk = 1
for record in records:

    # 使用 UPDATE 语句更新 serverrecords 表中的记录
    client_db_cursor.execute("UPDATE serverrecords SET PCip_address = ? WHERE id = ?", (aabc, idkk))
    idkk += 1

# 提交更改并关闭客户端数据库连接
server_db_conn.commit()
"""

"""修改列
conn = sqlite3.connect('serverdatabase.db')
c = conn.cursor()

# 执行 SQL 语句
#c.execute('''ALTER TABLE serverrecords ADD COLUMN PCip_address TEXT;''')
#c.execute('''ALTER TABLE records DROP COLUMN recordbase64;''')
c.execute('''ALTER TABLE serverrecords DROP COLUMN recordbase64;''')

# 提交更改并关闭连接
conn.commit()
conn.close()
"""

# 生成一個4位數的隨機數
import random


def random_number():
    return random.randint(1000, 9999)


import sqlite3
import random


def register_number(PCip_address):
    conn = sqlite3.connect('serverdatabase.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM Numbers WHERE PCip_address = ?", (PCip_address,))
    result2 = c.fetchone()
    if result2[0] == 0:
        while True:
            # Generate a random number
            number = random_number()
            # Check if the random number is not already in the database
            c.execute("SELECT COUNT(*) FROM Numbers WHERE number = ?", (number,))
            result = c.fetchone()
            if result[0] == 0:
                # Insert the number into the database table
                c.execute("INSERT INTO Numbers (number, PCip_address) VALUES (?, ?)", (number, PCip_address))
                conn.commit()
                conn.close()
                break
        return number
    else:
        c.execute("SELECT number FROM Numbers WHERE PCip_address = ?", (PCip_address,))
        number = c.fetchall()
        conn.close()
        print("12222222222222222222222222222222")
        print(str(number[0][0]))
        return str(number[0][0])


@app.route('/get_message1', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/others/copy_paste', methods=['GET'])
def conc():
    msg = request.args.get('hhhhh')
    return msg + msg + msg + msg + msg + msg


@app.route('/user/api/login', methods=['GET'])
def loginn():
    u = request.args.get('user')
    p = request.args.get('passwd')
    print(f"登录！   {u}    {p}")
    return f"success!         u={u}          pwd={p}"


@app.route('/fall_report', methods=['GET'])
def fall():
    t = request.args.get('time')
    who = request.args.get('who')
    print(f"调用了fall()      时间{t}      跌倒的人是{who}")
    return "ok"


@app.route('/paring_code', methods=['POST'])
def store_number():
    # 从请求中获取数字
    number = request.form.get('number')

    # 将数字插入数据库表中
    c.execute("INSERT INTO Numbers (number) VALUES (?)", (number,))
    conn.commit()

    return 'Number stored successfully!'


import base64


@app.route('/user/api/getdatabase', methods=['GET'])
def get_database():
    # 连接到服务器数据库
    server_db_conn = sqlite3.connect('serverdatabase.db')
    server_db_cursor = server_db_conn.cursor()

    # 查询数据库
    server_db_cursor.execute("SELECT id, source, time FROM serverrecords")

    # 获取查询结果
    rows = server_db_cursor.fetchall()
    print("查询数据库getdatabase1")

    # 关闭服务器数据库连接
    # server_db_conn.close()

    # 将查询结果转换为 JSON 格式并返回
    records = []
    for row in rows:
        records.append(list(row))
    return json.dumps(records)


from flask import request


@app.route('/user/api/getdatabaseV2', methods=['GET'])
def get_databaseV2():
    print("查询数据库getdatabaseV2++1234")

    # 获取参数
    id_param = request.args.get('id')
    ip_param = request.args.get('ip')
    print(id_param)

    # 连接到服务器数据库
    server_db_conn = sqlite3.connect('serverdatabase.db')
    server_db_cursor = server_db_conn.cursor()
    print("连接到服务器数据库")

    # 构建查询语句
    if id_param:

        # 查询数据库
        server_db_cursor.execute("SELECT PCip_address FROM Numbers where PHip_address = ?", (ip_param,))
        result = server_db_cursor.fetchall()
        query = "SELECT id, source, time FROM serverrecords WHERE id = ? and PCip_address = ?"
        server_db_cursor.execute(query, (id_param, result[0][0]))
        print("id_param:")
    else:
        query = "SELECT id, source, time FROM serverrecords"
        server_db_cursor.execute(query)
        print("else:")
    # 获取查询结果
    rows = server_db_cursor.fetchall()
    print("查询数据库getdatabase")

    # 关闭服务器数据库连接
    # server_db_conn.close()

    # 将查询结果转换为 JSON 格式并返回

    return json.dumps(rows)


@app.route('/user/api/getroll', methods=['GET'])
def getrollnumber():  # 棄用
    ip_param = request.args.get('ip')
    server_db_conn = sqlite3.connect('serverdatabase.db')
    server_db_cursor = server_db_conn.cursor()

    # 查询数据库
    server_db_cursor.execute("SELECT id FROM serverrecords where PCip_address =? ", (ip_param,))

    # 获取查询结果
    rows = server_db_cursor.fetchall()
    aa = len(rows)
    print("getrollnumber")
    return str(aa)


def get_array_dimension(arr):
    if isinstance(arr, list):
        return 1 + get_array_dimension(arr[0])
    else:
        return 0


@app.route('/user/api/login1', methods=['POST'])
def login1():  # 電腦向服務器發送數據，附上電腦ip
    print("login1():")

    # 解析 JSON 数据
    data = request.json
    # ip=request.args.get('ip')
    # data2=request.args.get('data')
    # data2 = request.args.get('data')
    # data2 = data['data']
    # ip = data['ip']
    data2 = json.loads(data.get('data'))
    ip = data.get('ip')  # 从 JSON 数据中获取 'ip'

    print("data = request.json")
    # data = json.loads(request.json)
    print("json.loads(request.json)")
    # type(data2)
    # print((data2[0][0]))
    # print(type(data2[0][0]))
    # print(ip[0])
    # print(data2[0][0])
    PCip_address = '特定IP';

    server_db_conn = sqlite3.connect('serverdatabase.db')
    client_db_cursor = server_db_conn.cursor()
    print("client_db_cursor = server_db_conn.cursor()")
    client_db_cursor.execute("DELETE FROM serverrecords WHERE PCip_address = ?", (ip,))
    print("client_db_cursor.execute")

    # print(get_array_dimension(data2))
    # print(data2[0])
    # print(data2[0][1])
    # print("data2[0][1]")
    for record in data2:
        # aaa=record[0][0]
        # print(record['id'])
        # print(aaa)
        # print(record)
        # print('1')
        client_db_cursor.execute('''INSERT INTO serverrecords (id, source, time, mp4base64, PCip_address)
                                   VALUES (?, ?, ?, ?, ?)''', (record[0], record[1], record[2], record[3], ip))

    print("record in data:")
    server_db_conn.commit()

    server_db_conn.close()

    print("收到")

    # print(data)

    return "success!"


@app.route('/user/api/login12', methods=['GET'])
def login12():  # 電腦向服務器發送數據，附上電腦ip
    print("login1():")

    # 解析 JSON 数据
    data = request.json
    # ip=request.args.get('ip')
    # data2=request.args.get('data')
    # data2 = request.args.get('data')
    # data2 = data['data']
    # ip = data['ip']

    print("data = request.json")
    # data = json.loads(request.json)
    print("json.loads(request.json)")
    # type(data2)
    # print((data2[0][0]))
    # print(type(data2[0][0]))
    # print(ip[0])
    # print(data2[0][0])
    PCip_address = '特定IP';

    server_db_conn = sqlite3.connect('serverdatabase.db')
    client_db_cursor = server_db_conn.cursor()
    # main.get_local_ip()
    ip = "123"
    # print(get_array_dimension(data2))
    # print(data2[0])
    # print(data2[0][1])
    # print("data2[0][1]")
    # for record in data:
    # aaa=record[0][0]
    # print(record['id'])
    # print(aaa)
    # print(record)
    # print('1')
    # client_db_cursor.execute('''INSERT INTO serverrecords (id, source, time, mp4base64, PCip_address)
    # VALUES (?, ?, ?, ?, ?)''', (123, record['source'], record['time'], record['mp4base64']),ip)

    print("record in data:")
    server_db_conn.commit()

    server_db_conn.close()

    print("收到")

    # print(data)

    return "success!"


@app.route('/user/api/submitcode', methods=['POST'])
def submitcode():  # 手機向服務器發送code，，檢查配對，附上手機ip
    if request.method == 'POST':
        # 从请求中获取字符串数据
        # code = request.data.decode('utf-8')
        code = request.values["code"]
        print(code)
        param2 = request.values["param2"]
        print(param2)
        server_db_conn = sqlite3.connect('serverdatabase.db')
        server_db_cursor = server_db_conn.cursor()

        # 查询数据库
        server_db_cursor.execute("SELECT number FROM Numbers")

        server_db_cursor.execute("SELECT id FROM Numbers WHERE number = ?", (code,))
        result = server_db_cursor.fetchone()

        if result:  # 如果存在匹配的元素
            # 更新匹配元素的PHip_address为param2的值
            server_db_cursor.execute("UPDATE Numbers SET PHip_address=? WHERE number = ?", (param2, code))
            server_db_conn.commit()
            server_db_cursor.execute("SELECT PCip_address FROM Numbers WHERE  number = ?", (code,))
            result = server_db_cursor.fetchall()

            print("連接成功")
            return result[0][0], 200
        else:
            # 返回123
            print("連接失敗")
            return "連接失敗", 200

        # 打印接收到的字符串
        print("Received code:", code)

        # 在这里处理收到的 code 数据，你可以将其保存到数据库或者执行其他操作

        return "Success", 200


@app.route('/user/api/submitip', methods=['POST'])
def submitip():  # 棄用
    if request.method == 'POST':
        # 从请求中获取字符串数据
        # code = request.data.decode('utf-8')
        ip = request.values["ip"]
        server_db_conn = sqlite3.connect('serverdatabase.db')
        server_db_cursor = server_db_conn.cursor()

        # 查询数据库
        server_db_cursor.execute("SELECT number FROM Numbers")

        # 打印接收到的字符串
        print("Received code:", ip)

        # 在这里处理收到的 code 数据，你可以将其保存到数据库或者执行其他操作

        return "Success", 200


@app.route('/user/api/getrollnumberV2', methods=['GET'])
def getrollnumberV2():  # 新的get roll number
    if request.method == 'GET':
        # 从请求中获取字符串数据
        # code = request.data.decode('utf-8')
        ip = request.values["ip"]
        server_db_conn = sqlite3.connect('serverdatabase.db')
        server_db_cursor = server_db_conn.cursor()

        # 查询数据库
        server_db_cursor.execute("SELECT PCip_address FROM Numbers where PHip_address = ?", (ip,))
        result = server_db_cursor.fetchall()
        server_db_cursor.execute("SELECT id FROM serverrecords where PCip_address = ?", (result[0][0],))

        rows = server_db_cursor.fetchall()
        aa = len(rows)
        print("getrollnumber")
        return str(aa)


@app.route('/user/api/getpcip', methods=['POST'])
def getpcip():  # 新的get roll number
    if request.method == 'POST':
        # 从请求中获取字符串数据
        # code = request.data.decode('utf-8')
        ip = request.values["ip"]
        server_db_conn = sqlite3.connect('serverdatabase.db')
        server_db_cursor = server_db_conn.cursor()

        # 查询数据库
        server_db_cursor.execute("SELECT PCip_address FROM Numbers where PHip_address = ?", (ip,))
        result = server_db_cursor.fetchall()
        server_db_cursor.execute("SELECT id FROM serverrecords where PCip_address = ?", (result[0][0],))

        rows = server_db_cursor.fetchall()
        aa = len(rows)
        print("getrollnumber")
        return str(aa)


@app.route('/user/api/getvideo', methods=['GET'])
def getvideo():
    id_param = request.args.get('id')
    ip_param = request.args.get('ip')
    server_db_conn = sqlite3.connect('serverdatabase.db')
    server_db_cursor = server_db_conn.cursor()
    server_db_cursor.execute("SELECT PCip_address FROM Numbers where PHip_address = ?", (ip_param,))
    result = server_db_cursor.fetchall()

    # 查询数据库
    server_db_cursor.execute("SELECT mp4base64 FROM serverrecords where id = ? and PCip_address= ?",
                             (id_param, result[0][0]))

    # 获取查询结果
    rows = server_db_cursor.fetchall()

    return json.dumps(rows)


def start_flask():
    # ssl_context = ('D:/b1programFile/bigprogram/cert.pem', 'D:/b1programFile/bigprogram/key.pem')
    # app.run(host='100.86.49.106',port=5678,ssl_context=ssl_context)
    app.run(host='100.86.59.179', port=8765)


'''
import asyncio
import websockets


async def echo(websocket, path):
    try:
        # 客户端连接时发送消息
        await websocket.send("連上了！")

        async for message in websocket:
            print(f"Received message from client: {message}")
            # 在这里处理客户端发送的消息
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed.")


start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
'''
# def efffe(xxx):
# return xxx

import asyncio
import websockets
import sqlite3
import json


# global connecttoserver
# connecttoserver=False
async def echo(websocket, path):
    try:
        # await websocket.send("已连接！")  # 在连接建立时向客户端发送消息

        records_json = await websocket.recv()  # 接收来自客户端的数据
        print("从客户端接收到的 JSON 数据:", records_json)  # 打印接收到的 JSON 数据
        if isinstance(records_json, str):
            aa = register_number(records_json)
            print("回傳register_number給客戶端")
            await websocket.send(aa)
            print("回傳register_number給客戶端成功")

        # connecttoserver=True
        try:
            records = json.loads(records_json)  # 尝试解析 JSON 数据
            print("从客户端接收到的记录:")

            # 连接服务器数据库
            server_db_conn = sqlite3.connect('serverdatabase.db')
            server_db_cursor = server_db_conn.cursor()
            print("連接到數據庫12347")
            # 将接收到的数据存储到服务器数据库中
            server_db_cursor.executemany("REPLACE INTO serverrecords (id, source, time, mp4base64) VALUES (?, ?, ?, ?)",
                                         records)
            server_db_conn.commit()
            print("已存儲到數據庫")

            print("从客户端接收并存储到数据库的记录.")

            # 关闭服务器数据库连接
            server_db_conn.close()

        except json.decoder.JSONDecodeError as e:
            print("解析 JSON 时出错:", e)
            # 可选择性地向客户端发送错误消息

    except websockets.exceptions.ConnectionClosedOK:
        print("连接已关闭.")
        # connecttoserver = False


if __name__ == '__main__':
    # 在新线程中启动 Flask 应用程序
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    print("-=============-8765")
    start_server = websockets.serve(echo, "100.86.59.179", 8767)  # 100.86.49.106 localhost

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# if __name__ == '__main__':

# conn = sqlite3.connect('serverdatabase.db')
# c = conn.cursor()

# 查询数据库
# c.execute("SELECT id, source, time FROM serverrecords")

# 获取查询结果

# rows = c.fetchall()

# 检查每一行的数据
# for row in rows:
# for item in row:
#   print(item)


'''
server_db_conn = sqlite3.connect('serverdatabase.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT record FROM serverrecords")
records = client_db_cursor.fetchall()

# 遍历记录并更新到服务器数据库
idkk = 1
for record in records:
    record_base64 = base64.b64encode(record[0]).decode('utf-8')
    # 使用 UPDATE 语句更新 serverrecords 表中的记录
    client_db_cursor.execute("UPDATE serverrecords SET recordbase64 = ? WHERE id = ?", (record_base64, idkk))
    idkk += 1

# 提交更改并关闭客户端数据库连接
server_db_conn.commit()
'''

#from ultralytics import YOLO as yolo
import json
import os.path
import database1
import livewebcam
import cv2
import torch
import io
import asyncio
import websockets
import tempfile
from ultralytics import YOLO
import zlib
from moviepy.editor import VideoFileClip

#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
#if __name__ =='__main__':
    #yolo().predict(model='yolov8m-pose.pt',source='D:/Apex Legends 2024.01.30 - 01.52.00.01.mp4',save=True)
import requests
import tkinter as tk
from tkinter import filedialog
import sqlite3
#import storeresult
from ultralytics import settings
from datetime import datetime
#print(os.path.abspath(settings['runs_dir']))
#raise
# 定义 SQLite 数据库名称
DB_NAME = 'Analysis Record Sheet.db'
# 创建数据库连接
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# 创建数据表
# 创建表格
# 检查表是否存在
c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='AnalysisRecord' ''')

# 如果表不存在，创建表
if c.fetchone()[0] != 1:
    c.execute('''
        CREATE TABLE AnalysisRecord (
            id INTEGER PRIMARY KEY,
            source TEXT,
            time DATETIME,
            record BLOB
        )
    ''')
conn.commit()


setconnected = None
setcode= None
def setsetconnected(a):
    global setconnected
    setconnected = a

def setsetcode(a):
    global setcode
    setcode = a

#results = model(source=video_path,show=True,conf=0.6,  save=True,save_txt=True,save_crop=True)
#results = model(source="0",show=True,conf=0.6,  save=True)
#print(results)
#results = model(source='D:/af8181c5be25592469fc82b8bdff9b08.mp4',show=True,conf=0.3,  save=True)

import math

def calculate_angle(A, B, C, D):
    # 計算向量 AB 和向量 CD
    vector_AB = (B[0] - A[0], B[1] - A[1])
    vector_CD = (D[0] - C[0], D[1] - C[1])

    # 計算向量的長度
    length_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2)
    length_CD = math.sqrt(vector_CD[0] ** 2 + vector_CD[1] ** 2)

    # 計算內積
    dot_product = vector_AB[0] * vector_CD[0] + vector_AB[1] * vector_CD[1]

    # 計算夾角的餘弦值
    cos_theta = dot_product / (length_AB * length_CD)

    # 使用反餘弦函數計算夾角
    angle_rad = math.acos(cos_theta)

    # 將弧度轉換為角度
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def length_AB(A, B):
    return float(math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2))


def fallcal(results):
    new_array = [0 for _ in results]
    NOTFALL=0
    for i in range(len(results) - 1):  # 遍历结果列表，注意索引范围
        if len(results[i])!=0 and len(results[i+1])!=0:#判断是否有检测到人
            # 计算相邻两帧中某个关键点（比如脖子）的位置差的平方和
            for j in range(len(results[i])):#遍历每个人
                a=False
                if results[i].keypoints.conf[j][5] > 0.65 and results[i].keypoints.conf[j][11] > 0.65:#判断是否有检测到关键点
                    angle1=calculate_angle(results[i].keypoints.data[j][11],results[i].keypoints.data[j][5],(0,1),(0,0))
                    if angle1 > 20:
                        if results[i].keypoints.conf[j][13] > 0.5 :  # 判断是否有检测到关键点
                            if calculate_angle(results[i].keypoints.data[j][13], results[i].keypoints.data[j][11], (0, 1),
                                               (0, 0)) > 15:
                                if results[i].keypoints.conf[j][15] > 0.5 :
                                    if calculate_angle(results[i].keypoints.data[j][15], results[i].keypoints.data[j][13], (0, 1),
                                                       (0, 0)) > 15:
                                        if ((results[i].keypoints.data[j][5][0] > results[i].keypoints.data[j][11][0]  >
                                                results[i].keypoints.data[j][13][0] )or (results[i].keypoints.data[j][5][0]  < results[i].keypoints.data[j][11][0]  <results[i].keypoints.data[j][13][0] ))or(abs(results[i].keypoints.data[j][15][0]-results[i].keypoints.data[j][11][0])>(length_AB(results[i].keypoints.data[j][11],results[i].keypoints.data[j][13]))*0.6):

                                            print(str(i) + "fall")
                                            new_array[i]=1
                                            #results[i].show()
                                            NOTFALL+=1
                elif results[i].keypoints.conf[j][6] > 0.6 and results[i].keypoints.conf[j][12] > 0.6:
                    angle2=calculate_angle(results[i].keypoints.data[j][12],results[i].keypoints.data[j][6],(0,1),(0,0))
                    if angle2 > 20:
                        if results[i].keypoints.conf[j][14] > 0.5 :
                            if calculate_angle(results[i].keypoints.data[j][14], results[i].keypoints.data[j][12], (0, 1),
                                               (0, 0)) > 15:
                                if results[i].keypoints.conf[j][16] > 0.5 :
                                    if calculate_angle(results[i].keypoints.data[j][16], results[i].keypoints.data[j][14], (0, 1),
                                                       (0, 0)) > 15:
                                        if ((results[i].keypoints.data[j][6][0] > results[i].keypoints.data[j][12][0]  >
                                             results[i].keypoints.data[j][14][0]) or (
                                                    results[i].keypoints.data[j][6][0] < results[i].keypoints.data[j][12][
                                                0] < results[i].keypoints.data[j][14][0])) or (abs(results[i].keypoints.data[j][16][0] - results[i].keypoints.data[j][12][0]) > (
                                                                                               length_AB(results[i].keypoints.data[j][12],results[i].keypoints.data[j][14])) * 0.6):
                                            print(str(i) + "fall")
                                            new_array[i] = 1
                                            #results[i].show()
                                            NOTFALL+=1
    return new_array,NOTFALL


def jsontime(path):
    current_time = datetime.now()
    # 格式化输出
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    json_string = json.dumps(current_time_str)
    path1 = f'{path}/time.json'
    # 将字典转换成 JSON 格式的字符串并写入文件
    with open(path1, "w") as json_file:
        json.dump(json_string, json_file)



def actual_fall_time(new_array,fps):
    ijk = 0
    array_sum = sum(new_array)
    answerarray = [0] * array_sum
    for i in range (len(new_array)):
        if new_array[i]==1:
            answerarray[ijk]=i*(1/ fps)
            ijk+=1
    return answerarray



def find_continuous_ones(new_array):
    continuous_ones_positions = []

    # 迭代檢查new_array中的元素
    for i in range(len(new_array) - 4):
        # 檢查連續五個元素是否都是1
        if all(new_array[i+j] == 1 for j in range(5)):
            continuous_ones_positions.append(i)

    return continuous_ones_positions



def extract_first_last_elements(groups):
    extracted_elements = []

    for group in groups:
        if len(group) > 0:
            first_element = group[0]
            last_element = group[-1]
            extracted_elements.append([first_element, last_element])

    return extracted_elements




def group_continuous_less_than_10(array):
    groups = []
    current_group = [array[0]]

    for i in range(1, len(array)):
        # 檢查與前一個元素的差是否小於10
        if array[i] - current_group[-1] < 150:
            current_group.append(array[i])
        else:
            groups.append(current_group)
            current_group = [array[i]]

    # 將最後一個組添加到groups中
    groups.append(current_group)

    return groups

def oneposition(array_01):
    new_array = [index for index, value in enumerate(array_01) if value == 1]
    return new_array






# 使用示例
# 准备要插入的数据


#print(results.plot())


#from PIL import Image
#img= Image.fromarray(results[70].plot()[...,::-1])
#img.show()
#results.show()
#print(results[0].save_dir)


def actualfalltimeV2(array,fps=30):


    answerarray = [[0, 0] for _ in range(len(array))]  # 初始化二维数组
    for i in range(len(array)):
        answerarray[i][0]=int(array[i][0]/ fps)
        answerarray[i][1]=int(array[i][1]/ fps)
    return answerarray



import socket

def get_local_ip():
    try:
        # 创建一个套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到外部的公共IP地址，然后获取本地IP地址
        s.connect(("8.8.8.8", 80))
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
        # 关闭套接字连接
        s.close()
        #json1=json.dumps(local_ip)
        #return json1
        return local_ip
    except socket.error:
        return "Unable to get local IP address"

# 调用函数获取本地IP地址并打印输出
#print("Local IP Address:", get_local_ip())












import cv2

def convert_avi_to_mp4(input_path, output_path):
    try:
        # 加载 AVI 文件
        clip = VideoFileClip(input_path)

        # 写入 MP4 文件
        clip.write_videofile(output_path, codec='libx264')

        print("转换完成")
    except Exception as e:
        print(f"转换时出错：{str(e)}")

def outputvedio(extract_first_last_elements1,results,fps=30,iswebcam=True,file_path="webcam"):
    print("正在輸出文件1")
    height, width = results[0].orig_shape[:2]
    # 定义视频文件名的基础部分



    # 创建 VideoWriter 对象并写入视频文件
    for idx, segment in enumerate(extract_first_last_elements1):
        start_frame, end_frame = segment[0], segment[1]
        if  start_frame > 30:
            start_frame -= 30
        else:
            start_frame = 0

        if end_frame< len(results)-60:
            end_frame += 60
        else:
            end_frame = len(results)-1

        if end_frame< len(results)-30:
            end_frame += 30
        else:
            end_frame = len(results)-1

        print("正在輸出文件2")

        # 定义当前视频文件名
        count132=database1.maxplusone()
        #count132 = database1.increment_counter()
        path = filepathandname(count132)
        starttime=int(int(segment[0])/fps)

        endtime=int(segment[1]/fps)
        if endtime==starttime:
            endtime=starttime+1
        current_time = datetime.now()
        # 格式化输出
        timedb = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("正在輸出文件3")
        file_name="webcam"
        if not iswebcam:
            timedb=f'{starttime}秒-{endtime}秒'
            file_name = os.path.basename(file_path)

        video_filename = f'{path}/video_{idx}.avi'
        # 创建 VideoWriter 对象
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
        print("正在輸出文件4")
        # 将图像序列写入视频文件
        for i in range(start_frame, end_frame):
            # 将 PIL 图像转换为 OpenCV 图像
            img = cv2.cvtColor(results[i].plot()[...,::-1], cv2.COLOR_RGB2BGR)
            out.write(img)
        print("正在輸出文件5")
        # 释放资源
        out.release()

        #convert_avi_to_mp4(video_filename, f'{path}/video_{idx}.mp4')

        with open(video_filename, 'rb') as f:
            video_bytes = f.read()
            #compressed_data = zlib.compress(video_bytes)
        #record_base64 = base64.b64encode(video_bytes).decode('utf-8')

            #temp_video_filename = 'D:/temp_video.avi'
        #with open(video_filename, 'wb') as f:
            #f.write(record[0])
        clip = VideoFileClip(video_filename)
        output_filename = 'D:/output.mp4'
        clip.write_videofile('D:/output.mp4', codec='libx264')
        with open('D:/output.mp4', "rb") as f:
            mp4_bytes = f.read()
        mp4_base64 = base64.b64encode(mp4_bytes).decode('utf-8')
        print("正在輸出文件6")

        database1.insert_data(count132, file_name,timedb , video_bytes,mp4_base64)#,record_base64
        print('寫入數據庫')
#data_to_insert = (count132, 'video1.mp4', '2024-03-05 08:30:00', b'binary_data_here')
"""
# 插入数据
c.execute('''
    INSERT INTO AnalysisRecord (id, source, time, record)
    VALUES (?, ?, ?, ?)
''', data_to_insert)
"""
def filepathandname(count):
    video_base_filename = f'D:/1resultoutput1/output_video{count}'
    if not os.path.exists(video_base_filename):
        os.makedirs(video_base_filename)
        print(f"文件夹 {video_base_filename} 已创建")
    return video_base_filename
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"文件夹 {path} 已创建")
    return path
def vedioanalyze(video_path):
    #count132 = database1.increment_counter()

    model = YOLO('yolov8x-pose-p6.pt')
    #model = YOLO('yolov8x-pose.pt')

    # video_path = 'D:/fallvedio/2d1d961b8093d32a6f59a175addf2edd.mp4'  # 请将路径替换为您的视频文件路径#半身
    # video_path = 'D:/4bd4c9ed367fc9665d4c831e15e17979.mp4'#兩人
    # video_path = 'D:/fallvedio/1973f5f2f4440fb4557edd3533bd9cd7.mp4'#跌倒
    # video_path = 'D:/fallvedio/childfall.mp4'#小孩跌倒
    # video_path = 'D:/ca60918a31e05c9a2ccdcd3df845b033.mp4'#彎腰
    # video_path = 'D:/ridefall.mp4'#騎車自摔
    # video_path = 'D:/fallvedio/NBA  Scary Fall  MOMENTS.mp4'#騎車自摔
    #video_path = 'D:/fallvedio/falltwice.mp4'  # 跌倒2次

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    results = model(source=video_path, show=True, conf=0.7)#, save=True, save_txt=True, save_crop=True
    print("视频帧率为:", fps)
    falltiming,falltime=fallcal(results)
    if falltime >5:
        #actual_fall_time(falltiming,fps)

        oneposition1 = oneposition(falltiming)
        print("1的位置：", oneposition1)
    # find_continuous_ones1=find_continuous_ones(falltiming)
        group_continuous_less_than_101 = group_continuous_less_than_10(oneposition1)
        print("連續小於10的元素分組：", group_continuous_less_than_101)
        extract_first_last_elements1 = extract_first_last_elements(group_continuous_less_than_101)
        print("提取的第一個和最後一個元素：", extract_first_last_elements1)

        #actual_fall_time(falltiming, fps)
    #if falltime不等於0
        #path = filepathandname(200)

        outputvedio(extract_first_last_elements1, results,fps, iswebcam=False, file_path=video_path)
    cv2.destroyAllWindows()
    return falltime


    #storeresult.process_video_and_save_json(results, path)

#def setwifigg(xxx):
    #xxx


def livewebcamanalyze():
    #count132 = database1.increment_counter()
    #path1 = filepathandname(count132)
    idx= 0
    livewebcam.livewebcamgo(analyze)

def analyze(gg):
    idx = 0
    falltiming, falltime = fallcal(gg)
    if falltime == 0:
        print("not fall")
    if falltime > 5:
        count132 = database1.increment_counter()
        path = filepathandname(count132)
        # path=f'{path1}/{idx}'
        create_path(path)
        oneposition1 = oneposition(falltiming)
        group_continuous_less_than_101 = group_continuous_less_than_10(oneposition1)
        extract_first_last_elements1 = extract_first_last_elements(group_continuous_less_than_101)
        outputvedio(extract_first_last_elements1, gg)
        # outputvedio(extract_first_last_elements1,results,path)
        # storeresult.process_video_and_save_json(gg, path)
        # jsontime(path)
        idx += 1

#livewebcamanalyze()
#vedioanalyze()

"""
print(type(current_time_str))
# 打印当前时间
# 创建包含时间的字典
data = {"current_time": current_time_str}

# 将字典转换成 JSON 格式的字符串
json_string = json.dumps(data)
print("当前时间（年-月-日 时:分:秒）：", current_time_str)
file_path = "/path/to/your/file.json"  # 修改为你想要存储的路径
"""
#array_2d = [[30, 100], [200, 300], [500, 1000]]
#print(len(array_2d))

#print(actualfalltimeV2(array_2d))

"""
id_value = 1
source_value = 'video1.mp4'
time_value = '2024-03-05 08:30:00'
record_blob_value = b'binary_data_here'
#data_to_insert = (id_value, source_value, time_value, record_blob_value)
#cursor.execute('''INSERT INTO records (id, source, time, record) VALUES (?, ?, ?, ?)''', data_to_insert)

cursor.execute('''SELECT * FROM records''')
rows = cursor.fetchall()

    # 输出查询结果
for row in rows:
    print(row)
    print("123")
"""


# 输出查询结果












#print("Inserted Data:", inserted_data)

def play_video_from_database(database_path, video_id):
    # 连接到数据库
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # 执行查询，获取视频数据
    cursor.execute('''SELECT record FROM records WHERE id = ?''', (video_id,))
    video_blob = cursor.fetchone()[0]

    # 将视频数据写入临时文件
    temp_video_file = tempfile.NamedTemporaryFile(delete=False)
    temp_video_file.write(video_blob)
    temp_video_file.close()

    # 读取临时文件中的视频并在屏幕上播放
    video_capture = cv2.VideoCapture(temp_video_file.name)
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # 清理临时文件
    video_capture.release()
    cv2.destroyAllWindows()
    temp_video_file.close()

    # 关闭数据库连接
    conn.close()

#play_video_from_database('databasego.db', 44)
#url = 'https://localhost:8000'
#new_array = [1, 2, 3, 4, 5]
# 设置要发送的数据
#data = {'message': '12345'}
#data = {'results': answerarray}
# 发送 HTTPS POST 请求
#response = requests.post(url, data=data, verify=False)

# 打印服务器响应
#print(response.text)
# 发送 HTTPS POST 请求
#response = requests.post(url, json=data, verify=False)

# 打印服务器响应
#print(response.text)

def report_fall(time, who):
    response = requests.get("http://127.0.0.1:5000/fall_report?t=" + time + "&who=" + who)


def login(username, password):
    response = requests.get("http://127.0.0.1:5000/user/api/login?user=" + username + "&passwd=" + password)


#login("LIU-SHU CHI", "123456789ABCDEF")

#report_fall("2024-03-02-18-43", "奶奶")

import base64


def pagejson():
    server_db_conn = sqlite3.connect('databasego.db')
    client_db_cursor = server_db_conn.cursor()
    # 查询数据库并将结果转换为 JSON 格式
    client_db_cursor.execute("SELECT id, source, time, recordrecord64 FROM records")
    records = client_db_cursor.fetchall()

    # 对包含字节类型数据的记录进行处理
    processed_records = []
    for record in records:
        id, source, time, record_bytes = record  # 分解记录中的各个字段
        # 将字节类型数据转换为 base64 编码的字符串
        record_base64 = base64.b64encode(record_bytes).decode('utf-8')
        processed_record = (id, source, time, record_base64)  # 更新记录
        processed_records.append(processed_record)

    # 将处理后的记录转换为 JSON 格式
    records_json = json.dumps(processed_records)
    return records_json


def packjson():
    server_db_conn = sqlite3.connect('databasego.db')
    client_db_cursor = server_db_conn.cursor()
    # 查询数据库并将结果转换为 JSON 格式
    print("client_db_cursor = server_db_conn.cursor()")
    client_db_cursor.execute("SELECT id, source, time, mp4base64 FROM records")
    print("client_db_cursor.execute(SELECT id, source, time, recordbase64 FROM records)")
    records = client_db_cursor.fetchall()
    print("records = client_db_cursor.fetchall()")
    records_json = json.dumps(records)#,ensure_ascii=False
    print(" records_json = json.dumps(records)")
    server_db_conn.close()
    return records_json

def login1(ip,data):
    print("login1")
    url = "http://100.86.59.179:8765/user/api/login1"

    try:

        #response = requests.get(url, json=payload)
        #aa = [None]
        #aa[0]=ip
        #aa[1]=data

        #response = requests.get(url, json=payload)
        #response = requests.get(url, params=aa)
        #response = requests.post(url, json={'ip': ip,'data': data })
        response = requests.post(url, json={'ip': ip, 'data': data})

        # 如果连接服务器成功，可以根据需要处理响应
        if response.status_code == 200:
            print("成功连接到服务器并发送数据。")
        else:
            print(f"连接到服务器，但出现问题：{response.status_code}")

        # 在这里执行剩余的代码

    except requests.exceptions.RequestException as e:
        print("连接服务器时出现异常:", e)
        # 如果连接服务器失败，可以根据需要执行其他操作l
        # 在这里执行剩余的代码



def login12(data):
    print("login1")
    url = "http://100.86.59.179:8765/user/api/login12"

    print('id')
    for record in data:
        print(record['id'])
    print('id')
    try:

        #response = requests.get(url, json=payload)
        #aa = [None]
        #aa[0]=ip
        #aa[1]=data

        #response = requests.get(url, json=payload)
        #response = requests.get(url, params=aa)
        #response = requests.post(url, json={'ip': ip,'data': data })
        response = requests.get(url, json=data)

        # 如果连接服务器成功，可以根据需要处理响应
        if response.status_code == 200:
            print("成功连接到服务器并发送数据。")
        else:
            print(f"连接到服务器，但出现问题：{response.status_code}")

        # 在这里执行剩余的代码

    except requests.exceptions.RequestException as e:
        print("连接服务器时出现异常:", e)
#login1(packjson())


import asyncio#數據庫
import threading
import websockets

websocket_connected = False

async def send_message_to_server(message):
    global websocket_connected
    uri = "ws://100.86.59.179:8767"
    try:
        async with websockets.connect(uri) as websocket:
            websocket_connected = True

            
            await websocket.send(message)
            print(f"Sent message to server: {message}")
            code =await websocket.recv()
            if code is not None:
                print("Message from server 密碼:", code)
                global setcode

                setcode(str(code))
                #await websocket.send(message)



    except Exception as e:
        websocket_connected = False
        print("Failed to connect to server:", e)
    global setconnected
    if setconnected is not None:
        setconnected(websocket_connected)



async def connect_to_server():
    while True:
        await asyncio.sleep(10)  # 每10秒尝试连接一次
        await send_message_to_server(get_local_ip())
        #code =await websocket.recv()


        #if message is not None:
            #print("Message from server:", message)


        #print("Message from server:", code)

        #await send_message_to_server("Hello, Server!")
async def send_database_to_server(message):
    if websocket_connected:
        # 连接客户端数据库

        print("====234r4324233")
        # 连接服务器
        uri = "ws://100.86.59.179:8767"
        async with websockets.connect(uri) as websocket:
            # 发送数据到服务器
            await websocket.send(message)
            print("Sent database records to server.")
        # 关闭客户端数据库连接
        #client_db_conn.close()
    else:
        print("Not connected to server. Cannot send database.")
def background_task():
    asyncio.run(connect_to_server())

def send_iiii_message():
    if websocket_connected:
        asyncio.run(send_message_to_server("iiii[]"))

    else:
        print("Not connected to server. Cannot send message.")

def send_database_to_serverport():
    if websocket_connected:
        client_db_conn = sqlite3.connect('databasego.db')
        client_db_cursor = client_db_conn.cursor()
        """
        # 查询数据库并将结果转换为 JSON 格式
        client_db_cursor.execute("SELECT id,source,time,recordbase64 FROM records where id =1")
        records = client_db_cursor.fetchall()
        records_json = json.dumps(records)
        asyncio.run(send_message_to_server(records_json))
        """

        client_db_cursor.execute("SELECT id,source,time,mp4base64 FROM records ")
        for row in client_db_cursor.fetchall():
            row_json = json.dumps(row)
            asyncio.run(send_message_to_server(row_json))

    else:
        print("Not connected to server. Cannot send database.")



def main():
    # 在新线程中启动后台任务
    background_thread = threading.Thread(target=background_task)
    background_thread.start()

    # 其他操作可以放在这里，不会被连接服务器的操作阻塞
    print("Main program is running...")

    # 示例：每隔一段时间调用发送消息的函数
    #while True:
        # 在这里添加您希望调用发送消息的逻辑
        #send_iiii_message()
        #asyncio.sleep(30)  # 每30秒调用一次发送消息的函数

main()

#asyncio.run(send_iiii_message())





"""
import zlib
import base64

# Connect to the server database
server_db_conn = sqlite3.connect('databasego.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT record FROM records")
records = client_db_cursor.fetchall()

# 遍历记录并更新到服务器数据库
idkk = 1
for record in records:
    # 获取原始记录数据
    record_data = record[0]
    print("record_data")
    print(type(record_data))

    # 计算原始数据大小
    original_size = len(record_data)

    # 将原始数据进行 Base64 编码
    uncompressbase64 = base64.b64encode(record_data).decode('utf-8')
    print("uncompressbase64")
    print(type(uncompressbase64))

    # 计算 Base64 编码后数据大小
    uncompressbase64_size = len(uncompressbase64)

    # 压缩数据
    compressed_data = zlib.compress(record_data)

    # 计算压缩后数据大小
    compressed_size = len(compressed_data)

    record_base64= base64.b64encode(compressed_data)
    print("record_base64")
    print(type(record_base64))

    # 将压缩后的数据转换为 Base64 编码
    record_base64utf = base64.b64encode(compressed_data).decode('utf-8')

    print("record_base64utf")
    print(type(record_base64utf))

    # 计算 Base64 编码后数据大小
    base64_size = len(record_base64)

    # 使用 UPDATE 语句更新 serverrecords 表中的记录
    client_db_cursor.execute("UPDATE records SET recordbase64 = ? WHERE id = ?", (record_base64, idkk))

    # 输出记录的大小信息
    print(
        f"Record {idkk}: Original size: {original_size} bytes, Compressed size: {compressed_size} bytes, uncompressbase64_size: {uncompressbase64_size}, Base64 size: {base64_size} bytes")

    idkk += 1

# 提交更改并关闭客户端数据库连接
server_db_conn.commit()

"""









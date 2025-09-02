from moviepy.editor import VideoFileClip

import os
import sqlite3
import base64
def increment_counter(file_path='counter.txt'):
    try:
        # 读取之前的数字
        with open(file_path, 'r') as file:
            count = int(file.read().strip())
    except FileNotFoundError:
        # 如果文件不存在，则从1开始
        count = 1

    # 将数字加1
    count += 1

    # 将新数字写入文件
    with open(file_path, 'w') as file:
        file.write(str(count))

    return count



# 连接到 SQLite 数据库
conn = sqlite3.connect('databasego.db')
cursor = conn.cursor()

# 创建表格
# 创建表格
cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY,
                    source TEXT,
                    time TEXT,
                    record BLOB
                )''')

# 提交更改并关闭连接
conn.commit()
conn.close()

def insert_data(id_value, source_value, time_value, record_blob_value,mp4):
    print(f"innnnnnnnnnnnnnnnnnnn  {id_value} {source_value} {time_value}")
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('databasego.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY,
                        source TEXT,
                        time TEXT,
                        record BLOB
                        mp4base64 TEXT
                        
                    )''')

    # 插入一条数据
    data_to_insert = (id_value, source_value, time_value, record_blob_value,mp4)
    cursor.execute('''INSERT INTO records (id, source, time, record,mp4base64) VALUES (?, ?, ?, ?,?)''', data_to_insert)

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

# 使用示例
#insert_data('id_value', 'source_value', 'time_value', b'record_blob_value')
def creatcount():
    import sqlite3

    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行创建表的 SQL 语句
    cursor.execute('''CREATE TABLE IF NOT EXISTS tablecount (
                        count1 INTEGER,
                        count2 INTEGER
                    )''')

    cursor.execute("INSERT INTO tablecount (count1, count2) VALUES (1, 1)")
    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()

def findmax():
    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行查询，获取count1列的最大值
    cursor.execute("SELECT MAX(count1) FROM tablecount")

    # 从游标中获取查询结果
    max_count1 = cursor.fetchone()[0]

    # 关闭连接
    conn.close()
    return max_count1

def findmax2():
    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行查询，获取count1列的最大值
    cursor.execute("SELECT MAX(id) FROM records")

    # 从游标中获取查询结果
    max_count1 = cursor.fetchone()[0]

    # 关闭连接
    conn.close()
    return max_count1



def maxplusone():
    import sqlite3

    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询表中count1列的最大值
    cursor.execute("SELECT MAX(id) FROM records")

    # 从游标中获取查询结果
    max_count1 = cursor.fetchone()[0]

    # 计算新的值
    new_count1 = max_count1 + 1

    # 插入新的行
    #cursor.execute("INSERT INTO tablecount (count1) VALUES (?)", (new_count1,))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()

    # 打印插入的值
    print(new_count1)
    return new_count1


def maxplusone2():
    import sqlite3

    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询表中count1列的最大值
    cursor.execute("SELECT MAX(count1) FROM tablecount")

    # 从游标中获取查询结果
    max_count1 = cursor.fetchone()[0]

    # 计算新的值
    new_count1 = max_count1 + 1

    # 插入新的行
    cursor.execute("INSERT INTO records (ID) VALUES (?)", (new_count1,))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()

    # 打印插入的值
    print(new_count1)
    return new_count1

import sqlite3

def reassign_ids():
    # 连接到数据库
    conn = sqlite3.connect('databasego.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询表中的所有id，并按照大小排序
    cursor.execute("SELECT id FROM records ORDER BY id")

    # 获取查询结果
    ids = cursor.fetchall()

    # 遍历查询结果，为每个id分配一个新的值
    new_ids = {}
    for index, old_id in enumerate(ids, start=1):
        new_ids[old_id[0]] = index

    # 更新表中的id值为新的值
    for old_id, new_id in new_ids.items():
        cursor.execute("UPDATE records SET id = ? WHERE id = ?", (new_id, old_id))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()

# 调用函数
reassign_ids()


#conn = sqlite3.connect('databasego.db')
#c = conn.cursor()

# 执行 SQL 语句
#c.execute('''ALTER TABLE records ADD COLUMN PCip_address TEXT;''')
#c.execute('''ALTER TABLE records DROP COLUMN recordbase64;''')
#c.execute('''ALTER TABLE records DROP COLUMN PCip_address;''')

# 提交更改并关闭连接
#conn.commit()
#conn.close()


"""
conn = sqlite3.connect('databasego.db')
cursor = conn.cursor()
cursor.execute('''DROP TABLE recordstest''')
cursor.execute('''CREATE TABLE IF NOT EXISTS recordstest (
                    id INTEGER PRIMARY KEY,
                    source TEXT,
                    time TEXT,
                    record BLOB,
                    recordbase64 TEXT
                    mp4base64 TEXT

                )''')
conn.commit()
"""
# conn.close()

# 插入一条数据

'''
# 提交更改并关闭连接

server_db_conn = sqlite3.connect('databasego.db')
client_db_cursor = server_db_conn.cursor()
# 查询数据库并将结果转换为 JSON 格式
client_db_cursor.execute("SELECT id, source, time, recordbase64 FROM records")
records = client_db_cursor.fetchall()

for i in [0,1,2,3]:
    re=records[i]
    data_to_insert = (re[0], re[1], re[2], re[3])
    #cursor.execute(INSERT INTO recordstest (id, source, time, recordbase64) VALUES (?, ?, ?, ?) data_to_insert)
    conn.commit()



conn.close()
'''
"""
server_db_conn = sqlite3.connect('databasego.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT record FROM records")
records1 = client_db_cursor.fetchall()

# 遍历记录并更新到服务器数据库
idkk = 1
for record in records1:
    record_base64 = base64.b64encode(record[0]).decode('utf-8')

    # 使用 UPDATE 语句更新 serverrecords 表中的记录
    client_db_cursor.execute("UPDATE records SET mp4base64 = ? WHERE id = ?", (record_base64, idkk))
    idkk += 1

# 提交更改并关闭客户端数据库连接
server_db_conn.commit()
"""




"""#轉換到mp4
server_db_conn = sqlite3.connect('databasego.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT record FROM records")
records1 = client_db_cursor.fetchall()
print("client_db_cursor.fetchall()")
#print(type(records1[0][0]))

idkk = 1
for record in records1:
    temp_video_filename = 'D:/temp_video.avi'
    with open(temp_video_filename, 'wb') as f:
        f.write(record[0])
    clip = VideoFileClip(temp_video_filename)
    output_filename = 'D:/output.mp4'
    clip.write_videofile('D:/output.mp4', codec='libx264')
    with open('D:/output.mp4', "rb") as f:
        mp4_bytes = f.read()
    mp4_base64 = base64.b64encode(mp4_bytes).decode('utf-8')
    # 使用 UPDATE 语句更新 serverrecords 表中的记录
    client_db_cursor.execute("UPDATE records SET mp4base64 = ? WHERE id = ?", (mp4_base64, idkk))
    idkk += 1
# 提交更改并关闭客户端数据库连接
server_db_conn.commit()
os.remove(temp_video_filename)
os.remove(output_filename)

"""









# 删除临时文件
"""
server_db_conn = sqlite3.connect('databasego.db')
client_db_cursor = server_db_conn.cursor()

# 查询客户端数据库并获取记录
client_db_cursor.execute("SELECT record FROM records where id = 4")
recordaa = client_db_cursor.fetchall()
temp_video_filename = 'D:/temp_video.avi'
with open(temp_video_filename, 'wb') as f:
    f.write(recordaa[0][0])
clip = VideoFileClip(temp_video_filename)
output_filename = 'D:/output.mp4'
clip.write_videofile('D:/output.mp4', codec='libx264')
with open('D:/output.mp4', "rb") as f:
    mp4_bytes = f.read()
mp4_base64 = base64.b64encode(mp4_bytes).decode('utf-8')
print(mp4_base64)
# 使用 UPDATE 语句更新 serverrecords 表中的记录
client_db_cursor.execute("UPDATE records SET mp4base64 = ? WHERE id = ?", (mp4_base64, 4))
print("client_db_cursor.execute()")
server_db_conn.commit()
os.remove(temp_video_filename)
"""
"""
import cv2
from ultralytics import YOLO
def vedioanalyze(video_path):
    model = YOLO('yolov8m-pose.pt') # 初始化YOLO模型
    cap = cv2.VideoCapture(video_path) # 打開視頻文件
    fps = cap.get(cv2.CAP_PROP_FPS)    # 獲取視頻的幀率
    results = model(source=video_path, show=True, conf=0.7, save=True, save_txt=True, save_crop=True) # 使用YOLO模型進行視頻分析
    falltiming, falltime = fallcal(results) #分析跌倒
    # 如果跌倒數帧數超過5，則進行進一步處理
    if falltime > 5:
        # 將連續跌倒視為一次跌倒，給出跌倒起始和結束時間
        oneposition1 = oneposition(falltiming)
        group_continuous_less_than_101 = group_continuous_less_than_10(oneposition1)
        extract_first_last_elements1 = extract_first_last_elements(group_continuous_less_than_101)
        # 生成分析結果視頻
        outputvedio(extract_first_last_elements1, results, fps, iswebcam=False, file_path=video_path)
    cv2.destroyAllWindows()# 關閉視窗
    return falltime    # 返回跌倒時間

from datetime import datetime
def outputvedio(extract_first_last_elements1, results, fps=30, iswebcam=True, file_path="webcam"):
    height, width = results[0].orig_shape[:2] # 获取结果图像的高度和宽度
    for idx, segment in enumerate(extract_first_last_elements1): # 遍历分段列表并生成视频文件
        start_frame, end_frame = segment[0], segment[1]
        # 获取当前视频的文件名
        count132 = database1.maxplusone()#获取数据库中的行數並加一
        path = filepathandname(count132) #將行數並加一作為文件路径的一部份
        starttime = int(int(segment[0]) / fps)#計算實際跌倒起始時間
        endtime = int(segment[1] / fps) #計算實際跌倒結束時間
        # 如果结束时间与开始时间相同，则增加1秒
        if endtime == starttime:
            endtime = starttime + 1
        # 获取当前时间并格式化输出
        current_time = datetime.now()
        timedb = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # 如果不是来自摄像头，则使用开始和结束时间作为时间戳
        file_name = "webcam"
        if not iswebcam:
            timedb = f'{starttime}秒-{endtime}秒'
            file_name = os.path.basename(file_path)
        # 设置视频文件名
        video_filename = f'{path}/video_{idx}.avi'
        # 创建 VideoWriter 对象
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
        # 将图像序列写入视频文件
        for i in range(start_frame, end_frame):
            # 将 PIL 图像转换为 OpenCV 图像
            img = cv2.cvtColor(results[i].plot()[...,::-1], cv2.COLOR_RGB2BGR)
            out.write(img)
        out.release()  # 释放资源
        
        # 读取视频文件
        with open(video_filename, 'rb') as f:
            video_bytes = f.read()
        # 转换为Mp4视频文件
        clip = VideoFileClip(video_filename)
        output_filename = 'D:/output.mp4'
        clip.write_videofile('D:/output.mp4', codec='libx264')
        # 读取MP4文件并转换为base64编码
        with open('D:/output.mp4', "rb") as f:
            mp4_bytes = f.read()
        mp4_base64 = base64.b64encode(mp4_bytes).decode('utf-8')
        # 将数据插入数据库
        database1.insert_data(count132, file_name, timedb, video_bytes, mp4_base64)

"""
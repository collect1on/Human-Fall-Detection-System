from ultralytics import YOLO
import threading
import cv2
import time

# 定义全局变量
iiii = []
stop_thread = False
def run_tracker_in_thread(filename, model: YOLO, file_index, xxx):
    """
    运行视频文件或网络摄像头流并与 YOLOv8 模型同时进行处理。
    """
    start_thread_func()

    global iiii, stop_thread
    video = cv2.VideoCapture(filename)  # 读取视频文件或摄像头流
    start_time = time.time()

    while True:
        ret, frame = video.read()  # 读取视频帧

        if not ret:
            break

        # 使用模型进行目标跟踪
        results = model.track(frame, persist=True, conf=0.70)
        iiii.extend(results)

        # 显示处理后的视频帧
        res_plotted = results[0].plot()
        cv2.imshow(f"Tracking_Stream_{file_index}", res_plotted)

        # 等待按键 'q' 或者超过30秒退出
        key = cv2.waitKey(1)
        if time.time() - start_time >= 10:
            print("====================================================\n"*10)
            xxx(iiii)
            iiii = []
            start_time = time.time()

        if key == ord('q') or stop_thread:
            break

    # 释放视频源
    video.release()
    cv2.destroyAllWindows()






def stop_thread_func():
    """
    停止线程的函数
    """
    global stop_thread
    stop_thread = True

def start_thread_func():
    """
    停止线程的函数
    """
    global stop_thread
    stop_thread = False


def livewebcamgo(xxx):
    """
    启动实时视频处理
    """


    global iiii, stop_thread
    iiii = []


    # 加载模型
    model1 = YOLO('yolov8m-pose.pt')

    # 定义视频文件
    video_file1 = 0  # 0代表网络摄像头

    # 创建线程
    tracker_thread1 = threading.Thread(target=run_tracker_in_thread, args=(video_file1, model1, 1, xxx), daemon=True)

    # 启动线程
    tracker_thread1.start()

    # 等待线程结束
    # tracker_thread1.join()
    #for i in range(len(iiii)):
    #    iiii[i].save(f'{path}/resultsqq{i}.jpg')
    # 返回处理结果
    return stop_thread

# 调用实时视频处理函数
#livewebcamgo()

# 处理结束后保存结果图片


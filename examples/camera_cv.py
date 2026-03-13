import numpy as np # 引入numpy 用于矩阵运算
import cv2 # 引入opencv库函数
import time

## VideCapture里面的序号
# 0 : 默认为笔记本上的摄像头(如果有的话) / USB摄像头 webcam
# 1 : 奥比中光相机
# 6 ：罗技C922摄像头

# 创建一个video capture的实例
cap = cv2.VideoCapture(6)

# 查看Video Capture是否已经打开
print("摄像头是否已经打开 ？ {}".format(cap.isOpened()))

## 设置画面的尺寸和帧率
# 罗技 C922 推荐配置：
#   1920x1080 @ 30fps (高清)
#   1280x720  @ 60fps (高帧率)
#   640x480   @ 60fps (低延迟)

# 目标分辨率和帧率
configurations = [
    (1920, 1080, 30), # 1080p 配置
    (640, 480, 30)    # 640x480 配置
]
target_width = configurations[1][0] # 1920
target_height = configurations[1][1] # 480
target_fps = configurations[1][2] # 30

print(f"\n尝试设置分辨率: {target_width}x{target_height} @ {target_fps}fps")

# 设置分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)
# 设置帧率
cap.set(cv2.CAP_PROP_FPS, target_fps)

# 验证实际设置的参数
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
actual_fps = int(cap.get(cv2.CAP_PROP_FPS))

print(f"实际分辨率: {actual_width}x{actual_height} @ {actual_fps}fps")
if actual_width != target_width or actual_height != target_height:
    print(f"⚠️  警告: 相机不支持目标分辨率，已自动调整")
if actual_fps != target_fps:
    print(f"⚠️  警告: 相机不支持目标帧率，已自动调整")

## 创建一个名字叫做 “image_win” 的窗口
# 窗口属性 flags
#   * WINDOW_NORMAL：窗口可以放缩
#   * WINDOW_KEEPRATIO：窗口缩放的过程中保持比率
#   * WINDOW_GUI_EXPANDED： 使用新版本功能增强的GUI窗口
cv2.namedWindow('image_win',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

# 图像计数 从1开始
img_count = 1

# 计算FPS的变量
prev_time = time.time()
fps = 0
frame_count = 0

# 帮助信息
helpInfo = '''
==============
提示-按键前需要选中当前画面显示的窗口

按键Q： 退出程序
按键C： Capture 拍照
'''
print(helpInfo)
while(True):
    ## 逐帧获取画面
    # 如果画面读取成功 ret=True，frame是读取到的图片对象(numpy的ndarray格式)
    ret, frame = cap.read()
    
    if not ret:
        print("图像获取失败，请按照说明进行问题排查")
        break
    
    ## 颜色空间变换
    # 将BGR彩图变换为灰度图
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ## 图片镜像
    # * 水平翻转 flipCode = 1
    # * 垂直翻转 flipCode = 0
    # * 同时水平翻转与垂直翻转 flipCode = -1
    # 
    # flipCode = -1
    # frame = cv2.flip(frame, flipCode)

    # --- FPS 计算 ---
    frame_count += 1
    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    
    if elapsed_time >= 1.0: # 每秒更新一次 FPS
        fps = frame_count / elapsed_time
        # print(f"当前实时帧 rate: {fps:.2f} FPS") # 终端打印
        frame_count = 0
        prev_time = curr_time
    
    # 更新窗口“image_win”中的图片
    cv2.putText(frame, f"FPS: {fps:.2f}", (20, 40), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3) 
    # 参数说明：(图片对象，文本内容，文本位置，字体，字体大小，颜色，线宽)
    cv2.imshow('image_win',frame)
    
    # 等待按键事件发生 等待1ms
    key = cv2.waitKey(1)
    if key == ord('q'):
        # 如果按键为q 代表quit 退出程序
        print("程序正常退出")
        break
    elif key == ord('c'):
        ## 如果c键按下，则进行图片保存
        # 写入图片 并命名图片为 图片序号.png
        cv2.imwrite("{}.png".format(img_count), frame)
        print("截图，并保存为  {}.png".format(img_count))
        # 图片编号计数自增1
        img_count += 1

# 释放VideoCapture
cap.release()
# 销毁所有的窗口
cv2.destroyAllWindows()

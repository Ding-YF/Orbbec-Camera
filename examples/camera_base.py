import cv2
import time
from pyorbbecsdk import Pipeline, Config, OBSensorType, OBFormat, FrameSet
from utils import frame_to_bgr_image

def main():
    pipeline = Pipeline()
    config = Config()

    try:
        config.enable_video_stream(OBSensorType.COLOR_SENSOR, 640, 480, 60, OBFormat.RGB)
        pipeline.start(config)
    except Exception as e:
        print(f"无法启动流: {e}")
        return

    prev_time = time.time()
    fps = 0
    frame_count = 0

    try:
        while True:
            frames: FrameSet = pipeline.wait_for_frames(100)
            if frames is None:
                continue

            color_frame = frames.get_color_frame()
            if color_frame is None:
                continue

            # --- FPS 计算 ---
            frame_count += 1
            curr_time = time.time()
            elapsed_time = curr_time - prev_time
            
            if elapsed_time >= 1.0: # 每秒更新一次 FPS
                fps = frame_count / elapsed_time
                # print(f"当前实时帧 rate: {fps:.2f} FPS") # 终端打印
                frame_count = 0
                prev_time = curr_time

            # 2. 转换并显示图像
            color_image = frame_to_bgr_image(color_frame)
            if color_image is not None:
                # 在图像上绘制 FPS
                cv2.putText(color_image, f"FPS: {fps:.2f}", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow("Orbbec SDK FPS Demo", color_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
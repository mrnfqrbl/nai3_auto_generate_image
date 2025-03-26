import imageio
import imageio_ffmpeg
import os
import sys
import cv2
import numpy as np

def 降低帧率(输入文件路径, 输出文件路径, 目标帧率):
    """
    降低视频的帧率，但保持总帧数不变。

    Args:
        输入文件路径 (str): 输入视频文件的路径。
        输出文件路径 (str): 输出视频文件的路径。
        目标帧率 (int): 降低后的目标帧率。
    """
    try:
        # 读取视频
        reader = imageio.get_reader(输入文件路径)
        原始帧率 = reader.get_meta_data()['fps']
        宽度 = reader.get_meta_data()['size'][0]
        高度 = reader.get_meta_data()['size'][1]

        # 创建视频写入器
        writer = imageio.get_writer(输出文件路径, fps=目标帧率, quality=None)  # quality=None 避免压缩

        # 读取帧并进行处理
        for i, frame in enumerate(reader):
            writer.append_data(frame)

        # 释放资源
        reader.close()
        writer.close()
        print(f"降低帧率完成 (保持总帧数): {输入文件路径} -> {输出文件路径}")

    except Exception as e:
        print(f"降低帧率失败: {输入文件路径}")
        print(f"错误信息: {e}")

import cv2
import numpy as np

def 高级插帧(输入文件路径, 输出文件路径, 目标帧率):
    """
    使用光流法进行插帧，以减少拖影、提高稳定性和清晰度。

    Args:
        输入文件路径 (str): 输入视频文件的路径。
        输出文件路径 (str): 输出视频文件的路径。
        目标帧率 (int): 插帧后的目标帧率。
    """
    try:
        # 读取视频
        视频 = cv2.VideoCapture(输入文件路径)
        原始帧率 = 视频.get(cv2.CAP_PROP_FPS)
        宽度 = int(视频.get(cv2.CAP_PROP_FRAME_WIDTH))
        高度 = int(视频.get(cv2.CAP_PROP_FRAME_HEIGHT))
        总帧数 = int(视频.get(cv2.CAP_PROP_FRAME_COUNT))

        # 创建视频写入器
        视频写入器 = cv2.VideoWriter(输出文件路径, cv2.VideoWriter_fourcc(*'mp4v'), 目标帧率, (宽度, 高度))

        # 创建光流估计器 (DIS算法)
        光流估计器 = cv2.optflow.createOptFlow_DIS(cv2.optflow.DISOPTICAL_FLOW_PRESET_ULTRAFAST)

        # 读取第一帧并转换为灰度图
        成功, 上一帧 = 视频.read()
        if not 成功:
            print("无法读取第一帧")
            return
        上一帧灰度 = cv2.cvtColor(上一帧, cv2.COLOR_BGR2GRAY)

        帧计数 = 1 # 从1开始计数，因为已经读取了第一帧

        while True:
            # 读取下一帧
            成功, 当前帧 = 视频.read()
            if not 成功:
                break

            帧计数 += 1
            print(f"处理帧: {帧计数}/{总帧数}")

            # 转换为灰度图
            当前帧灰度 = cv2.cvtColor(当前帧, cv2.COLOR_BGR2GRAY)

            # 计算光流
            光流 = 光流估计器.calc(上一帧灰度, 当前帧灰度, None)

            # 计算需要插值的帧数
            插值帧数 = int(目标帧率 / 原始帧率) - 1

            # 插值
            for i in range(1, 插值帧数 + 1):
                # 计算插值比例
                比例 = i / (插值帧数 + 1)

                # 创建空的插值帧
                插值帧 = np.zeros_like(当前帧, dtype=np.float32)

                # 遍历每个像素
                for y in range(高度):
                    for x in range(宽度):
                        # 使用光流估计像素在上一帧和当前帧之间的位置
                        x_偏移 = 光流[y, x][0]
                        y_偏移 = 光流[y, x][1]

                        # 计算插值后的像素位置
                        插值_x = int(x - 比例 * x_偏移)
                        插值_y = int(y - 比例 * y_偏移)

                        # 确保像素位置在图像范围内
                        插值_x = np.clip(插值_x, 0, 宽度 - 1)
                        插值_y = np.clip(插值_y, 0, 高度 - 1)

                        # 使用双线性插值获取像素颜色
                        插值帧[y, x] = (1 - 比例) * 上一帧[插值_y, 插值_x] + 比例 * 当前帧[y, x]

                # 转换为 uint8
                插值帧 = np.uint8(插值帧)

                # 写入插值帧
                视频写入器.write(插值帧)

            # 写入当前帧
            视频写入器.write(当前帧)

            # 更新上一帧
            上一帧 = 当前帧
            上一帧灰度 = 当前帧灰度

        # 释放资源
        视频.release()
        视频写入器.release()
        print(f"高级插帧完成: {输入文件路径} -> {输出文件路径}")

    except Exception as e:
        print(f"高级插帧失败: {输入文件路径}")
        print(f"错误信息: {e}")

# 主程序
if __name__ == "__main__":
    降速后的视频 = r"D:\down\降速后的视频.mp4"  # 注意：这里输入的是降速后的视频
    插帧后的视频 = r"D:\down\插帧后的视频.mp4"
    目标帧率_降速 = 7  # 设置降低后的帧率
    目标帧率_插帧 = 30  # 设置插帧后的目标帧率 (通常与原始视频帧率相同)
    原始视频文件 = r"D:\down\WanVideoWrapper_I2V_00001.mp4" # 原始视频文件

    # 检查 OpenCV 是否已安装
    try:
        import cv2
    except ImportError:
        print("OpenCV 未安装，正在安装...")
        os.system(f"{sys.executable} -m pip install opencv-python")
        print("OpenCV 安装完成，请重新运行脚本。")
        exit()

    # 检查 imageio-ffmpeg 是否已安装
    try:
        import imageio_ffmpeg
    except ImportError:
        print("imageio-ffmpeg 未安装，正在安装...")
        os.system(f"{sys.executable} -m pip install imageio-ffmpeg")
        print("imageio-ffmpeg 安装完成，请重新运行脚本。")
        exit()

    # 检查 FFmpeg 是否已下载
    try:
        imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        print("FFmpeg 未下载，正在下载...")
        try:
            imageio_ffmpeg.download()
            print("FFmpeg 下载完成，请重新运行脚本。")
        except Exception as e2:
            print("FFmpeg 下载失败，请检查网络连接或手动安装 FFmpeg。")
        exit()

    # 1. 降低帧率 (保持总帧数)
    降低帧率(原始视频文件, 降速后的视频, 目标帧率_降速) # 注释掉，因为已经有降速后的视频

    # 2. 线性插帧 (保持动作速度)
    高级插帧(降速后的视频, 插帧后的视频, 目标帧率_插帧)

    print("完成！")

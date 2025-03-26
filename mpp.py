# import cv2
# from pymediainfo import MediaInfo
#
# def 分析视频信息(视频文件路径):
#     """
#     分析视频文件信息，并找出可能导致解码问题的因素。
#
#     Args:
#         视频文件路径 (str): 视频文件的路径。
#
#     Returns:
#         dict: 包含视频信息的字典。
#     """
#
#     视频信息 = {}
#
#     # 使用 OpenCV 读取视频信息
#     cap = cv2.VideoCapture(视频文件路径)
#     if not cap.isOpened():
#         print(f"无法打开视频文件: {视频文件路径}")
#         return None
#
#     视频信息['宽度'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     视频信息['高度'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     视频信息['帧率'] = cap.get(cv2.CAP_PROP_FPS)
#     视频信息['总帧数'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     视频信息['视频编码'] = cap.get(cv2.CAP_PROP_FOURCC)  # 返回的是 FOURCC 码
#
#     # 将 FOURCC 码转换为可读的字符串
#     fourcc_int = int(视频信息['视频编码'])
#     视频信息['视频编码_字符串'] = chr(fourcc_int & 0xFF) + chr((fourcc_int >> 8) & 0xFF) + chr((fourcc_int >> 16) & 0xFF) + chr((fourcc_int >> 24) & 0xFF)
#
#     cap.release()
#
#     # 使用 MediaInfo 读取更详细的视频信息
#     try:
#         media_info = MediaInfo.parse(视频文件路径)
#         for track in media_info.tracks:
#             if track.track_type == 'Video':
#                 视频信息['编码器'] = track.codec
#                 视频信息['配置文件'] = track.format_profile
#                 视频信息['码率'] = track.bit_rate
#                 视频信息['颜色空间'] = track.color_space
#                 视频信息['扫描类型'] = track.scan_type
#                 # 添加更多 MediaInfo 提供的字段
#     except Exception as e:
#         print(f"使用 MediaInfo 解析视频文件时出错: {e}")
#
#     return 视频信息
#
#
# def 打印视频信息(视频信息):
#     """
#     打印视频信息。
#
#     Args:
#         视频信息 (dict): 包含视频信息的字典。
#     """
#
#     if not 视频信息:
#         print("未获取到视频信息。")
#         return
#
#     print("视频信息:")
#     for 键, 值 in 视频信息.items():
#         print(f"  {键}: {值}")
#
# def 分析解码问题(视频信息):
#     """
#     根据视频信息分析可能导致解码问题的因素。
#
#     Args:
#         视频信息 (dict): 包含视频信息的字典。
#     """
#
#     if not 视频信息:
#         print("未获取到视频信息，无法分析解码问题。")
#         return
#
#     print("\n可能导致解码问题的因素:")
#
#     # 检查编码格式
#     常见编码 = ['H264', 'AVC', 'VP9', 'HEVC', 'MPEG4', 'Theora']
#     if '编码器' in 视频信息 and 视频信息['编码器'] not in 常见编码:
#         print(f"  - 编码格式 '{视频信息['编码器']}' 可能不被所有播放器支持。")
#
#     # 检查分辨率
#     if '宽度' in 视频信息 and '高度' in 视频信息:
#         if 视频信息['宽度'] > 3840 or 视频信息['高度'] > 2160:  # 4K 分辨率
#             print("  - 分辨率过高，某些播放器可能无法正常显示。")
#
#     # 检查帧率
#     if '帧率' in 视频信息:
#         if 视频信息['帧率'] > 60:
#             print("  - 帧率过高，某些播放器可能无法流畅播放。")
#
#     # 检查码率
#     if '码率' in 视频信息 and 视频信息['码率'] is not None:  # 添加码率检查
#         if 视频信息['码率'] > 20000000:  # 20 Mbps
#             print("  - 码率过高，某些播放器可能无法流畅播放。")
#
#     # 检查配置文件
#     if '配置文件' in 视频信息:
#         if 'High' in 视频信息['配置文件']:
#             print("  - 配置文件为 High Profile，某些播放器可能不支持。")
#
#     # 检查颜色空间
#     if '颜色空间' in 视频信息:
#         if 视频信息['颜色空间'] not in ['YUV', 'YCbCr', 'RGB']:
#             print(f"  - 颜色空间 '{视频信息['颜色空间']}' 可能不被所有播放器支持。")
#
#     # 检查扫描类型
#     if '扫描类型' in 视频信息:
#         if 视频信息['扫描类型'] == 'Interlaced':
#             print("  - 扫描类型为隔行扫描，某些播放器可能无法正确显示。")
#
#
# # 主程序
# if __name__ == "__main__":
#     视频文件路径 = r"D:\down\WanVideoWrapper_I2V_00001.mp4"
#
#     视频信息 = 分析视频信息(视频文件路径)
#
#     打印视频信息(视频信息)
#
#     分析解码问题(视频信息)

import imageio
import imageio_ffmpeg
import os
import sys
import cv2

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

        # 计算时间缩放因子
        时间缩放因子 = 原始帧率 / 目标帧率

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


# 主程序
if __name__ == "__main__":
    输入视频文件 = r"D:\down\WanVideoWrapper_I2V_00001.mp4"
    输出视频文件 = r"D:\down\降速后的视频.mp4"
    目标帧率 = 7 # 设置降低后的帧率

    # 检查 OpenCV 是否已安装
    try:
        import cv2
    except ImportError:
        print("OpenCV 未安装，但此脚本不需要 OpenCV。")

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
            print(f"错误信息: {e2}")
        exit()

    # 1. 降低帧率 (保持总帧数)
    降低帧率(输入视频文件, 输出视频文件, 目标帧率)

    print("完成！")
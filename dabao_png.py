from datetime import datetime
import os
import subprocess
import time  # 用于获取当前时间，生成目录名等


当天时间=datetime.now().strftime('%Y年%m月%d日')
def compress_directory(directory_path, output_dir, compression_level=5):
    """
    使用 7z 命令行工具压缩指定目录，并为输出文件附加 'nai' 后缀。
    :param directory_path: 需要压缩的目录路径
    :param output_dir: 压缩包保存的目标目录
    :param compression_level: 压缩级别，默认为 5 (中等压缩)
    """
    # 获取目录的名称（不包含路径）
    dir_name = os.path.basename(directory_path)

    # 创建压缩文件的名称，附加 'nai' 后缀
    compressed_filename = os.path.join(output_dir, f"{dir_name}_nai.7z")

    # 定义7z可执行文件路径
    seven_zip_path = r"C:\Program Files\7-Zip-Zstandard\7z.exe"

    # 构建7z命令，指定LZMA2算法、多线程和压缩级别
    command = [
        seven_zip_path,
        "a",  # 添加到压缩包
        f"-m0=lzma2",  # 使用 LZMA2 算法
        f"-mx={compression_level}",  # 设置压缩级别（1-9，数字越大压缩越慢但效果越好）
        f"-mmt=on",  # 启用多线程
        f"{compressed_filename}",  # 输出的压缩包文件名
        f"{directory_path}\\*"  # 需要压缩的文件和文件夹
    ]

    # 使用 subprocess 调用系统命令执行压缩
    try:
        subprocess.run(command, check=True)
        print(f"成功压缩目录: {directory_path} -> {compressed_filename}")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {directory_path}. 错误信息: {e}")


def compress_all_directories_in_current_dir(input_dir, output_dir, compression_level=5):
    """
    压缩当前目录下的每个子目录，并为压缩包名称附加 'nai' 后缀。
    :param input_dir: 输入的目录，包含子目录
    :param output_dir: 输出目录，用于保存压缩包
    :param compression_level: 压缩级别，默认为 5 (中等压缩)
    """
    # 遍历当前目录下的每个子目录
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)

        # 判断是否是目录
        if os.path.isdir(item_path):
            dir_name = os.path.basename(item_path)
            if dir_name== 当天时间:
                pass
            else:

                compressed_filename = os.path.join(output_dir, f"{dir_name}_nai.7z")

                # 检查是否已存在压缩包
                if os.path.exists(compressed_filename):
                    print(f"压缩包 {compressed_filename} 已存在，")
                    #append_new_images_to_archive(compressed_filename, item_path, output_dir, compression_level)
                else:
                    print(f"压缩包 {compressed_filename} 不存在，正在压缩目录...")
                    compress_directory(item_path, output_dir, compression_level)

if __name__ == "__main__":
#    input_dir = r"W:\nai"  # 设置你要压缩的目录路径
#    output_dir = r"F:\图\ai备份"  # 设置压缩包保存的目标目录
    input_dir=r"W:\sd"
    output_dir=r"F:\图\sd备份"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    compression_level = 0  # 设置压缩级别，默认为 5（中等压缩）

    # 确保输出目录存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 执行压缩
    compress_all_directories_in_current_dir(input_dir, output_dir, compression_level)

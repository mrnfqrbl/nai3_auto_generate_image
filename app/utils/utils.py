import json
import os
import zipfile
from io import BytesIO


from app.utils.log_config import logger
from datetime import datetime


class 保存序号和图片:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        # cls._instance.__init__(*args, **kwargs)  # 这里调用会初始化两次
        return cls._instance

    def __init__(self, 序号文件位置):

        self.序号文件位置 = 序号文件位置
        self.image_counter = None
        self.current_date = datetime.now().strftime('%Y%m%d')
        self.f_current_date=datetime.now().strftime('%Y年%m月%d日')

    def load_counter(self):

        """
        加载序号计数器，检查日期是否匹配，如果匹配则返回存储的序号，否则重置为1。
        如果文件不存在，创建新的文件并初始化计数器。
        """
        #logger.debug(f"序号文件路径: {self.序号文件位置}")  # 调试打印文件路径

        # 如果序号文件存在，则读取文件
        self.current_date = datetime.now().strftime('%Y%m%d')
        self.f_current_date=datetime.now().strftime('%Y年%m月%d日')
        if os.path.exists(self.序号文件位置):
            try:
                with open(self.序号文件位置, 'r', encoding='utf-8') as f:
                    data = json.load(f)


                    # 检查文件格式：外层应该是字典
                    if not isinstance(data, dict):
                        logger.error(f"序号文件格式错误，期望为字典类型，但读取到的是 {type(data)}")
                        return 1  # 如果格式错误，直接返回初始序号 1

                    # 检查当前日期是否存在于文件中
                    logger.debug(f"data:{data}")
                    logger.debug(f"current_date:{self.current_date}")

                    date_entry = data.get(self.f_current_date)
                    if date_entry and date_entry.get("date") == self.current_date:
                        return data[self.f_current_date]['counter']  # 返回当天的计数器
                    else:
                        return 1  # 如果当前日期不在文件中，返回初始序号 1
            except (json.JSONDecodeError, IOError) as e:
                self.initialize_counter()
                logger.warning(f"警告: 序号文件损坏或无法读取，正在重置计数器。错误信息: {e}")

        # 如果文件不存在或者损坏，则初始化文件
        self.initialize_counter()
        return 1  # 如果文件不存在或日期不匹配，返回初始序号 1

    def initialize_counter(self):
        """
        如果序号文件不存在或无法读取，则初始化文件并保存初始序号。
        """
        data = {
            self.f_current_date: {'date': self.current_date, 'counter': 1}
        }
        # 确保目录存在
        data_folder = os.path.dirname(self.序号文件位置)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # 创建并写入新的序号文件
        with open(self.序号文件位置, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4,ensure_ascii=False)
        logger.info(f"初始化序号文件: {self.序号文件位置}")

    def save_counter(self):
        """
        保存当前日期和序号到文件。
        """
        #logger.info(f"序号;{self.image_counter}")
        try:
            with open(self.序号文件位置, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

        # 更新当前日期的序号
        if self.f_current_date in data:
            data[self.f_current_date]['counter'] = self.image_counter
        else:
            data[self.f_current_date] = {'date': self.current_date, 'counter': self.image_counter}

        # 保存更新后的数据
        with open(self.序号文件位置, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4,ensure_ascii=False)

        logger.debug(f"保存序号到文件: {self.序号文件位置}")
    def save_image(self,image_data: bytes, save_path: str,  img_name: str=""):
    # 确保保存图像的目录存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 创建 ZIP 文件对象
        try:
            with zipfile.ZipFile(BytesIO(image_data)) as zf:
                file_names = zf.namelist()

                if file_names:
                    image_filename = file_names[0]  # 获取第一个图像文件名

                    with zf.open(image_filename) as img_file:
                        img_data = img_file.read()

                        # 生成文件名，附加种子


                        image_path = os.path.join(save_path , img_name)

                        # 确保保存图像的目录存在
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)

                        # 将图像数据保存为本地文件
                        with open(image_path, "wb") as f:
                            f.write(img_data)

                    #logger.info(f"图像已保存至: {image_path}")
                    return {"状态": "成功", "保存路径": image_path}
                else:
                    return {"状态": "失败", "错误信息": "ZIP文件中没有图像。"}
                    #3logger.error("ZIP文件中没有图像。")
        except Exception as e:
            return {"状态": "失败", "错误信息": f"下载图像时出错: {e}"}

            #logger.error(f"下载图像时出错: {e}")















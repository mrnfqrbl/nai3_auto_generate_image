import json
import os
import random
import sys
import time
import traceback
import zipfile
from datetime import datetime
from io import BytesIO

from app.config_manager import ConfigManager
from app.log_config import logger
from app.novelai_api import NovelAI_API
from app.tag import 提示词生成器


# 全局异常捕获函数
def global_exception_handler(exctype, value, tb):
    """
    全局异常处理函数，捕获程序中未处理的异常并记录日志。
    """
    if exctype == UnicodeDecodeError:
        logger.error(f"捕获到编码错误: {value}")
    else:
        logger.error(f"未处理的异常: {exctype.__name__} - {value}")

    logger.error("堆栈信息:")
    logger.error(''.join(traceback.format_exception(exctype, value, tb)))

    # 选择是否退出程序
    sys.exit(1)  # 或者使用 `exit(1)` 退出程序

# 注册全局异常处理
sys.excepthook = global_exception_handler

class ImageGenerator:
    def __init__(self, config_path: str):
        """
        初始化类，加载配置文件，实例化API。

        :param config_path: 配置文件路径
        """
        self.config_path = config_path
        self.token = ""
        self.quantity = 0
        self.sm = 0
        self.保存位置 = r".\img"
        self.序号文件位置 = r"data\sequence.json"
        self.tags位置 = r"data\tags.json"
        # 加载配置
        # 初始化 API 实例


        # 获取当前日期并初始化图像计数器
        self.current_date = datetime.now().strftime('%Y%m%d')
        self.f_current_date= datetime.now().strftime('%Y年%m月%d日')
        logger.info(f"当前日期: {self.f_current_date}")

        self.config_load()
        self.api = NovelAI_API(self.token)
        self.image_counter = self.load_counter()


    def config_load(self):
        """
        加载配置文件并设置 token 和生成图像的数量等参数。
        """
        config_manager = ConfigManager(self.config_path)

        # 读取配置文件中的API token和生成图像数量
        self.token = config_manager.get("API", "token")
        # print("tonken:",self.token.strip())
        if self.token.strip() == "" or self.token.strip() == "你的api令牌":
            logger.warning("未设置API Token，请检查配置文件。")
            time.sleep(5)
            exit(1)
        self.quantity = config_manager.get_int("GENERATION", "quantity")
        保存位置_a = config_manager.get("GENERATION", "保存位置")
        tags位置_a = config_manager.get("GENERATION", "tags位置")
        序号文件位置_a = config_manager.get("GENERATION", "序号文件位置")
        # 将保存位置、tags位置和序号文件位置的赋值修改为 os.path.join
        self.保存位置 = os.path.join(保存位置_a)
        self.tags位置 = os.path.join(tags位置_a)
        self.序号文件位置 = os.path.join(序号文件位置_a)

        logger.info(f"保存位置: {self.保存位置}")
        logger.info(f"tags位置: {self.tags位置}")
        logger.info(f"序号文件位置: {self.序号文件位置}")

        logger.debug(f"API Token: {self.token}")
        logger.info(f"总数量: {self.quantity}")

    def load_counter(self):
        """
        加载序号计数器，检查日期是否匹配，如果匹配则返回存储的序号，否则重置为1。
        如果文件不存在，创建新的文件并初始化计数器。
        """
        logger.debug(f"序号文件路径: {self.序号文件位置}")  # 调试打印文件路径

        # 如果序号文件存在，则读取文件
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

                    # date = data[self.f_current_date]['date']
                    # logger.debug(f"date:{date}")
                    # if self.current_date in date:
                    #     return data[self.f_current_date]['counter']  # 返回当天的计数器
                    # else:
                    #     return 1  # 如果当前日期不在文件中，返回初始序号 1
            except (json.JSONDecodeError, IOError) as e:
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

    def generate_img(self, *args, **kwargs):

        # 获取或设置默认参数
        角色 = kwargs.get('角色', None)
        画风 = kwargs.get('画风', None)
        动作 = kwargs.get('动作', None)
        质量 = kwargs.get('质量', "best quality, amazing quality, very aesthetic, absurdres")
        proportional = kwargs.get('proportional', "竖向")
        self.sm=kwargs.get('sm', 0)
        new_negative_prompt = kwargs.get('new_negative_prompt', "")
        sampling = kwargs.get('sampling', "ke")
        seed_a = kwargs.get('seed', 0)
        smea = kwargs.get('smea', 0)

        提示词=提示词生成器(角色=角色, 画风=画风, 动作=动作, 质量=质量)
        # 使用每次循环时重新生成提示词
        for i in range(self.quantity):
            # 每次循环重新生成prompt
            prompt = 提示词.提示词组合(是否随机=True)
            # 使用随机种子
            if seed_a in (None, 0, "", -1):
                seed = random.randint(11111, 10000000)
            elif seed_a >= 10000:
                seed = seed_a
            else:
                seed = random.randint(11111, 10000000)
                logger.warning(f"警告: 输入的种子 {seed_a} 不在有效范围内，已使用随机种子 {seed} 代替。")


            logger.info(f"第 {i + 1} 张图像生成中，种子: {seed}")

            logger.debug(f"main-generate_img_提示词为:{prompt}")
            # 调用API生成图像
            image_data = self.api.generate_image(prompt, seed=seed, proportional=proportional, smea=self.sm,
                                                 sampling=sampling, )

            if image_data:

                logger.info(f"第 {i + 1} 张图像生成成功，已返回原始ZIP文件内容！")
                self.download_img(image_data, seed)  # 下载并保存图像
            else:
                logger.error(f"第 {i + 1} 张图像生成失败。")

            # 每生成一张图像后延时1秒
            time.sleep(1)

    def get_filename(self, seed: int):
        """
        生成带有种子的文件名，并确保每次生成图像时序号递增。

        :param seed: 生成图像的种子
        :return: 返回生成的文件名
        """
        self.image_counter = self.load_counter()
        current_time = datetime.now().strftime('%H-%M-%S')
        filename = f"{self.image_counter:03d}---{current_time}---{seed}.png"

        # 更新序号
        self.image_counter += 1
        self.save_counter()
        return filename

    def download_img(self, img_data: bytes, seed: int):
        """
        处理生成的图像数据，保存到本地文件。

        :param img_data: 图像数据
        :param seed: 生成图像的种子，附加到文件名

        """
        logger.info(f"保存位置{self.保存位置}")
        save_directory = self.保存位置
        # if save_directory is None:
        #
        #
        logger.info(f"保存目录: {save_directory}类型为: {type(save_directory)}")

        # 确保保存图像的目录存在
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # 创建 ZIP 文件对象
        try:
            with zipfile.ZipFile(BytesIO(img_data)) as zf:
                file_names = zf.namelist()

                if file_names:
                    image_filename = file_names[0]  # 获取第一个图像文件名

                    with zf.open(image_filename) as img_file:
                        img_data = img_file.read()

                        # 生成文件名，附加种子
                        filename = self.get_filename(seed)

                        print(save_directory)
                        image_path = os.path.join(save_directory, self.f_current_date, filename)

                        # 确保保存图像的目录存在
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)

                        # 将图像数据保存为本地文件
                        with open(image_path, "wb") as f:
                            f.write(img_data)

                    logger.info(f"图像已保存至: {image_path}")
                else:
                    logger.error("ZIP文件中没有图像。")
        except Exception as e:

            logger.error(f"下载图像时出错: {e}")
            tb_info = traceback.format_exc()
            logger.error(tb_info)




if __name__ == "__main__":
    # 配置文件路径
    config_path = "config.ini"

    # 创建图像生成器实例
    image_gen = ImageGenerator(config_path)
    tags位置 = image_gen.tags位置
    logger.info(f"generate_img  保存位置: {image_gen.保存位置}")
    # 检查文件是否存在
    tags_file_path = tags位置
    default_tags = {
        "__注释": "角色：为你喜欢的角色格式如下，画风：为艺术家组合同下，动作：为除开角色画风的其余部分包括服装动作等以及需要叠加覆盖的人物特征，质量：指定生成图片质量的一般不需要改",
        "角色": {
            "1": "{yaoyao (genshin impact)}",
            "2": "bailu (honkai: star rail)"
        },
        "画风": {
            "1": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]",
            "2": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]"
        },
        "动作": {
            "1": "1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,green eyes,{loli},ahoge,looking at viewer,standing on one leg,blush,standing,parted lips,leg up, cowboy shot, {{close-up}}, ,no_panties,tuncensored,pussy ,{Sneakers},{{Pussy object  insertion}},{sex},{anus},{Very thick carrot},{Orgasm}, {shivering},{bedroom},Full body portrait",
            "2": "1girl,loli,ass focus,(see-through,white pantyhose),side lying,looking at viewer,from below,{{Cat ears}},{sex},{nsfw},{no panties},Pussy, anus,{ Thick Tentacles}, {{Anal insertion}},{No tail},{{Tentacle anal insertion}},clothes_pull,"
        },
        "质量": "best quality, amazing quality, very aesthetic, absurdres"
    }
    if not os.path.exists(tags_file_path):
        # 如果文件不存在，创建文件并写入默认数据
        os.makedirs(os.path.dirname(tags_file_path), exist_ok=True)  # 确保目录存在
        with open(tags_file_path, "w", encoding="utf-8") as file:
            json.dump(default_tags, file, ensure_ascii=False, indent=4)
        logger.warning(f"文件 {tags_file_path} 不存在，已创建并写入默认数据。")
    # 读取文件内容
    with open(tags_file_path, "r", encoding="utf-8") as file:
        tags = json.load(file)
        if json.dumps(tags, ensure_ascii=False, indent=4).strip() == json.dumps(default_tags, ensure_ascii=False,
                                                                                indent=4).strip():
            logger.warning("检测到默认数据，请修改tags.json文件后启动，延时5秒关闭")
            time.sleep(5)
            sys.exit()

    角色= tags['角色']
    画风= tags['画风']
    动作= tags['动作']
    质量 =tags['质量']

    logger.debug(f"角色:{角色}")
    logger.debug(f"画风:{画风}")
    logger.debug(f"动作:{动作}")
    logger.debug(f"质量:{质量}")

    """
    samplers = {
    "ke": "k_euler",
    "kea": "k_euler_ancestral",
    "dmp++2s": "k_dpmpp_2s_ancestral",
    "dmp++2m": "k_dpmpp_2m_sde",
    }
    """
    image_gen.generate_img(proportional="随机", 角色=角色, 画风=画风, 动作=动作, 质量=质量, sm=2, seed=0, sampling=1)

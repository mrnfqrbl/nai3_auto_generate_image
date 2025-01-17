import configparser
import os
import sys
import time

from app import logger


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

        # 如果配置文件不存在，则创建默认配置
        if not os.path.exists(config_path):
            logger.info("配置文件不存在，正在创建默认配置...")
            self.create_default_config()
        else:
            # 读取配置文件，确保使用 UTF-8 编码
            self.config.read(config_path, encoding='utf-8')

    def create_default_config(self):
        # 创建默认配置内容
        self.config['API'] = {
            'token': '你的api令牌'  # 请手动填写 token
        }
        self.config['GENERATION'] = {
            'quantity': '10',  # 默认生成 10 张图像
            "保存位置": r"D:\xm\nai3_auto_generate_image\img",
            '序号文件位置': r"D:\xm\nai3_auto_generate_image\data\sequence.json",
            'tags位置': r'D:\xm\nai3_auto_generate_image\data\tags.json'
        }

        # 如果需要更多的路径配置，取消下面的注释
        # self.config['PATHS'] = {
        #     'positive_prompt_file': 'data/positive_prompts.json',
        #     'negative_prompt_file': 'data/negative_prompts.json',
        #     'rules_file': 'data/rules.json',
        #     'configuration_file': 'data/configuration.json',
        #     'output_folder': 'outputs/'
        # }

        # 写入配置文件，确保使用 UTF-8 编码
        with open(self.config_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        logger.info(f"默认配置已创建，配置文件路径: {self.config_path}")

    def get(self, section: str, option: str) -> str:
        # 如果配置文件中没有指定 section 和 option 的配置项，抛出 ValueError 异常
        if not self.config.has_option(section, option):
            raise ValueError(f"配置项不存在: {section}.{option}")

        # 获取 API token 配置，并去除多余的空格
        token = self.config.get("API", "token").strip()

        # 记录读取到的 token 值，帮助排查
        logger.debug(f"读取的 token 值: '{token}'")

        # 检查 token 是否为默认值
        if token == "你的api令牌" or token == "":
            logger.warning("未设置有效的 API Token，请检查配置文件。")
            time.sleep(5)
            sys.exit("程序退出：请修改配置文件中的 token 配置")

        return self.config.get(section, option)

    def get_int(self, section: str, option: str) -> int:
        # 获取整数配置项
        return self.config.getint(section, option)
    # def load_data(self):
    #
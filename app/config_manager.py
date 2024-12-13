import configparser
import os
from app.log_config import logger
class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

        # 如果配置文件不存在，则创建默认配置
        if not os.path.exists(config_path):
            print("配置文件不存在，正在创建默认配置...")
            self.create_default_config()
        else:
            self.config.read(config_path)

    def create_default_config(self):
        # 创建默认配置内容
        self.config['API'] = {
            'token': '你的api令牌'  # 请手动填写 token
        }
        self.config['GENERATION'] = {
            'quantity': '10'  # 默认生成 10 张图像
        }
        # self.config['PATHS'] = {
        #     'positive_prompt_file': 'data/positive_prompts.json',
        #     'negative_prompt_file': 'data/negative_prompts.json',
        #     'rules_file': 'data/rules.json',
        #     'configuration_file': 'data/configuration.json',
        #     'output_folder': 'outputs/'
        # }

        # 写入配置文件
        with open(self.config_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        logger.info(f"默认配置已创建，配置文件路径: {self.config_path}")

    def get(self, section: str, option: str) -> str:
        return self.config.get(section, option)

    def get_int(self, section: str, option: str) -> int:
        return self.config.getint(section, option)

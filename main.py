import asyncio
import json
import os
import sys
import time
import traceback

from app import logger
from app.utils.config_manager import ConfigManager
from app.utils.fozu import 佛祖保佑

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

class main():
    def __init__(self):
        self.root_dir=os.getcwd()
        logger.info(f"当前路径: {self.root_dir}")
        self.token=None
        self.生成数量=None
        self.保存位置=None
        self.load_config()


    def load_config(self):
        """
        加载配置文件并设置 token 和生成图像的数量等参数。
        """
        config_manager = ConfigManager("config.ini")

        # 读取配置文件中的API token和生成图像数量
        self.token = config_manager.get("API", "token")
        # print("tonken:",self.token.strip())
        if self.token.strip() == "" or self.token.strip() == "你的api令牌":
            logger.warning("未设置API Token，请检查配置文件。")
            time.sleep(5)
            exit(1)
        self.生成数量 = config_manager.get_int("GENERATION", "quantity")
        保存位置_a = config_manager.get("GENERATION", "保存位置")
        # tags位置_a = config_manager.get("GENERATION", "tags位置")
        # 序号文件位置_a = config_manager.get("GENERATION", "序号文件位置")
        # 将保存位置、tags位置和序号文件位置的赋值修改为 os.path.join
        self.保存位置 = os.path.join(保存位置_a)
        # tags位置 = os.path.join(tags位置_a)
        # 序号文件位置 = os.path.join(序号文件位置_a)
        #
        logger.info(f"保存位置: {self.保存位置}")
        # logger.info(f"tags位置: {tags位置}")
        # logger.info(f"序号文件位置: {序号文件位置}")
        #
        logger.debug(f"API Token: {self.token}")
        logger.info(f"总数量: {self.生成数量}")


    def tag(self):
        佛祖保佑()
        tags位置 = f"{self.root_dir}/data/tags.json"
        tags_file_path = tags位置
        try:
            with open(tags_file_path, "r", encoding="utf-8") as file:
                tags = json.load(file)
                self.角色 = tags['角色']
                self.画风 = tags['画风']
                self.动作 = tags['动作']
                self.质量 = tags['质量']
                logger.info("Tags loaded successfully.")
        except FileNotFoundError:
            logger.error(f"Error: tags.json file not found at {tags_file_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"Error: Invalid JSON in tags.json file.")
            sys.exit(1)
        except KeyError as e:
            logger.error(f"Error: Missing key in tags.json: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            sys.exit(1)

    def 无限生成提示词(self):
        """
        无限生成提示词，每 3 秒输出一个到控制台。
        """
        if not all([self.角色, self.画风, self.动作, self.质量]):
            logger.error("请先运行 tag() 方法加载 tags.json 数据。")
            return
        from app.utils.tag import 提示词生成器
        提示词生成器实例 = 提示词生成器(
            角色=self.角色,
            画风=self.画风,
            质量=self.质量,
            动作=self.动作,
        )

        try:
            while True:
                prompt = 提示词生成器实例.提示词组合(sd=True)
                logger.info(f"生成的提示词: {prompt}")
                time.sleep(5)  # 暂停 3 秒
        except asyncio.CancelledError:
            logger.info("无限生成任务已取消。")






    def main(self):
        佛祖保佑()
        from app import ApiOperation
        #api=ApiOperation(__token="123",test=True,保存路径="./dev_img",批量生成=True,生成次数=self.生成数量,root_dir=self.root_dir)
        api=ApiOperation(__token=self.token,环境="正式",保存路径=self.保存位置,批量生成=True,生成次数=self.生成数量,root_dir=self.root_dir)
        tags位置 = f"{self.root_dir}/data/tags.json"
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
        参数={"角色":角色,
              "画风":画风,
              "质量":质量,
              "动作":动作,
              "seed":0,
              "尺寸":"随机",
              "采样":0,
              "cfg":0,
              "smea":0,
              "是否随机组合画师":False,
              "是否指定画风":8,
              "是否指定动作": False,
              "是否指定角色": False,
              "角色是否可无":True,
              "角色获取方式":"顺序",
              "画风获取方式":"顺序",
              "动作获取方式":"顺序",
              }
        asyncio.run(api.无限生成图片(**参数))
#2345789
if __name__ == "__main__":
    class_main=main()
    class_main.tag()
    class_main.无限生成提示词()

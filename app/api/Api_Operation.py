import asyncio
import json
import os
import sys
import time
import tracemalloc

from app import logger
from app import save_image, Counter
from app import 参数生成器
from app import 提示词生成器
from app.api.api import NovelAIAPI

tracemalloc.start()
class ApiOperation(NovelAIAPI):
    def __new__(cls,**kwargs):
        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance
    def __init__(self,**kwargs):
        self.root_dir=kwargs.get("root_dir","../../")
        self.__token=kwargs.get("__token","1211113")
        self.test=kwargs.get("test",False)
        self.保存路径=kwargs.get("保存路径","./dev_img/")
        self.序号实例=Counter(f"{self.root_dir}/data/序号.json")
        self.批量生成=kwargs.get("批量生成",False)

        super().__init__(__token=self.__token,test=self.test)
        self.json_data=json.load(open(f"{self.root_dir}/data/data.json", "r", encoding="utf-8"))
        self.gi_json_data=self.json_data["Generate_Image"]["v3"]
        #self.序号实例=Counter(f"{root_dir}data/序号.json")
        if self.批量生成:
            self.批量生成次数=kwargs.get("生成次数",1)





    async def 单次生成图片(self,**接收参数):
        提示词 = 接收参数.get("prompt")
        #模型 = 接收参数.get("model")
        宽度 = 接收参数.get("width")
        高度 = 接收参数.get("height")
        采样器 = 接收参数.get("sampler")
        引导系数 = 接收参数.get("cfg")
        种子 = 接收参数.get("seed")
        负面 = 接收参数.get("negative_prompt")
        sm = 接收参数.get("sm")
        debug = 接收参数.get("debug")

        self.gi_json_data["input"]=提示词
        #self.gi_json_data["model"]=模型
        self.gi_json_data["parameters"]["width"]=宽度
        self.gi_json_data["parameters"]["height"]=高度
        self.gi_json_data["parameters"]["scale"]=引导系数
        self.gi_json_data["parameters"]["sampler"]=采样器
        self.gi_json_data["parameters"]["seed"]=种子
        if 负面:
            新负面=self.gi_json_data["parameters"].get("negative_prompt", "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract],") +","+ 负面
            self.gi_json_data["parameters"]["negative_prompt"] = 新负面
        self.gi_json_data["parameters"]["smea"]=sm
        # return await self.api_generate_image(self.gi_json_data,debug=debug)
        logger.debug(f"json为：{self.gi_json_data}")
        img_data=await self.api_generate_image(self.gi_json_data ,debug=debug)
        图片序号=self.序号实例.load_counter()
        logger.info(f"图片序号:{图片序号}")
        from datetime import datetime
        标准可读_日期= datetime.now().strftime('%H-%M-%S')
        年月日_日期 = datetime.now().strftime('%Y年%m月%d日')
        文件名 = f"{图片序号:03d}--{年月日_日期}--{标准可读_日期}--{种子}.png"
        save_image(img_data, self.保存路径, 文件名)
        图片序号 += 1
        self.序号实例.image_counter=图片序号
        logger.info(f"新图片序号:{图片序号}")
        self.序号实例.save_counter()

    async def 批量随机生成图片(self,**接收参数):
        角色=接收参数["角色"]
        画风=接收参数["画风"]
        质量=接收参数["质量"]
        动作=接收参数["动作"]
        接收种子=接收参数["seed"]
        尺寸=接收参数["尺寸"]
        采样=接收参数["采样"]
        cfg=接收参数["cfg"]
        smea=接收参数["smea"]

        提示词生成器实例=提示词生成器(角色=角色,画风=画风,质量=质量,动作=动作,是否随机=True)
        参数生成器实例=参数生成器(尺寸=尺寸,采样=采样,提示词引导系数=cfg,种子=接收种子,smea=smea)
        用户数据=await self.api_get_user_data()
        logger.debug(f"用户数据为：{用户数据}")
        logger.info(f"无限生成状态为：{用户数据['subscription']['perks']['unlimitedImageGeneration']}")
        if 用户数据["subscription"]["perks"]["unlimitedImageGeneration"] == False:
            logger.warning("没有无限生成需要付费，已停止")
            logger.info("没有无限生成需要付费确定还要继续吗？靓仔")
            if input("确定还要继续吗？(y/n)") == "y":
                logger.info("继续")
                pass
            else:
                logger.info("停止")
                return "停止"
            # return "没有无限生成需要付费确定还要继续吗？靓仔"
        logger.info(f"无限生成正常")
        for i in range(self.批量生成次数):
            # 每次循环重新生成prompt
            prompt = 提示词生成器实例.提示词组合(是否随机=True)
            参数=参数生成器实例.获取参数()
            传递参数字典={
                "prompt":prompt,
                "width":参数["尺寸"].get("宽度"),
                "height":参数["尺寸"].get("高度"),
                "sampler":参数["采样"],
                "cfg":参数["提示词引导系数"],
                "seed":参数["种子"],
                "sm":参数["smea"],
            }

            logger.info(f"第 {i + 1} 张图像生成中，种子: {参数['种子']}")

            logger.debug(f"main-generate_img_提示词为:{prompt}")
            # 调用API生成图像
            await self.单次生成图片(**传递参数字典)
            time.sleep(1)







if __name__ == '__main__':

    api=ApiOperation(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj",test=False,保存路径=r"../../dev_img",批量生成=True,生成次数=10)
    logger.info("开始生成图片")
    tags位置 = "../../data/tags.json"
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
        "seed":0,"尺寸":"随机","采样":0,"cfg":0,"smea":0}
    asyncio.run(api.批量随机生成图片(**参数))

# "角色":{
#     "1":"星野",
#     "2":"七七",
#     "3":"小泽",
#     "4":"叶晨",
#     "5":"苏玄",
#     "6":"叶天命",
#     "7":"洪武大帝",
#     "8":"皇太极"
# },
# "画风": {
#     "1":"写实",
#     "2":"动漫",
#     "3":"可爱",
#     "4":"复古",
#     "5":"抽象",
# },
# "质量":"非常好","动作": {
#     "1":"站立"
#     , "2":"行走"
#     , "3":"跳跃"
#     , "4":"坐下"
#     , "5":"起飞"
# },
# userdata=asyncio.run(api.api_get_user_data())
    #
    # logger.info(userdata)

    # dianshu=asyncio.run(api.api_dianshu())
    # logger.info(dianshu)

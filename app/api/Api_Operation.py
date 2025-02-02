import asyncio
import json
import os
import random
import re
import sys
import time
import tracemalloc
from datetime import datetime

from humanfriendly.terminal import output

from app import logger
from app import 保存序号和图片
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
        self.默认root_dir=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.root_dir=kwargs.get("root_dir",self.默认root_dir)
        self.__token=kwargs.get("__token","1211113")
        self.环境=kwargs.get("环境","测试")# 测试，正式，代理
        self.保存路径=kwargs.get("保存路径",f"{self.root_dir}/dev_img/")

        self.序号实例=保存序号和图片(f"{self.root_dir}/data/序号.json")
        # self.批量生成=kwargs.get("批量生成",False)
        # self.debug = kwargs.get("debug", False)

        super().__init__(__token=self.__token,环境=self.环境)
        self.json_data=json.load(open(f"{self.root_dir}/data/data.json", "r", encoding="utf-8"))
        self.gi_json_data=self.json_data.get("Generate_Image",{}).get("v3",{})
        self.放大_json=self.json_data.get("upscale",{})
        if not self.gi_json_data:
            logger.error("data.json中Generate_Image.v3为空")
            sys.exit()
        if not self.放大_json:
            logger.error("data.json中upscale为空")
            sys.exit()
        #self.序号实例=Counter(f"{root_dir}data/序号.json")






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
        点数数据=await self.api_dianshu()
        # 无限生成状态=点数数据["perks"]["unlimitedImageGeneration"]
        无限生成状态=点数数据.get("perks",{}).get("unlimitedImageGeneration",False)
        if not 无限生成状态:
            logger.warning( f"无限生成状态为：{无限生成状态}")
            logger.error( f"无限生成状态为：{无限生成状态}")
            return {"status": "error", "message": "无限生成状态为：False"}
        logger.info(f"无限生成状态为：{点数数据['perks']['unlimitedImageGeneration']}")
        图片序号=self.序号实例.load_counter()
        图片序号 += 1
        # logger.info(f"图片序号:{图片序号}")
        try:

            img_data=await self.api_generate_image(self.gi_json_data)
        except Exception as e:
            logger.error(f"生成图片时出错: {e}")
            return {"status": "error", "message": f"生成图片时出错: {e}", "序号": 图片序号}


        标准可读_时间= datetime.now().strftime('%H-%M-%S')
        年月日_日期 = datetime.now().strftime('%Y年%m月%d日')
        文件名 = f"{图片序号:03d}--{年月日_日期}--{标准可读_时间}--{种子}.png"
        try:
            保存路径=os.path.join(self.保存路径,年月日_日期)
            返回=self.序号实例.save_image(img_data,保存路径, 文件名)
        except Exception as e:
            logger.error(f"保存图片时出错: {e}")
            return {"status": "error", "message": f"保存图片时出错: {e}", "序号": 图片序号}


        self.序号实例.image_counter=图片序号
        # logger.info(f"新图片序号:{图片序号}")
        self.序号实例.save_counter()
        return {"status": "success", "message": "图片保存成功", "图片保存路径":返回.get("保存路径", "111111") ,"序号": 图片序号}

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
        角色是否可无 = 接收参数.get('角色是否可无', False)
        是否指定画风 = 接收参数.get('是否指定画风', False)
        #注固定类参数 值可以为 false和 数字 “数字位你需要固定的提示词在tags的序号，如果画风输入为artist文件则固定的是画师 数字为画师在artist。json的序号
        是否指定角色 = 接收参数.get('是否指定角色', False)
        #print(f"指定角色为：{是否指定角色}")
        #print(f"指定角色类型为：{type(是否指定角色)}")
        是否指定动作 = 接收参数.get('是否指定动作', False)
        角色获取方式 = 接收参数.get('角色获取方式', '随机')
        动作获取方式 = 接收参数.get('动作获取方式', '随机')
        画风获取方式 = 接收参数.get('动作获取方式', '随机')#如果输入为 artist文件 则指定无效
        是否随机组合画师=接收参数.get('是否随机组合画师',False)
        if 是否随机组合画师:
            提示词生成器实例=提示词生成器(角色=角色,质量=质量,动作=动作,角色是否可无=角色是否可无,角色获取方式=角色获取方式,动作获取方式=动作获取方式,画风获取方式=画风获取方式,root_dir=self.root_dir, 是否指定画风=是否指定画风,是否指定角色=是否指定角色,是否指定动作=是否指定动作)
        else:
            提示词生成器实例=提示词生成器(角色=角色,画风=画风,质量=质量,动作=动作,角色是否可无=角色是否可无,角色获取方式=角色获取方式,动作获取方式=动作获取方式,画风获取方式=画风获取方式,root_dir=self.root_dir, 是否指定画风=是否指定画风,是否指定角色=是否指定角色,是否指定动作=是否指定动作)
        参数生成器实例=参数生成器(尺寸=尺寸,采样=采样,提示词引导系数=cfg,种子=接收种子,smea=smea)

        返回=await self.api_get_user_data()
        if 返回["状态"] == "失败":
            logger.error(返回)
            return 返回
        用户数据=返回["响应体"]
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
            prompt = 提示词生成器实例.提示词组合()
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

            logger.info(f"main-generate_img_提示词为:{prompt}")
            # 调用API生成图像
            返回=await self.单次生成图片(**传递参数字典)
            if 返回["status"] == "success":
                logger.info(返回)
                pass
            else:
                pass
                logger.error(返回)
                return 返回


            time.sleep(1)

    async def 无限生成图片(self,**接收参数):
        角色=接收参数["角色"]
        画风=接收参数["画风"]
        质量=接收参数["质量"]
        动作=接收参数["动作"]
        接收种子=接收参数["seed"]
        尺寸=接收参数["尺寸"]
        采样=接收参数["采样"]
        cfg=接收参数["cfg"]
        smea=接收参数["smea"]
        角色是否可无 = 接收参数.get('角色是否可无', False)
        是否指定画风 = 接收参数.get('是否指定画风', False)
        #注固定类参数 值可以为 false和 数字 “数字位你需要固定的提示词在tags的序号，如果画风输入为artist文件则固定的是画师 数字为画师在artist。json的序号
        是否指定角色 = 接收参数.get('是否指定角色', False)
        #print(f"指定角色为：{是否指定角色}")
        #print(f"指定角色类型为：{type(是否指定角色)}")
        是否指定动作 = 接收参数.get('是否指定动作', False)
        角色获取方式 = 接收参数.get('角色获取方式', '随机')
        动作获取方式 = 接收参数.get('动作获取方式', '随机')
        画风获取方式 = 接收参数.get('动作获取方式', '随机')#如果输入为 artist文件 则指定无效
        是否随机组合画师=接收参数.get('是否随机组合画师',False)
        if 是否随机组合画师:
            提示词生成器实例=提示词生成器(角色=角色,质量=质量,动作=动作,角色是否可无=角色是否可无,角色获取方式=角色获取方式,动作获取方式=动作获取方式,画风获取方式=画风获取方式,root_dir=self.root_dir, 是否指定画风=是否指定画风,是否指定角色=是否指定角色,是否指定动作=是否指定动作)
        else:
            提示词生成器实例=提示词生成器(角色=角色,画风=画风,质量=质量,动作=动作,角色是否可无=角色是否可无,角色获取方式=角色获取方式,动作获取方式=动作获取方式,画风获取方式=画风获取方式,root_dir=self.root_dir, 是否指定画风=是否指定画风,是否指定角色=是否指定角色,是否指定动作=是否指定动作)
        参数生成器实例=参数生成器(尺寸=尺寸,采样=采样,提示词引导系数=cfg,种子=接收种子,smea=smea)
        返回=await self.api_get_user_data()
        if 返回["状态"] == "失败":
            logger.error(返回)
            return 返回
        用户数据=返回["响应体"]
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
        while True:
            # 每次循环重新生成prompt
            prompt = 提示词生成器实例.提示词组合()
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



            logger.info(f"提示词为:{prompt}")
            # 调用API生成图像
            返回=await self.单次生成图片(**传递参数字典)
            # logger.info(返回)
            if 返回["status"] == "success":
                logger.info(f"序号为：{返回['序号']}的图片生成成功")
                logger.info(返回)
                pass
            else:
                if 返回.get("序号"):
                    logger.error(f"序号为：{返回['序号']}的图片生成失败")

                logger.error(返回)
                return 返回

            delay_seconds = random.randint(5, 40)  # 生成 1 到 60 之间的随机整数
            logger.info(f"等待{delay_seconds}秒进行下一次生成")
            time.sleep(delay_seconds)


    ###其他操作区
    async def 单次放大图片(self,**接收参数):
        放大倍数=接收参数.get("放大倍数",4)
        宽度=接收参数.get("宽度",832)
        高度=接收参数.get("高度",1216)
        图片base64数据=接收参数.get("图片base64数据","")
        文件名=接收参数.get("文件名","")
        保存路径=接收参数.get("保存路径","")
        try:
            返回数据=await self.api_图片放大({
            "image":图片base64数据,
            "width":宽度,
            "height":高度,
            "scale":放大倍数
        })
        except Exception as e:
            logger.error(f"放大图片失败，错误信息为：{e}")
            return {"status":"error","message":f"放大图片失败，错误信息为：{e}"}

        try:
            返回=self.序号实例.save_image(返回数据,保存路径,文件名)
            #logger.info(返回)
            return 返回
        except Exception as e:
            logger.error(f"保存图片失败，错误信息为：{e}")
            return {"状态":"错误","message":f"保存图片失败，错误信息为：{e}"}
    async def 批量放大图片(self, **接收参数):
        """
        批量放大图片，并为每个日期目录添加统计信息。

        Args:
            接收参数: 包含以下键的字典：
                放大倍数 (int, optional): 放大倍数，默认为 4。
                图片所在目录 (str, optional): 图片所在的根目录，默认为空字符串。
                保存路径 (str, optional): 放大后图片保存的根目录，默认为空字符串。
                成功后是否删除原图 (bool, optional): 是否在成功放大后删除原图，默认为 False。

        Returns:
            dict: 包含操作状态和消息的字典。
        """
        #函数内导入
        import base64
        import re
        import os
        import json
        from PIL import Image
        #参数
        点数数据=await self.api_dianshu()
        # logger.info(f"点数数据为：{点数数据}")
        点数=点数数据.get("trainingStepsLeft",{}).get("fixedTrainingStepsLeft",0)+点数数据.get("trainingStepsLeft",{}).get("purchasedTrainingSteps",0)
        logger.info(f"初始点数为：{点数}")
        if 点数 < 7:
            logger.error("点数不足，无法进行批量放大操作。")
            return {"状态": "错误", "message": "点数不足，无法进行批量放大操作。"}

        放大倍数 = 接收参数.get("放大倍数", 4)
        图片所在目录 = 接收参数.get("图片所在目录", "")
        初始保存路径 = 接收参数.get("保存路径", "")
        成功后是否删除原图 = 接收参数.get("成功后是否删除原图", False)

        logger.info(f"开始批量放大图片，图片所在目录：{图片所在目录}，保存路径：{初始保存路径}，放大倍数：{放大倍数}，成功后是否删除原图：{成功后是否删除原图}")

        if not 图片所在目录:
            logger.error("图片所在目录为空，无法进行批量放大操作。")
            return {"状态": "错误", "message": "图片所在目录为空，无法进行批量放大操作。"}

        try:
            all_stats = {}  # 用于存储所有日期目录的统计信息
            for root, dirs, files in os.walk(图片所在目录):
                当前目录名称 = os.path.basename(root)
                date_match = re.search(r'\d{4}-+\d{1,2}-+\d{1,2}', 当前目录名称)

                if date_match:
                    logger.info(f"正在处理日期目录：{当前目录名称}")
                    date_str = date_match.group(0)
                    stats = {"成功数量": 0, "错误数量": 0}  # 初始化当前日期目录的统计信息
                    all_stats[date_str] = stats  # 将当前日期目录的统计信息添加到总统计信息中
                    del_info = {}  # 用于存储当前目录删除图片的信息，格式为 {父目录名称: {文件名1, 文件名2, ...}}
                    for file in files:
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):

                            file_path = os.path.join(root, file)
                            logger.debug(f"正在处理文件：{file_path}")

                            try:
                                with Image.open(file_path) as img: # 使用 with 语句打开图片，确保资源释放
                                    图片宽度 = img.width
                                    图片高度 = img.height
                                    with open(file_path, "rb") as image_file:
                                        图片的父目录名称 = os.path.basename(os.path.dirname(file_path))
                                        最终保存路径 = os.path.join(初始保存路径, 图片的父目录名称)
                                        图片文件名 = os.path.basename(file)
                                        图片字节数据 = image_file.read()
                                        图片base64数据 = base64.b64encode(图片字节数据).decode('utf-8')
                                del_json_path = os.path.join(初始保存路径, "del.json")
                                if os.path.exists(del_json_path):
                                    with open(del_json_path, "r", encoding="utf-8") as f:

                                        try:
                                            del_data = json.load(f)
                                        except json.JSONDecodeError:
                                            del_data = {}  # 如果文件为空或不是有效的 JSON，则初始化为空字典
                                else:
                                    del_data = {}
                                logger.info(f"图片的父目录名称:{图片的父目录名称},图片文件名:{图片文件名}")
                                if 图片的父目录名称 in del_data and 图片文件名 in del_data[图片的父目录名称]:
                                    图片测试保持路径= os.path.join(初始保存路径, 图片的父目录名称, 图片文件名)
                                    logger.info(f"图片测试保持路径:{图片测试保持路径}")
                                    if os .path.exists(图片测试保持路径) and os.path.getsize(图片测试保持路径) > 1024*100 :
                                        logger.info(f"图片 {图片文件名} 已存在，跳过放大操作。")
                                        continue
                                输入参数 = {
                                    "放大倍数": 放大倍数,
                                    "宽度": 图片宽度,
                                    "高度": 图片高度,
                                    "图片base64数据": 图片base64数据,
                                    "文件名": 图片文件名,
                                    "保存路径": 最终保存路径,
                                }
                                # logger.info(f"输入参数为：{输入参数}")

                                返回 = await self.单次放大图片(**输入参数)  # 注释掉，因为你没有提供单次放大图片的实现
                                点数数据=await self.api_dianshu()
                                # logger.info(f"点数数据为：{点数数据}")
                                点数=点数数据.get("trainingStepsLeft",{}).get("fixedTrainingStepsLeft",0)+点数数据.get("trainingStepsLeft",{}).get("purchasedTrainingSteps",0)

                                logger.info(f"当前图片放大后的剩余点数：{点数}")
                                logger.info(f"返回数据为：{返回}")

                                if 返回["状态"] == "成功" and 返回.get("保存路径", ""):
                                    保存的图片 = 返回.get("保存路径", "")
                                    if os.path.exists(保存的图片):
                                        if 成功后是否删除原图:
                                            try:

                                                os.remove(file_path)  # 实际删除操作，这里注释掉方便测试
                                                logger.info(f"删除原图片成功，文件路径为：{file_path}")


                                                try:




                                                    if 图片的父目录名称 in del_data:
                                                        if 图片文件名 not in del_data[图片的父目录名称]:
                                                            del_data[图片的父目录名称].append(图片文件名)

                                                    else:
                                                        del_data[图片的父目录名称] = [图片文件名]
                                                    # logger.info(f"删除文件信息：{del_data}")
                                                    with open(del_json_path, "w", encoding="utf-8") as f:
                                                        json.dump(del_data, f, ensure_ascii=False, indent=4)

                                                        # os.makedirs(os.path.dirname(del_json_path), exist_ok=True)
                                                        # del_data = {图片的父目录名称: [图片文件名]}
                                                        # with open(del_json_path, "w", encoding="utf-8") as f:
                                                        #     json.dump(del_data, f, ensure_ascii=False, indent=4)
                                                    logger.info(f"删除信息已写入：{del_json_path}")
                                                except Exception as e:
                                                    logger.error(f"写入 del.json 失败：{del_json_path}，错误信息：{e}")
                                            except  Exception as e:
                                                logger.error(f"删除图片失败：{file_path}，错误信息：{e}")

                                # logger.info(f"图片的父目录为：{图片的父目录名称}，图片文件名为：{图片文件名}，图片宽度为：{图片宽度}，图片高度为：{图片高度}")
                                stats["成功数量"] += 1  # 成功处理一张图片，计数加一
                                # input("已暂停输入任意继续")
                            except FileNotFoundError:
                                logger.error(f"文件未找到：{file_path}")
                                stats["错误数量"] += 1
                            except Exception as e:
                                logger.error(f"放大图片失败，文件：{file_path}，错误信息：{e}")
                                stats["错误数量"] += 1  # 处理图片失败，错误计数加一


            logger.info(f"批量放大图片完成，统计信息：{all_stats}")
            logger.info(f"批量放大图片完成，总数目录为 {len(all_stats)}，总成功数量为 {sum(stats['成功数量'] for stats in all_stats.values())}，总错误数量为 {sum(stats['错误数量'] for stats in all_stats.values())}")

            return {"状态": "成功", "message": "批量放大图片完成", "statistics": all_stats}

        except Exception as e:
            logger.error(f"批量放大图片失败，错误信息：{e}")
            return {"状态": "错误", "message": f"批量放大图片失败，错误信息：{e}"}





#放大测试


if __name__ == '__main__':
       输入路径=r"D:\xm\nai3_auto_generate_image\input\dev_img"
       放大倍数=4
       保存路径=r"D:\xm\nai3_auto_generate_image\output\dev_放大2"
       api=ApiOperation(__token="123",环境="测试",保存路径=r"../../dev_img",批量生成=True,生成次数=10)
       # api=ApiOperation(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj",环境="正式",保存路径=r"../../dev_img",生成次数=10)
       asyncio.run(api.批量放大图片(**{"放大倍数":放大倍数,"图片所在目录":输入路径,"保存路径":保存路径,"成功后是否删除原图":True}))



# if __name__ == '__main__':
#
#     #api=ApiOperation(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj",test=False,保存路径=r"../../dev_img",批量生成=True,生成次数=10)
#     api=ApiOperation(__token="1123",环境="测试",保存路径=r"../../dev_img",批量生成=True,生成次数=10)
#     logger.info("开始生成图片")
#     tags位置 = "../../data/tags.json"
#     # 检查文件是否存在
#     tags_file_path = tags位置
#     default_tags = {
#         "__注释": "角色：为你喜欢的角色格式如下，画风：为艺术家组合同下，动作：为除开角色画风的其余部分包括服装动作等以及需要叠加覆盖的人物特征，质量：指定生成图片质量的一般不需要改",
#         "角色": {
#             "1": "{yaoyao (genshin impact)}",
#             "2": "bailu (honkai: star rail)"
#         },
#         "画风": {
#             "1": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]",
#             "2": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]"
#         },
#         "动作": {
#             "1": "1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,green eyes,{loli},ahoge,looking at viewer,standing on one leg,blush,standing,parted lips,leg up, cowboy shot, {{close-up}}, ,no_panties,tuncensored,pussy ,{Sneakers},{{Pussy object  insertion}},{sex},{anus},{Very thick carrot},{Orgasm}, {shivering},{bedroom},Full body portrait",
#             "2": "1girl,loli,ass focus,(see-through,white pantyhose),side lying,looking at viewer,from below,{{Cat ears}},{sex},{nsfw},{no panties},Pussy, anus,{ Thick Tentacles}, {{Anal insertion}},{No tail},{{Tentacle anal insertion}},clothes_pull,"
#         },
#         "质量": "best quality, amazing quality, very aesthetic, absurdres"
#     }
#     if not os.path.exists(tags_file_path):
#         # 如果文件不存在，创建文件并写入默认数据
#         os.makedirs(os.path.dirname(tags_file_path), exist_ok=True)  # 确保目录存在
#         with open(tags_file_path, "w", encoding="utf-8") as file:
#             json.dump(default_tags, file, ensure_ascii=False, indent=4)
#         logger.warning(f"文件 {tags_file_path} 不存在，已创建并写入默认数据。")
#     # 读取文件内容
#     with open(tags_file_path, "r", encoding="utf-8") as file:
#         tags = json.load(file)
#         if json.dumps(tags, ensure_ascii=False, indent=4).strip() == json.dumps(default_tags, ensure_ascii=False,
#                                                                                 indent=4).strip():
#             logger.warning("检测到默认数据，请修改tags.json文件后启动，延时5秒关闭")
#             time.sleep(5)
#             sys.exit()
#
#     角色= tags['角色']
#     画风= tags['画风']
#     动作= tags['动作']
#     质量 =tags['质量']
#     参数={"角色":角色,
#            "画风":画风,
#            "质量":质量,
#            "动作":动作,
#         "seed":0,"尺寸":"随机","采样":0,"cfg":0,"smea":0,"是否随机组合画师":True}
#     asyncio.run(api.无限生成图片(**参数))


####库导入
import asyncio
import os
import sys
from typing import Dict, Any
import json
import aiohttp  # 添加aiohttp库

###环境变量设置

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../../"))


###项目模块导入

from app.utils.log_config import logger





class NovelAIAPI:
    _instance = None
    _lock = asyncio.Lock()  # 单例锁
    _lock_generate_image = asyncio.Lock()  # 限制generate_image方法的并发
    _lock_img_enlarge = asyncio.Lock()  # 限制img_enlarge方法的并发
    _lock_subscription = asyncio.Lock()  # 限制subscription方法的并发
    _lock_get_user_data = asyncio.Lock()
    _lock_api_请求= asyncio.Lock()

    def __new__(cls,*args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # cls._instance.__init__(*args, **kwargs)  # 这里调用会初始化两次
        return cls._instance

    def __init__(self, *args, **kwargs):
        """
        初始化API类，配置请求的头信息和常规参数。
        :param __token: 用户API Token，用于授权访问API
        """
        self.logger = logger
        self.__token = kwargs.get("__token", "1211113")
        self.环境 = kwargs.get("环境", "正式")
        self.debug = kwargs.get("debug", False)
        if self.debug:
            logger.level("DEBUG")

        logger.debug(f"令牌：{self.__token}, 环境：{self.环境}")

        # 定义不同环境的 API URL
        api_urls = {
            "测试": {
                "api_image": "http://127.0.0.1:2800/ai/generate-image",
                "api_user_data": "http://127.0.0.1:2800/user/data",
                "api_image_enlarge": "http://127.0.0.1:2800/ai/upscale",
                "api_subscription": "http://127.0.0.1:2800/user/subscription",
            },
            "代理": {
                "api_image": "https://nai-image-api.mrnf.xyz/ai/generate-image",
                "api_user_data": "https://nai-api.mrnf.xyz/user/data",
                "api_image_enlarge": "https://nai-api.mrnf.xyz/ai/upscale",
                "api_subscription": "https://nai-api.mrnf.xyz/user/subscription",
            },
            "正式": {
                "api_image": "https://image.novelai.net/ai/generate-image",
                "api_user_data": "https://api.novelai.net/user/data",
                "api_image_enlarge": "https://api.novelai.net/ai/upscale",
                "api_subscription": "https://api.novelai.net/user/subscription",
            },
        }

        # 设置默认环境为测试
        default_env = "测试"

        # 根据环境参数选择对应的 API URL
        env_config = api_urls.get(self.环境, api_urls[default_env])
        if self.环境 not in api_urls:
            logger.info(f"当前环境 '{self.环境}' 未知，使用默认环境 '{default_env}' 配置")
        else:
            logger.info(f"当前环境：{self.环境}模式")

        self.api_image = env_config["api_image"]
        self.api_user_data = env_config["api_user_data"]
        self.api_image_enlarge = env_config["api_image_enlarge"]
        self.api_subscription = env_config["api_subscription"]

        logger.info(f"{'-' * 50}")

        # 配置请求头
        self.headers = {
            "authorization": f"Bearer {self.__token}",
            "authority": "api.novelai.net",
            "Origin": "https://novelai.net",
            "Referer": "https://novelai.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Content-Type": "application/json",
        }



    async def api_请求(self, 请求信息: Dict[str, Any], debug: bool = False) -> Dict[str, Any]:
        """
        接收请求信息并发送请求，添加重试机制，并统一返回格式，包含完整的响应对象。

        Args:
            请求信息: 包含请求信息的字典，例如 {"请求方法": "GET", "请求url": "...", "headers": {...}, "data": {...}, "json": {...}}
            debug: 是否开启调试模式，输出调试信息。

        Returns:
            Dict[str, Any]: 包含请求状态、消息、数据和完整响应对象的字典。
        """
        # logger.info(f"debug={debug}")

        async with self._lock_api_请求:
            最大重试次数 = 3
            重试次数 = 0
            重试延迟 = 1

            while 重试次数 <= 最大重试次数:
                try:
                    请求方法 = 请求信息.get("请求方法", "GET")
                    请求url = 请求信息.get("请求url")
                    请求头 = self.headers
                    请求数据 = 请求信息.get("请求数据", None)
                    请求json = 请求信息.get("请求json", None)
                    请求查询信息 = 请求信息.get("请求查询信息", None)

                    if not 请求url:
                        return {"状态": "失败", "消息": "请求url为空，请检查请求信息", "数据": None, "response": None}


                    self.logger.debug(f"请求方法: {请求方法}, 请求URL: {请求url}, headers: {请求头}, data: {请求数据}, json: {请求json}, params: {请求查询信息}")

                    async with aiohttp.ClientSession() as session:
                        async with session.request(
                                method=请求方法,
                                url=请求url,
                                headers=请求头,
                                data=请求数据,
                                json=请求json,
                                params=请求查询信息,
                        ) as response:
                            if debug:
                                self.logger.debug(f"响应状态码: {response.status}")
                            response.raise_for_status()  # 如果状态码不是 2xx，则抛出异常

                            # 读取响应体，并根据 Content-Type 选择合适的处理方式
                            content_type = response.headers.get('Content-Type', '').lower()
                            # logger.info(f"content_type={content_type}")
                            if content_type.startswith('application/json'):
                                # logger.info(f"这是json-if")
                                # logger.info(f"原始响应体={response.text}")
                                response_body = await response.json()
                                # logger.info(f"response_body={response_body}")

                            elif content_type.startswith('text/'):
                                # logger.info(f"这是text-if")
                                response_body = await response.text()

                            else:
                                # logger.info(f"这是else-if")
                                response_body = await response.read()

                            return {
                                "状态": "成功",
                                "消息": "请求成功",
                                "状态码": response.status,
                                "响应体": response_body,
                                "响应体类型": content_type
                            }

                except aiohttp.ClientError as e:

                    self.logger.debug(f"请求失败 (重试 {重试次数 + 1}/{最大重试次数}): {e}")
                    重试次数 += 1
                    if 重试次数 <= 最大重试次数:
                        await asyncio.sleep(重试延迟)
                    else:
                        self.logger.error(f"所有重试都失败: {e}")
                        return {"状态": "失败", "消息": f"所有重试都失败: {e}", "数据": None, "response": None}
                except Exception as e:
                    self.logger.error(f"请求过程中发生未知错误: {e}")
                    return {"状态": "失败", "消息": f"请求过程中发生未知错误: {e}", "数据": None, "response": None}


    async def api_generate_image(self, json_payload: dict):
            """
            根据传入的参数生成图像，并返回原始的ZIP文件响应体。
            :param debug:
            :param json_payload: 请求的参数字典，包含所有生成图像所需的配置
            :return: 如果成功，返回图像生成的ZIP文件内容；否则返回None
            """
            async with self._lock_generate_image:  # 使用锁限制并发
                请求信息= {
                    "请求方法": "POST",
                    "请求url": self.api_image,
                    "请求头": self.headers,
                    "请求json": json_payload,
                }
                返回= await self.api_请求(请求信息= 请求信息, debug=True)

                return 返回.get("响应体",None)


    async def api_get_user_data(self):
        """
        获取用户的相关数据（如账户信息、使用情况等）。
        :return: 如果成功，返回用户数据；否则返回None
        """
        async with self._lock_get_user_data:  # 使用锁限制并发
            请求信息= {
                "请求方法": "GET",
                "请求url": self.api_user_data,
                "请求头": self.headers,
            }

            返回=await self.api_请求(请求信息= 请求信息,debug=True)
            return  返回
    async def api_dianshu(self):
        """
        获取用户订阅情况。
        :return: 如果成功，返回订阅数据；否则返回None
        """
        async with self._lock_subscription:  # 使用锁限制并发
            请求信息= {
                "请求方法": "GET",
                "请求url": self.api_subscription,
                "请求头": self.headers,
            }
            返回=await self.api_请求(请求信息= 请求信息, debug=True)
            return 返回.get("响应体",None)
    async def api_img_enlarge(self, json_payload: dict):
        """
        图片放大功能
        :param json_payload: 请求的参数字典，包含图像数据和放大比例等信息
        :return: 返回放大后的图像数据
        """
        async with self._lock_img_enlarge:  # 使用锁限制并发
            请求信息= {
                "请求方法": "POST",
                "请求url": self.api_image_enlarge,
                "请求头": self.headers,
                "请求json": json_payload,
            }
            返回=await self.api_请求(请求信息= 请求信息, debug=True)
            return 返回.get("响应体",None)


# 使用示例：
if __name__ == "__main__":
    # #api=NovelAIAPI(__token="123")
    api实例 = NovelAIAPI(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj")
    json=  {
        "input": "1girl",  # 用户提供的生成图像提示词
        "model": "nai-diffusion-3",  # 使用的模型版本
        "action": "generate",  # 动作类型，生成图像
        "parameters": {
            "width": 832,  # 默认图像宽度（小图）
            "height": 1216,  # 默认图像高度（小图）
            "scale": 5,  # 细节比例，默认为5
            "sampler": "k_euler_ancestral",  # 默认采样器，使用欧拉采样器
            "steps": 28,  # 固定生成28步
            "seed": 0,  # 随机种子，0表示由API自动生成
            "n_samples": 1,  # 生成的图像数量
            "negative_prompt": "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], underwear",
            # 负面提示词
            "qualityToggle": True,  # 启用质量增强模式，以提高生成图像的质量。
            "sm": False,
            "sm_dyn": False,
            "dynamic_thresholding": False,  # 关闭动态阈值调整，保持固定的阈值。
            # 是否启用旧版模型。如果禁用，通常会使用新版本的模型。
            "legacy": False,  # 禁用旧版模型。
            # 是否将原始图像添加到输出中。如果启用，返回的图像中将包括原始图像。
            # "add_original_image": True,  # 启用此选项将原始输入图像也包含在返回数据中。

            # 配置重缩放参数。通常用于图像的尺寸调整。
            "cfg_rescale": 0,  # 配置重缩放因子，这里设置为0表示不做任何尺寸调整。
            "controlnet_strength": 1,

            # 噪声调度的算法，用于控制生成过程中噪声的减少方式。
            "noise_schedule": "karras",  # 使用的噪声调度算法。`karras`算法通常用于优化图像的清晰度。

            # 是否使用旧版v3扩展。设置为false表示不使用旧版的扩展。
            "legacy_v3_extend": False,  # 禁用旧版扩展。

            # 是否跳过配置的Sigma阈值。这个通常用于配置阈值是否跳过。
            "skip_cfg_above_sigma": None,  # 跳过高于Sigma阈值的配置，这里没有设置特定的Sigma值。

        },}
    #
    #
    #
    #
    #
    #     # imgdata=asyncio.run(api实例.api_generate_image(json))
    # imgdata=api实例.aaa(json)
    # save_image(imgdata, "./", "111.png")

    # usee_data = asyncio.run(api实例.api_get_user_data())
    # dianshu_data = asyncio.run(api实例.api_dianshu())
    # async def api_init():
    #     api实例 = NovelAIAPI(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj")
    #     usee_data = await api实例.api_get_user_data()
    #     logger.info(f"用户数据: {usee_data}")
    #     wuxianshengcheng = usee_data["subscription"]["perks"]["unlimitedImageGeneration"]
    #     dingyue = usee_data["subscription"]["tier"]
    #     print(f"订阅：{dingyue}")
    #     print(f"无限制生成：{wuxianshengcheng}")
    #     if not wuxianshengcheng:
    #         print("生成需要付费")
    #         exit()
    #     if dingyue == 0:
    #         print("订阅没了")
    #         exit()
    #     dianshu_data = await api实例.api_dianshu()
    #     logger.info(f"点数数据: {dianshu_data}")
    #     dianshu = dianshu_data["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    #     print(f"初始化获取点数：{dianshu}")
    #     print("-" * 50)
    # asyncio.run(api_init())
    # #
    # #
    # async def fangda(img_path, api, save_path):
    #     dianshu_data = await api.subscription()
    #
    #     # 获取新的点数
    #     dianshu = dianshu_data["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    #     print(f"操作前点数：{dianshu}")
    #
    #     # 打开图片并获取宽度和高度
    #     with Image.open(img_path) as img:
    #         width, height = img.size
    #
    #     # 将图片转换为Base64编码
    #     with open(img_path, "rb") as image_file:
    #         image_data = image_file.read()
    #         image_base64 = base64.b64encode(image_data).decode("utf-8")  # 转换为Base64字符串
    #
    #     # 构造JSON数据
    #     json = {
    #         "image": image_base64,  # Base64编码的图片数据
    #         "scale": 4,
    #         "width": width,
    #         "height": height
    #     }
    #
    #     # 假设有api对象可以调用img_enlarge方法
    #     image_data = await api.img_enlarge(json)
    #
    #     from save_img import save_image
    #     save_image(image_data, save_path, img_path=img_path)
    #
    #
    #     # 获取当前点数并比较
    #     dianshu1_data = await api.subscription()
    #
    #     # 获取新的点数
    #     dianshu1 = dianshu1_data["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    #     print(f"操作后点数：{dianshu1}")
    #     if dianshu1 == dianshu:
    #         print("点数不变")
    #     else:
    #         print("点数变化")
    #         print(f"点数变化从：{dianshu}变为{dianshu1}")
    #
    #
    # async def process_images(input_dir, include_subdirectories=False, save_path=None, api=None):
    #     if save_path is None:
    #         save_path = os.path.join(input_dir, "放大输出")
    #     """
    #     遍历指定目录下的图片文件，并依次处理每张图片
    #     :param input_dir: 输入目录路径
    #     :param include_subdirectories: 是否遍历子目录，默认为不遍历
    #     """
    #     if include_subdirectories:
    #         # 如果要遍历子目录，使用 Path.rglob()
    #         image_files = Path(input_dir).rglob('*')  # 遍历所有子目录及文件
    #     else:
    #         # 如果不遍历子目录，直接列出目录中的文件
    #         image_files = os.listdir(input_dir)
    #
    #     # 获取目录下所有图片文件
    #     image_tasks = []
    #     for img_file in image_files:
    #         if isinstance(img_file, Path):
    #             img_path = img_file
    #         else:
    #             img_path = os.path.join(input_dir, img_file)
    #
    #         # 判断文件是否是图片（根据扩展名判断）
    #         if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
    #             print(f"发现图片文件: {img_path}")
    #             image_tasks.append(fangda(img_path, api, save_path))
    #
    #     await asyncio.gather(*image_tasks)
    #
    # api= asyncio.run(api_init())
    # dianshu_data = asyncio.run(api.subscription())
    # dianshu = dianshu_data["trainingStepsLeft"]["fixedTrainingStepsLeft"]
    # print(f"操作前点数：{dianshu}")
    # #process_images(r"W:\放大输入", include_subdirectories=False,api)
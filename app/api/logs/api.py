
import os
import sys

import requests

from app.utils.utils import save_image

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../../"))

import asyncio

from requests.exceptions import SSLError, RequestException
from app.utils.log_config import logger
import aiohttp  # 添加aiohttp库


class NovelAIAPI:
    _instance = None
    _lock = asyncio.Lock()  # 单例锁
    _lock_generate_image = asyncio.Lock()  # 限制generate_image方法的并发
    _lock_img_enlarge = asyncio.Lock()  # 限制img_enlarge方法的并发
    _lock_subscription = asyncio.Lock()  # 限制subscription方法的并发
    _lock_get_user_data = asyncio.Lock()

    def __new__(cls,*args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # cls._instance.__init__(*args, **kwargs)  # 调用初始化函数
        return cls._instance

    def __init__(self, *args, **kwargs):

        """
        初始化API类，配置请求的头信息和常规参数。
        :param __token: 用户API Token，用于授权访问API
        """



        self.__token = kwargs.get("__token","1211113")
        self.test = kwargs.get("test",False)
        logger.debug(f"令牌：{self.__token},测试：{self.test}")
        if self.test == True:

            self.api_image = "http://127.0.0.1:2800/ai/generate-image"  # 图像生成API URL
            self.api_user_data = "http://127.0.0.1:2800/user/data"  # 用户数据API URL
            self.api_image_enlarge = "http://127.0.0.1:2800/ai/upscale"
            self.api_subscription = "http://127.0.0.1:2800/user/subscription"
            logger.info(f"当前是测试模式")

        else:

            self.api_image = "https://image.novelai.net/ai/generate-image"  # 图像生成API URL
            self.api_user_data = "https://api.novelai.net/user/data"  # 用户数据API URL
            self.api_image_enlarge = "https://api.novelai.net/ai/upscale"
            self.api_subscription = "https://api.novelai.net/user/subscription"
            logger.info(f"当前是正式模式")

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
        #获取信息
        # self.用户数据= asyncio.run(self.get_user_data())
        # self.无限生成 =self.用户数据["subscription"]["perks"]["unlimitedImageGeneration"]
        # self.订阅 = self.用户数据["subscription"]["tier"]
        #
        #
        # logger.info(f"-----------------------------------------------------------")
        #
    def aaa(self,json):
        logger.info(f"-----------------------------------------------------------")
        logger.info(f"请求头：{self.headers}")
        logger.info(f"请求参数: {json}")
        response = requests.post(self.api_image, headers=self.headers, json=json, timeout=120)
        if response.status_code == 200:
            logger.info(f"图像生成成功，正在处理数据...")
            return response.content
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            logger.error(f"返回信息: {response.text}")
            return None

    async def api_generate_image(self, json_payload: dict,debug=False):
        """
        根据传入的参数生成图像，并返回原始的ZIP文件响应体。
        :param debug:
        :param json_payload: 请求的参数字典，包含所有生成图像所需的配置
        :return: 如果成功，返回图像生成的ZIP文件内容；否则返回None
        """
        async with self._lock_generate_image:  # 使用锁限制并发
            try:
                # 发起POST请求
                logger.info(f"-----------------------------------------------------------")
                logger.debug(f"请求参数: {json_payload}")
                logger.debug(f"请求头: {self.headers}")
                logger.debug(f"请求API: {self.api_image}")
                async with aiohttp.ClientSession() as session:  # 使用aiohttp进行异步请求
                    async with session.post(self.api_image, headers=self.headers, json=json_payload, timeout=120) as response:
                        # 检查请求结果
                        if response.status == 200:
                            logger.info(f"图像生成成功，正在处理数据...")
                            if debug:
                                try:
                                    encoding = response.charset or "utf-8"
                                    text = await response.text(encoding=encoding)
                                    logger.debug(f"返回信息: {text}")
                                    return type(text) # 返回 text 的类型
                                except UnicodeDecodeError as e:
                                    logger.warning(f"解码错误")
                                    data = await response.read()
                                    logger.debug(f"返回数据类型: {type(data)}")
                                    return data
                            return await response.read()
                        else:
                            logger.error(f"请求失败，状态码: {response.status}")
                            logger.error(f"返回信息: {await response.text()}")
            except (SSLError, RequestException) as e:
                logger.error(f"请求失败: {e}")
            except Exception as e:
                logger.error(f"请求失败: {e}")
            return None

    async def api_get_user_data(self):
        """
        获取用户的相关数据（如账户信息、使用情况等）。
        :return: 如果成功，返回用户数据；否则返回None
        """
        async with self._lock_get_user_data:  # 使用锁限制并发
            try:
                # 发起GET请求获取用户数据
                logger.info(f"请求用户数据...")

                async with aiohttp.ClientSession() as session:  # 使用aiohttp进行异步请求
                    async with session.get(self.api_user_data, headers=self.headers, timeout=120) as response:
                        # 检查请求结果
                        if response.status == 200:
                            logger.debug(f"用户数据获取成功，正在处理数据...")
                            return await response.json()  # 返回JSON格式的用户数据
                        else:
                            logger.error(f"请求失败，状态码: {response.status}")
                            logger.error(f"返回信息: {await response.text()}")
            except (SSLError, RequestException) as e:
                logger.error(f"请求失败: {e}")
            return None

    async def api_dianshu(self):
        """
        获取用户订阅情况。
        :return: 如果成功，返回订阅数据；否则返回None
        """
        async with self._lock_subscription:  # 使用锁限制并发
            try:
                async with aiohttp.ClientSession() as session:  # 使用aiohttp进行异步请求
                    async with session.get(self.api_subscription, headers=self.headers, timeout=120) as response:
                        if response.status == 200:
                            logger.debug(f"用户数据获取成功，正在处理数据...")
                            return await response.json()  # 返回JSON格式的用户数据
                        else:
                            logger.error(f"请求失败，状态码: {response.status}")
                            logger.error(f"返回信息: {await response.text()}")
            except (SSLError, RequestException) as e:
                logger.error(f"请求失败: {e}")
            except Exception as e:
                logger.error(f"捕获到异常: {e}")

    async def api_img_enlarge(self, json_payload: dict):
        """
        图片放大功能
        :param json_payload: 请求的参数字典，包含图像数据和放大比例等信息
        :return: 返回放大后的图像数据
        """
        async with self._lock_img_enlarge:  # 使用锁限制并发
            try:
                async with aiohttp.ClientSession() as session:  # 使用aiohttp进行异步请求
                    async with session.post(self.api_image_enlarge, headers=self.headers, json=json_payload, timeout=120) as response:
                        if response.status == 200:
                            return await response.read()  # 读取响应内容
                        else:
                            logger.error(f"请求失败，状态码: {response.status}")
                            logger.error(f"返回信息: {await response.text()}")
            except (SSLError, RequestException) as e:
                logger.error(f"请求失败: {e}")
            except Exception as e:
                logger.error(f"捕获到异常: {e}")


# 使用示例：
if __name__ == "__main__":
    # #api=NovelAIAPI(__token="123")
    api实例 = NovelAIAPI(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj")
    json={'input': '1girl',
          'model': 'nai-diffusion-3',
          'action': 'generate',
          'parameters':
              {'width': 832, 'height': 1216, 'scale': 5, 'sampler': 'dpm2msde', 'steps': 28, 'seed': 552266196, 'n_samples': 1, 'negative_prompt': 'lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract],', 'qualityToggle': True, 'sm': False, 'sm_dyn': False, 'dynamic_thresholding': False, 'legacy': False, 'cfg_rescale': 0, 'controlnet_strength': 1, 'noise_schedule': 'karras', 'legacy_v3_extend': False, 'skip_cfg_above_sigma': None, 'smea': False}}
    logger.info(type(json))
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
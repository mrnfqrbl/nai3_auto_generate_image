import os
import random
import zipfile
from datetime import datetime
from io import BytesIO

import requests
from requests.exceptions import SSLError, RequestException

from app.log_config import logger


class NovelAI_API:
    def __init__(self, __token: str, __negative_prompt: str = ""):
        """
        初始化API类，配置请求的头信息和常规参数。
        :param __token: 用户API Token，用于授权访问API
        :param __negative_prompt: 负面提示词，帮助避免生成不符合需求的图像内容
        """
        # 保存用户的Token
        self.__token = __token
        self.__negative_prompt = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], underwear"

        # NovelAI 图像生成 API 的 URL
        self.api = "https://image.novelai.net/ai/generate-image"
        # self.api="http://127.0.0.1:5000/ai/generate-image"

        # 配置请求头，包含授权信息、来源、用户代理等
        self.headers = {
            "authorization": f"Bearer {self.__token}",
            "authority": "api.novelai.net",
            "Origin": "https://novelai.net",
            "Referer": "https://novelai.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Content-Type": "application/json",
        }

        # 初始化请求的默认参数
        self.json = {
            "input": "",  # 用户提供的生成图像提示词
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

            },
        }

    def validate_parameters(self):
        """
        验证图像生成请求的参数是否符合 NovelAI 免费账户的限制。
        """
        max_steps = 28
        max_samples = 1

        # 检查步数
        if self.json["parameters"]["steps"] > max_steps:
            logger.warning(f"警告: 步数超过限制，最大步数为 {max_steps}，已自动调整。")
            self.json["parameters"]["steps"] = max_steps

        # 检查生成数量
        if self.json["parameters"]["n_samples"] > max_samples:
            logger.warning(f"警告: 生成数量超过限制，最大生成数量为 {max_samples}，已自动调整。")
            self.json["parameters"]["n_samples"] = max_samples

    def merge_negative_prompts(self, new_negative_prompt: str):
        """
        合并负面提示词，避免重复，并附加新的负面提示词到原来的上面。
        :param new_negative_prompt: 新的负面提示词
        """
        if new_negative_prompt and new_negative_prompt.strip():
            existing_negative_prompt = self.json["parameters"].get("negative_prompt", "")

            # 分割现有的负面提示词并去除空值
            existing_words = existing_negative_prompt.split(", ") if existing_negative_prompt else []

            # 分割新的负面提示词并去除空值
            new_words = new_negative_prompt.split(", ")

            # 合并原有负面提示词和新的负面提示词，并去除重复项
            merged_words = list(set(existing_words + new_words))

            # 更新负面提示词
            self.json["parameters"]["negative_prompt"] = ", ".join(merged_words)

    def set_image_proportions(self, proportional: str):
        """
        设置图像的宽度和高度，根据比例调整。
        :param proportional: 图像比例，可以是"竖向"、"横向"、"正方形"或"随机"
        """
        proportions = {
            "竖向": (832, 1216),
            "横向": (1216, 832),
            "正方形": (1024, 1024),
        }
        if proportional == "随机":
            proportional = random.choice(["竖向", "横向", "正方形"])

        width, height = proportions.get(proportional, (832, 1216))
        self.json["parameters"]["width"] = width
        self.json["parameters"]["height"] = height

    def set_sampler(self, sampling: str or int):
        """
        设置图像生成时的采样器。
        :param sampling: 采样器类型
        """
        samplers = {
            "ke": "k_euler",
            "kea": "k_euler_ancestral",
            "dmp++2s": "k_dpmpp_2s_ancestral",
            "dmp++2m": "k_dpmpp_2m_sde",
        }
        if isinstance(sampling, int):
            cy = samplers[random.choice(list(samplers.keys()))]
        if isinstance(sampling, str):
            cy = samplers.get(sampling, "k_euler")  # 防止key不存在，返回一个默认值
            logger.debug(f"使用采样器: {cy}")

        self.json["parameters"]["sampler"] = cy

    def set_smea(self, smea: int):
        """
        设置SMEA参数。
        :param smea: 0禁用，1启用，2随机
        """
        if smea == 1:
            self.json["parameters"]["sm"] = True
            logger.debug("启用SMEA")
        elif smea == 0:
            self.json["parameters"]["sm"] = False
            logger.debug("禁用SMEA")
        elif smea == 2:
            self.json["parameters"]["sm"] = random.choice([True, False])
        else:
            self.json["parameters"]["sm"] = False
            logger.debug("不支持的参数，已使用默认参数。")

    def set_cfg(self, cfg: int or str):
        if isinstance(cfg, int):
            self.json["parameters"]["scale"] = cfg
        if isinstance(cfg, str) and cfg == "随机":
            self.json["parameters"]["scale"] = random.randint(3, 10)
        else:
            self.json["parameters"]["scale"] = 5

    def generate_image(self, __prompt: str, seed: int = -1, proportional: str = "竖向", new_negative_prompt: str = "",
                       sampling: str = "", smea: int = 0, cfg: int or str = 6):
        """
        根据传入的提示词生成图像，并返回原始的ZIP文件响应体。
        :param __prompt: 生成图像的提示词
        :param seed: 随机种子，默认为-1，表示使用随机种子
        :param proportional: 图像比例，默认"竖向"
        :param new_negative_prompt: 负面提示词
        :param sampling: 采样器类型
        :param smea: 是否启用SMEA
        :return: 如果成功，返回图像生成的ZIP文件内容；否则返回None
        """
        self.json["input"] = __prompt

        # 设置随机种子
        self.json["parameters"]["seed"] = seed if seed != -1 else random.randint(0, 9999999999)

        # 合并负面提示词
        # self.merge_negative_prompts(new_negative_prompt)

        # 设置图像比例、采样器和SMEA
        self.set_image_proportions(proportional)
        self.set_sampler(sampling)
        self.set_smea(smea)
        self.set_cfg(cfg)

        # 验证并调整参数
        self.validate_parameters()

        try:
            # 发起POST请求
            logger.info(f"-----------------------------------------------------------")
            logger.debug(f"参数: {self.json}")
            logger.info(f"提示词: {self.json['input']}")
            logger.debug(f"请求头: {self.headers}")
            response = requests.post(self.api, headers=self.headers, json=self.json, timeout=120)

            # 检查请求结果
            if response.status_code == 200:
                logger.info(f"图像生成成功，正在处理数据...")
                response.content
                return response.content
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                logger.error(f"返回信息: {response.text}")
        except (SSLError, RequestException) as e:
            logger.error(f"请求失败: {e}")
        return None


if __name__ == "__main__":
    # 替换为你的API Token和负面提示词
    token = "pst-VH5WClfIdwAcfN5PDUJgflU1GGFTiKvtRpxBM2W1fEYnzSp99zNZcjip8npSJPut"
    negative_prompt = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], underwear"

    # 创建API实例
    api = NovelAI_API(token, negative_prompt)

    # 生成图像，使用代号选择采样器和尺寸
    prompt = "{ Griseo (Honkai Impact 3)},year 2023,artist: tianliang duohe fangdongye,[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99],1girl,loli,ass focus,(see-through,white pantyhose),side lying,looking at viewer,best quality, amazing quality, very aesthetic, absurdres,from below,{{Cat ears}},{sex},{nsfw},{no panties},Pussy, anus,{ Thick Tentacles}, {{Anal insertion}},{No tail},{{Tentacle anal insertion}},clothes_pull,{{Crying}}, {{scared}}, {{frowning}},{{{{very painful expression}}}},{extremely painful},{ejaculation}, {semen},Petite,petite stature"
    image_data = api.generate_image(prompt, seed=-1,proportional="竖向")  # 使用代号 1 （即 "euler" 采样器 和 "small" 尺寸）

    if image_data:
        logger.debug("图像生成成功，已返回原始ZIP文件内容！")
        # 确保目录存在
        img_directory = 'img'
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)
        # 创建 ZIP 文件对象
        # 创建 ZIP 文件对象
        with zipfile.ZipFile(BytesIO(image_data)) as zf:
            # 获取 ZIP 文件中的所有文件名
            file_names = zf.namelist()

            # 假设只有一个图片文件，取第一个文件名
            if file_names:
                image_filename = file_names[0]  # 取第一个图像文件名

                # 提取图像并保存为本地图片
                with zf.open(image_filename) as img_file:
                    img_data = img_file.read()

                    # 获取提示词中第一个逗号之前的部分
                    first_part = prompt.split(',')[0]  # 取第一个逗号之前的部分

                    # 获取当前时间并格式化为 YYYYMMDDHHMMSS
                    current_time = datetime.now().strftime('%Y%m%d%H%M%S')

                    # 设置保存的图像文件路径
                    image_filename = f"{first_part}_{current_time}.png"  # 使用提示词的前部分和时间生成文件名
                    image_path = os.path.join(img_directory, image_filename)

                    # 将图像数据保存为本地文件
                    with open(image_path, "wb") as f:
                        f.write(img_data)

                logger.info(f"图像已保存至: {image_path}")
            else:
                logger.error("ZIP文件中没有图像。")
    else:
        logger.error( "图像生成失败。")












# ... 已有导入 ...
import copy  # 导入 copy 模块
import json  # 导入 json 模块
import sys  # 导入 sys 模块
import traceback  # 导入 traceback 模块
from typing import List, Union
from urllib.parse import urljoin  # 导入 urljoin 函数

import requests  # 导入 requests 模块
from loguru import logger  # 添加日志模块


# 移除所有默认的 handlers
logger.remove()
logger.add(sys.stdout, level="DEBUG")  # 添加控制台输出，日志级别为INFO

logger.info(f"当前日志级别为: {logger.level}")  # 添加日志级别信息

def 全局异常处理函数(exctype, value, tb):
    """
    全局异常处理函数，捕获程序中未处理的异常并记录日志。
    """
    if exctype == UnicodeDecodeError:
        logger.error(f"捕获到编码错误: {value}")  # 记录编码错误
    else:
        logger.error(f"未处理的异常: {exctype.__name__} - {value}")  # 记录未处理的异常

    logger.error("堆栈信息:")  # 记录堆栈信息
    logger.error(''.join(traceback.format_exception(exctype, value, tb)))  # 记录完整的堆栈信息

    # 选择是否退出程序
    sys.exit(1)  # 或者使用 `exit(1)` 退出程序


# 注册全局异常处理
sys.excepthook = 全局异常处理函数


class ComfyUI_API:  # 类名改为 ComfyUI_API
    def __init__(self, 提示词生成器实例, 客户端id="", 根目录="./data"):  # 修改参数名
        """初始化API实例"""
        # 加载基础请求体（使用深拷贝避免原始数据被修改）
        # with open(f"{根目录}/data/comfyui_json.json", "r", encoding="utf-8") as f:  # 修改变量名
        with open(f"{根目录}/data/comfyui_lora_noobai.json", "r", encoding="utf-8") as f:  # 修改变量名
            self.请求体 = copy.deepcopy(json.load(f))  # 修改变量名

        self.提示词生成器实例 = 提示词生成器实例  # 修改变量名
        self.客户端id = 客户端id  # 修改变量名
        logger.debug("ComfyUI API实例初始化完成")  # 记录调试信息

    def 生成请求体副本(self,输入):
        """生成包含新提示词的请求体副本"""
        请求体副本 = copy.deepcopy(self.请求体)  # 修改变量名

        if 输入:
            输入_tag=输入
            提示词1 = self.提示词生成器实例.提示词组合(sd=True,**输入_tag)  # 修改变量名
            提示词2 = self.提示词生成器实例.提示词组合(sd=True,**输入_tag)  # 修改变量名

        # # 生成提示词对
        # 输入={
        #     "画风":"tsubasa tsubasa",
        #     "角色":r"laffey ii \\(azur lane\\),long_hair,white hair,red eyes,blue hairband, blue ribbon,"
        # }
        else:
            提示词1 = self.提示词生成器实例.提示词组合(sd=True,)  # 修改变量名
            提示词2 = self.提示词生成器实例.提示词组合(sd=True,)  # 修改变量名


        logger.info(f"生成提示词对 - i号:[{提示词1[:20]}...] 2号:[{提示词2[:20]}...]")  # 记录调试信息

        # 更新提示词节点
        def 更新节点(节点id, 内容):  # 修改函数名
            if "prompt" in 请求体副本 and 节点id in 请求体副本["prompt"]:  # 修改变量名
                请求体副本["prompt"][节点id]["inputs"]["text"] = 内容  # 修改变量名
            else:
                logger.warning(f"节点{节点id}不存在或结构异常")  # 记录警告信息

        更新节点("4", 提示词1)  # 负面提示词  # 修改函数名
        更新节点("98", 提示词2)  # 正面提示词  # 修改函数名
        请求体副本["client_id"] = self.客户端id  # 修改变量名
        ##额外信息
        ids = [4, 98]
        提示词 = [提示词1, 提示词2]  # 提示词列表

        for i, id in enumerate(ids):
            根路径 = ["extra_data", "extra_pnginfo", "workflow", "nodes", {"id": id}, "widgets_values", 0]
            请求体副本 = self.更新字典信息(根路径, 内容=提示词[i], 请求体副本=请求体副本)
        logger.debug("请求体副本生成完成")  # 记录调试信息
        return 请求体副本  # 修改变量名

    def 更新字典信息(self,节点路径: List[Union[str, int, dict]], 内容: any, 请求体副本: dict) -> dict:
        """
        更新字典信息，支持在列表中的字典中通过键值对搜索特定字典，并直接修改找到的字典。
        支持路径中包含数字，作为列表索引。

        Args:
            节点路径: 节点路径的列表，例如 ["a", "c", "d", {"id": 2}, "xxx"] 或 ["a", "c", "d", 0, "xxx"]。
                     如果路径中包含字典，则会在前一个列表里搜索匹配该字典的元素。
                     如果路径中包含数字，则将其作为列表索引进行访问。
            内容: 要设置的新内容。
            请求体副本: 要修改的请求体副本。

        Returns:
            返回包含更新后内容的完整相关结构的请求体副本。如果更新失败，则返回原始请求体副本。
        """

        请求体副本 = copy.deepcopy(请求体副本)  # 创建请求体副本，避免修改原始数据
        目标 = 请求体副本  # 修改变量名
        逆向路径 = []

        if isinstance(节点路径[-1], int):  # 修改变量名
            最终键 = 节点路径[-2]  # 修改变量名
            列表键 = 节点路径[-1]  # 修改变量名
        else:
            最终键 = 节点路径[-1]  # 修改变量名
            列表键 = None  # 修改变量名

        for i, key in enumerate(节点路径[:-1]):  # 修改变量名
            逆向路径.append((目标, key))
            # 根据当前target类型决定处理方式
            if isinstance(目标, dict):  # 修改变量名
                if isinstance(key, str):
                    # 字典键访问
                    if key not in 目标:  # 修改变量名
                        logger.warning(f"键 '{key}' 不存在于字典中")  # 记录警告信息
                        return 请求体副本
                    目标 = 目标[key]  # 修改变量名
                    logger.debug(f"搜索结果: {目标}")  # 记录调试信息
                elif isinstance(key, dict):
                    # 字典中的列表搜索（需明确指定列表字段）
                    if not isinstance(目标.get(key['field']), list):  # 修改变量名
                        logger.warning(f"字典中 '{key['field']}' 字段不是列表")  # 记录警告信息
                        return 请求体副本
                    目标 = self._搜索列表(目标[key['field']], key)  # 修改变量名
                    logger.debug(f"搜索结果: {目标}")  # 记录调试信息
                else:
                    logger.warning(f"字典类型target不支持 {type(key)} 类型路径")  # 记录警告信息
                    return 请求体副本

            elif isinstance(目标, list):  # 修改变量名
                if isinstance(key, int):
                    # 列表索引访问
                    if key >= len(目标):  # 修改变量名
                        logger.warning(f"列表索引 {key} 越界 (长度 {len(目标)})")  # 记录警告信息
                        return 请求体副本
                    目标 = 目标[key]  # 修改变量名
                    logger.debug(f"搜索结果: {目标}")  # 记录调试信息
                elif isinstance(key, dict):
                    # 列表中的字典搜索
                    目标 = self._搜索列表(目标, key)  # 修改变量名
                    logger.debug(f"搜索结果: {目标}")  # 记录调试信息

                else:
                    logger.warning(f"列表类型target不支持 {type(key)} 类型路径")  # 记录警告信息
                    return 请求体副本


            else:
                logger.warning(f"不支持的target类型 {type(目标)}")  # 记录警告信息
                return 请求体副本

        # 更新目标值
        if isinstance(目标, dict):  # 修改变量名
            目标[最终键] = 内容  # 修改变量名
        elif isinstance(目标, list):  # 修改变量名
            if isinstance(列表键, int):  # 修改变量名
                目标[列表键] = 内容  # 修改变量名
            else:
                logger.warning(f"列表键不是整数")  # 记录警告信息
                return 请求体副本
        else:
            logger.warning(f"目标类型 {type(目标)} 不支持更新")  # 记录警告信息
            return 请求体副本

        return 请求体副本


    def _搜索列表(self, lst, condition):  # 修改函数名
        """在列表中搜索匹配条件的字典"""
        if not isinstance(lst, list):
            logger.warning("搜索目标不是列表")  # 记录警告信息
            return None
        matches = [item for item in lst
                   if isinstance(item, dict) and all(item.get(k) == v for k, v in condition.items())]

        if len(matches) > 1:
            logger.warning(f"找到多个匹配项 {condition}")  # 记录警告信息
            return None
        if not matches:
            logger.warning(f"未找到匹配项 {condition}")  # 记录警告信息
            return None
        return matches[0]

    def 发送请求(self, url, 自定义请求体=None):  # 修改函数名
        """执行API请求并返回响应"""
        请求数据 = 自定义请求体 or self.请求体  # 修改变量名
        full_url = urljoin(url, "prompt")  # 修改变量名

        logger.debug(f"正在向 {full_url} 发送请求...")  # 记录调试信息
        response = requests.post(
            url=full_url,
            json=请求数据,  # 修改变量名
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()

        if response_data := response.json():
            if pid := response_data.get("prompt_id"):
                logger.success(f"请求成功 (Prompt ID: {pid})")  # 记录成功信息
            return response_data

        return None

    def 单次生成(self, url,输入):  # 修改函数名
        """单次生成任务"""

        return self.发送请求(url, self.生成请求体副本(输入))  # 修改函数名

    def 批量生成(self, url, 批量生成次数=2,输入:dict =None):  # 修改函数名
        """批量生成任务"""
        if not url:
            logger.warning("空URL")  # 记录警告信息
            return
        logger.info(f"启动批量生成任务 [次数:{批量生成次数} 客户端ID: {self.客户端id or '未指定'}]")  # 记录信息
        for i in range(1, 批量生成次数 + 1):
            logger.debug(f"正在进行第{i}次生成...")  # 记录调试信息
            self.单次生成(url,输入)  # 修改函数名

    def 多URL批量生成(self, 参数):  # 修改函数名
        """多URL并行生成"""
        import threading  # 导入 threading 模块

        logger.info(f"启动多URL批量生成 :{参数}")  # 记录信息
        线程列表 = []  # 修改变量名

        for i in 参数:  # 修改变量名
            url = i["url"]
            批量生成次数 = i["数量"]  # 修改变量名
            输入 = i["输入"]  # 修改变量名
            t = threading.Thread(
                target=self.批量生成,  # 修改函数名
                args=(url, 批量生成次数,输入),  # 修改变量名
                name=f"Thread-{url}"  # 添加线程名称便于调试
            )
            t.start()
            线程列表.append(t)  # 修改变量名
            logger.debug(f"已启动线程: {t.name}")  # 记录调试信息

        # 等待所有线程完成
        for t in 线程列表:  # 修改变量名
            t.join()
        logger.info("所有生成线程已完成")  # 记录信息

#
# if __name__ == '__main__':
#     提示词生成器实例 = None  # 修改变量名
#     # 请求体副本 ={
#     #     "client_id": "ab78ba85e6e74d188d5fdd68b367da83",
#     #     "prompt": {
#     #         "4": {
#     #             "inputs": {
#     #                 "text": "Positive Prompt",
#     #                 "clip": [
#     #                     "17",
#     #                     1
#     #                 ]
#     #             },
#     #             "class_type": "CLIPTextEncode",
#     #             "_meta": {
#     #                 "title": "CLIP文本编码"
#     #             }
#     #         },
#     #         "5": {
#     #             "inputs": {
#     #                 "text": "Negative Prompt",
#     #                 "clip": [
#     #                     "17",
#     #                     1
#     #                 ]
#     #             },
#     #             "class_type": "CLIPTextEncode",
#     #             "_meta": {
#     #                 "title": "CLIP文本编码"
#     #             }
#     #         },
#     #         "98": {
#     #             "inputs": {
#     #                 "text": "Positive Prompt",
#     #                 "clip": [
#     #                     "17",
#     #                     1
#     #                 ]
#     #             },
#     #             "class_type": "CLIPTextEncode",
#     #             "_meta": {
#     #                 "title": "CLIP文本编码"
#     #             }
#     #         }
#     #     },
#     #     "extra_data": {
#     #         "extra_pnginfo": {
#     #             "workflow": {
#     #                 "nodes": [
#     #                     {
#     #                         "id": 4,
#     #                         "widgets_values": [
#     #                             "Positive Prompt"
#     #                         ]
#     #                     },
#     #                     {
#     #                         "id": 5,
#     #                         "widgets_values": [
#     #                             "Negative Prompt"
#     #                         ]
#     #                     },
#     #                     {
#     #                         "id": 98,
#     #                         "widgets_values": [
#     #                             "Positive Prompt"
#     #                         ]
#     #                     }
#     #                 ]
#     #             }
#     #         }
#     #     }
#     # }
#
#
#     api = ComfyUI_API(提示词生成器实例, "mrnf-api", 根目录="../../")  # 修改变量名
#     请求体副本=api.请求体
#     新请求体副本=api.更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":4}, "widgets_values", 0],
#                      "4的新内容",请求体副本)  # 修改函数名
#     新请求体副本=api.更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":5}, "widgets_values", 0],
#                      "5的新内容",新请求体副本)  # 修改函数名
#     新请求体副本=api.更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":98}, "widgets_values", 0],
#                      "98的新内容",新请求体副本)  # 修改函数名
#
#     print(新请求体副本)
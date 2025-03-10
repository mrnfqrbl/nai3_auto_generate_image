# ... 已有导入 ...
import copy
import json
import sys
import traceback
from urllib.parse import urljoin

import requests
from loguru import logger  # 添加日志模块
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



class comfyui_api:
    def __init__(self, 提示词生成器实例,客户端id="", root_dir="./data"):
        """初始化API实例"""
        # 加载基础请求体（使用深拷贝避免原始数据被修改）
        with open(f"{root_dir}/data/comfyui_json.json", "r", encoding="utf-8") as f:
            self.请求体 = copy.deepcopy(json.load(f))

        self.提示词生成器实例 = 提示词生成器实例
        self.客户端id = 客户端id
        logger.debug("ComfyUI API实例初始化完成")

    def 生成请求体副本(self):
        """生成包含新提示词的请求体副本"""
        请求体副本 = copy.deepcopy(self.请求体)

        # 生成提示词对
        提示词1 = self.提示词生成器实例.提示词组合(sd=True)
        提示词2 = self.提示词生成器实例.提示词组合(sd=True)
        logger.debug(f"生成提示词对 - 正面:[{提示词1[:15]}...] 负面:[{提示词2[:15]}...]")

        # 更新提示词节点
        def 更新节点(节点id, 内容):
            if "prompt" in 请求体副本 and 节点id in 请求体副本["prompt"]:
                请求体副本["prompt"][节点id]["inputs"]["text"] = 内容
            else:
                logger.warning(f"节点{节点id}不存在或结构异常")




        更新节点("4", 提示词1)   # 负面提示词
        更新节点("98", 提示词2)  # 正面提示词
        请求体副本["client_id"] = self.客户端id
        ##额外信息
        根路径=["extra_data","extra_pnginfo","workflow","nodes",]

        return 请求体副本
    def 更新字典信息(self, 节点路径, 内容):
        """
        更新字典信息，支持在列表中的字典中通过键值对搜索特定字典，并直接修改找到的字典。
        支持路径中包含数字，作为列表索引。

        Args:
            节点路径: 节点路径的列表，例如 ["a", "c", "d", {"id": 2}, "xxx"] 或 ["a", "c", "d", 0, "xxx"]。
                     如果路径中包含字典，则会在前一个列表里搜索匹配该字典的元素。
                     如果路径中包含数字，则将其作为列表索引进行访问。
            内容: 要设置的新内容。
        """

        请求体副本 = copy.deepcopy(self.请求体)
        target = 请求体副本
        found_dict = None


        if isinstance(节点路径[-1], int):
            final_key = 节点路径[-2]
            list_key=节点路径[-1]

        else:
            final_key = 节点路径[-1]
            list_key = None



        for i, key in enumerate(节点路径[:-1]):
            if isinstance(key, dict):  # 如果 key 是字典，表示要搜索列表
                if not isinstance(target, list):
                    logger.warning(f"期望列表，但找到 {type(target)}，路径错误")
                    return
                for item in target:
                    if isinstance(item, dict) and all(k in item and item[k] == key[k] for k in key):
                        target = item
                        found_dict = item
                        break
                else:
                    logger.warning(f"未找到匹配字典")
                    return
            elif isinstance(key, int):  # 如果 key 是数字，表示列表索引
                if not isinstance(target, list):
                    logger.warning(f"期望列表，但找到 {type(target)}，路径错误")
                    return
                try:
                    target = target[key]
                except IndexError:
                    logger.warning(f"列表索引超出范围: {key}")
                    return
            else:
                target = target[key]
        print(found_dict)
        if found_dict is not None:
            print(list_key)
            if isinstance(list_key, int):
                found_dict[final_key][list_key] = 内容
                print(final_key)
                print(list_key)
                print(f"修改后的字典: {found_dict}")

            else:
                found_dict[final_key] = 内容
                print(final_key)
                print(f"修改后的字典: {found_dict}")
        else:
            print(target)
            target[final_key] = 内容

    def 发送请求(self, url, 自定义请求体=None):
        """执行API请求并返回响应"""
        请求数据 = 自定义请求体 or self.请求体
        full_url = urljoin(url, "prompt")


        logger.debug(f"正在向 {full_url} 发送请求...")
        response = requests.post(
            url=full_url,
            json=请求数据,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()

        if response_data := response.json():
            if pid := response_data.get("prompt_id"):
                logger.success(f"请求成功 (Prompt ID: {pid})")
            return response_data


        return None

    def 单次生成(self, url):
        """单次生成任务"""

        return self.发送请求(url, self.生成请求体副本())

    def 批量生成(self, url, 批量生成次数=2):
        """批量生成任务"""
        logger.info(f"启动批量生成任务 [次数:{批量生成次数} 客户端ID: {self.客户端id or '未指定'}]")
        for i in range(1, 批量生成次数+1):
            logger.debug(f"正在进行第{i}次生成...")
            self.单次生成(url)

    def 多url批量生成(self, 参数):
        """多URL并行生成"""
        import threading

        logger.info(f"启动多URL批量生成 :{参数}")
        threads = []

        for i in 参数:
            url = i["url"]
            批量生成次数 = i["数量"]
            t = threading.Thread(
                target=self.批量生成,
                args=(url,批量生成次数),
                name=f"Thread-{url}"  # 添加线程名称便于调试
            )
            t.start()
            threads.append(t)
            logger.debug(f"已启动线程: {t.name}")

        # 等待所有线程完成
        for t in threads:
            t.join()
        logger.info("所有生成线程已完成")



if __name__ == '__main__':
    提示词生成器实例 = None
    api=comfyui_api(提示词生成器实例,"mrnf-api",root_dir="../../")
    api.更新字典信息(["extra_data","extra_pnginfo","workflow","nodes",0,"widgets_values",0], "11111111111111111111" )

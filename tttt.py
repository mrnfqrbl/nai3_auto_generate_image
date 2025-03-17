# import copy
# from loguru import logger
# from typing import List, Union
#
#
# def 更新字典信息(节点路径: List[Union[str, int, dict]], 内容: any, 请求体副本: dict) -> dict:
#     """
#     更新字典信息，支持在列表中的字典中通过键值对搜索特定字典，并直接修改找到的字典。
#     支持路径中包含数字，作为列表索引。
#
#     Args:
#         节点路径: 节点路径的列表，例如 ["a", "c", "d", {"id": 2}, "xxx"] 或 ["a", "c", "d", 0, "xxx"]。
#                  如果路径中包含字典，则会在前一个列表里搜索匹配该字典的元素。
#                  如果路径中包含数字，则将其作为列表索引进行访问。
#         内容: 要设置的新内容。
#         请求体副本: 要修改的请求体副本。
#
#     Returns:
#         返回包含更新后内容的完整相关结构的请求体副本。如果更新失败，则返回原始请求体副本。
#     """
#
#     请求体副本 = copy.deepcopy(请求体副本)  # 创建请求体副本，避免修改原始数据
#     目标 = 请求体副本  # 修改变量名
#     逆向路径 = []
#
#     if isinstance(节点路径[-1], int):  # 修改变量名
#         最终键 = 节点路径[-2]  # 修改变量名
#         列表键 = 节点路径[-1]  # 修改变量名
#     else:
#         最终键 = 节点路径[-1]  # 修改变量名
#         列表键 = None  # 修改变量名
#
#     for i, key in enumerate(节点路径[:-1]):  # 修改变量名
#         逆向路径.append((目标, key))
#         # 根据当前target类型决定处理方式
#         if isinstance(目标, dict):  # 修改变量名
#             if isinstance(key, str):
#                 # 字典键访问
#                 if key not in 目标:  # 修改变量名
#                     logger.warning(f"键 '{key}' 不存在于字典中")  # 记录警告信息
#                     return 请求体副本
#                 目标 = 目标[key]  # 修改变量名
#                 logger.debug(f"搜索结果: {目标}")  # 记录调试信息
#             elif isinstance(key, dict):
#                 # 字典中的列表搜索（需明确指定列表字段）
#                 if not isinstance(目标.get(key['field']), list):  # 修改变量名
#                     logger.warning(f"字典中 '{key['field']}' 字段不是列表")  # 记录警告信息
#                     return 请求体副本
#                 目标 = _搜索列表(目标[key['field']], key)  # 修改变量名
#                 logger.debug(f"搜索结果: {目标}")  # 记录调试信息
#             else:
#                 logger.warning(f"字典类型target不支持 {type(key)} 类型路径")  # 记录警告信息
#                 return 请求体副本
#
#         elif isinstance(目标, list):  # 修改变量名
#             if isinstance(key, int):
#                 # 列表索引访问
#                 if key >= len(目标):  # 修改变量名
#                     logger.warning(f"列表索引 {key} 越界 (长度 {len(目标)})")  # 记录警告信息
#                     return 请求体副本
#                 目标 = 目标[key]  # 修改变量名
#                 logger.debug(f"搜索结果: {目标}")  # 记录调试信息
#             elif isinstance(key, dict):
#                 # 列表中的字典搜索
#                 目标 = _搜索列表(目标, key)  # 修改变量名
#                 logger.debug(f"搜索结果: {目标}")  # 记录调试信息
#
#             else:
#                 logger.warning(f"列表类型target不支持 {type(key)} 类型路径")  # 记录警告信息
#                 return 请求体副本
#
#
#         else:
#             logger.warning(f"不支持的target类型 {type(目标)}")  # 记录警告信息
#             return 请求体副本
#
#     # 更新目标值
#     if isinstance(目标, dict):  # 修改变量名
#         目标[最终键] = 内容  # 修改变量名
#     elif isinstance(目标, list):  # 修改变量名
#         if isinstance(列表键, int):  # 修改变量名
#             目标[列表键] = 内容  # 修改变量名
#         else:
#             logger.warning(f"列表键不是整数")  # 记录警告信息
#             return 请求体副本
#     else:
#         logger.warning(f"目标类型 {type(目标)} 不支持更新")  # 记录警告信息
#         return 请求体副本
#
#     return 请求体副本
#
#
# def _搜索列表(lst: List[dict], condition: dict) -> Union[dict, None]:  # 修改函数名
#     """在列表中搜索匹配条件的字典"""
#     if not isinstance(lst, list):
#         logger.warning("搜索目标不是列表")  # 记录警告信息
#         return None
#     matches = [item for item in lst
#                if isinstance(item, dict) and all(item.get(k) == v for k, v in condition.items())]
#
#     if len(matches) > 1:
#         logger.warning(f"找到多个匹配项 {condition}")  # 记录警告信息
#         return None
#     if not matches:
#         logger.warning(f"未找到匹配项 {condition}")  # 记录警告信息
#         return None
#     return matches[0]
#
# 请求体副本 ={
#     "client_id": "ab78ba85e6e74d188d5fdd68b367da83",
#     "prompt": {
#         "4": {
#             "inputs": {
#                 "text": "Positive Prompt",
#                 "clip": [
#                     "17",
#                     1
#                 ]
#             },
#             "class_type": "CLIPTextEncode",
#             "_meta": {
#                 "title": "CLIP文本编码"
#             }
#         },
#         "5": {
#             "inputs": {
#                 "text": "Negative Prompt",
#                 "clip": [
#                     "17",
#                     1
#                 ]
#             },
#             "class_type": "CLIPTextEncode",
#             "_meta": {
#                 "title": "CLIP文本编码"
#             }
#         },
#         "98": {
#             "inputs": {
#                 "text": "Positive Prompt",
#                 "clip": [
#                     "17",
#                     1
#                 ]
#             },
#             "class_type": "CLIPTextEncode",
#             "_meta": {
#                 "title": "CLIP文本编码"
#             }
#         }
#     },
#     "extra_data": {
#         "extra_pnginfo": {
#             "workflow": {
#                 "nodes": [
#                     {
#                         "id": 4,
#                         "widgets_values": [
#                             "Positive Prompt"
#                         ]
#                     },
#                     {
#                         "id": 5,
#                         "widgets_values": [
#                             "Negative Prompt"
#                         ]
#                     },
#                     {
#                         "id": 98,
#                         "widgets_values": [
#                             "Positive Prompt"
#                         ]
#                     }
#                 ]
#             }
#         }
#     }
# }
#
#
# 请求体副本 = 更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":4}, "widgets_values", 0],
#                           "4的新内容",请求体副本)  # 修改函数名
# 请求体副本 = 更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":5}, "widgets_values", 0],
#                           "5的新内容",请求体副本)  # 修改函数名
# 请求体副本 = 更新字典信息(["extra_data", "extra_pnginfo", "workflow", "nodes", {"id":98}, "widgets_values", 0],
#                           "98的新内容",请求体副本)  # 修改函数名
#
# print(请求体副本)

import hashlib

def 生成目录名称(url):
    """
    根据 URL 生成一个 32 位以内、文本形式、唯一且相同输入相同输出的目录名称。
    """
    url_哈希 = hashlib.sha256(url.encode('utf-8')).hexdigest()  # 使用 SHA256，生成 64 位十六进制字符串
    目录名称 = url_哈希[:32]  # 截断到 32 位

    return 目录名称

# 示例
url1 = "https://www.example.com/path/to/resource"
url2 = "https://www.example.com/another/path"
url3 = "https://www.example.com/path/to/resource"  # 与 url1 相同

目录名称1 = 生成目录名称(url1)
目录名称2 = 生成目录名称(url2)
目录名称3 = 生成目录名称(url3)

print(f"URL 1: {url1} -> 目录名称: {目录名称1}")
print(f"URL 2: {url2} -> 目录名称: {目录名称2}")
print(f"URL 3: {url3} -> 目录名称: {目录名称3}")

print(f"目录名称 1 和 3 是否相同: {目录名称1 == 目录名称3}")
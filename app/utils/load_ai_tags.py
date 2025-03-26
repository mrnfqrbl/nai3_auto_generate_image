import datetime
import glob
import json
import os
import random
import re

from loguru import logger


def 加载提示词组(标签路径, 完整提示词组列表):
    """
    递归遍历目录及其子目录，加载符合条件的 JSON 文件到完整提示词组列表。

    Args:
        标签路径 (str): 根目录路径。
        完整提示词组列表 (list): 用于存储加载的提示词组的列表。

    Returns:
        list: 更新后的完整提示词组列表。
    """

    已加载文件 = set()  # 用于跟踪已加载的文件，防止重复加载

    def 验证JSON格式(数据):
        """
        验证 JSON 数据是否符合指定的格式。

        Args:
            数据 (list): JSON 数据。

        Returns:
            bool: 如果符合格式，返回 True；否则返回 False。
        """
        if not isinstance(数据, list):
            logger.warning("JSON 数据不是列表")
            return False

        for 项目 in 数据:
            if not isinstance(项目, dict):
                logger.warning(f"JSON 数据中的项目 {项目} 不是字典")
                return False
            if not all(键 in 项目 for 键 in ["中文说明", "英语提示词"]):
                logger.warning(f"JSON 数据中的项目 {项目} 缺少必要的键")
                return False
            # 可以根据需要添加更严格的类型检查和格式验证

        return True

    def 目录名是否符合日期格式(目录名):
        """
        检查目录名是否符合 'YYYY-MM-DD' 的日期格式。

        Args:
            目录名 (str): 目录名。

        Returns:
            bool: 如果符合日期格式，返回 True；否则返回 False。
        """
        match = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", 目录名)
        if match:
            try:
                年, 月, 日 = map(int, match.groups())
                datetime.date(年, 月, 日)  # 验证日期是否有效
                return True
            except ValueError:
                logger.warning(f"目录名 {目录名} 日期格式无效")
                return False
        else:
            logger.warning(f"目录名 {目录名} 不符合日期格式")
            return False

    logger.debug(f"开始加载提示词组，标签路径: {标签路径}")

    for 根目录, 子目录列表, 文件列表 in os.walk(标签路径):  # 使用 标签路径
        logger.debug(f"当前根目录: {根目录}")
        logger.debug(f"当前子目录列表: {子目录列表}")
        logger.debug(f"当前文件列表: {文件列表}")

        # 1. 检查当前根目录是否符合日期格式
        if 目录名是否符合日期格式(os.path.basename(根目录)):  # 检查根目录名是否符合日期格式
            # 使用 glob 查找所有 *.json 文件
            json_文件列表 = glob.glob(os.path.join(根目录, "*.json"))
            logger.debug(f"找到的 JSON 文件（根目录）: {json_文件列表}")

            for JSON文件路径 in json_文件列表:
                if os.path.isfile(JSON文件路径) and JSON文件路径 not in 已加载文件:  # 确保是文件而不是目录, 并且没有被加载过
                    try:
                        with open(JSON文件路径, "r", encoding="utf-8") as 文件:
                            数据 = json.load(文件)
                            if 验证JSON格式(数据):
                                完整提示词组列表.append(数据)  # 使用 append
                                已加载文件.add(JSON文件路径)  # 添加到已加载文件集合
                                logger.info(f"成功加载: {JSON文件路径}")
                            else:
                                logger.warning(f"JSON 格式不符合要求: {JSON文件路径}")
                    except json.JSONDecodeError:
                        logger.error(f"JSON 解码错误: {JSON文件路径}")
                    except Exception as 异常:
                        logger.exception(f"加载文件时发生错误: {JSON文件路径}, 错误信息: {异常}")
                elif JSON文件路径 in 已加载文件:
                    logger.debug(f"跳过已加载文件: {JSON文件路径}")

        # 2. 检查子目录列表中的目录是否符合日期格式 (如果需要)
        for 目录名 in 子目录列表:
            logger.debug(f"正在处理目录名: {目录名}")
            if 目录名是否符合日期格式(目录名):
                # 使用 glob 查找所有 *.json 文件
                json_文件列表 = glob.glob(os.path.join(根目录, 目录名, "*.json"))
                logger.debug(f"找到的 JSON 文件（子目录）: {json_文件列表}")

                for JSON文件路径 in json_文件列表:
                    if os.path.isfile(JSON文件路径) and JSON文件路径 not in 已加载文件:  # 确保是文件而不是目录, 并且没有被加载过
                        try:
                            with open(JSON文件路径, "r", encoding="utf-8") as 文件:
                                数据 = json.load(文件)
                                if 验证JSON格式(数据):
                                    完整提示词组列表.append(数据)  # 使用 append
                                    已加载文件.add(JSON文件路径)  # 添加到已加载文件集合
                                    logger.info(f"成功加载: {JSON文件路径}")
                                else:
                                    logger.warning(f"JSON 格式不符合要求: {JSON文件路径}")
                        except json.JSONDecodeError:
                            logger.error(f"JSON 解码错误: {JSON文件路径}")
                        except Exception as 异常:
                            logger.exception(f"加载文件时发生错误: {JSON文件路径}, 错误信息: {异常}")
                    elif JSON文件路径 in 已加载文件:
                        logger.debug(f"跳过已加载文件: {JSON文件路径}")

    def 计算总元素数量(列表):
        """
        计算嵌套列表中所有元素的总数。
        """
        总数 = 0
        for 子列表 in 列表:
            总数 += len(子列表)
        return 总数

    总提示词数量 = 计算总元素数量(完整提示词组列表)
    logger.info(f"加载提示词组完成，共加载 {len(已加载文件)} 个文件，包含 {总提示词数量} 个提示词")
    return 完整提示词组列表

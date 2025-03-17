
def 查询JSON数据(数据源, 路径列表):
    """
    JSON数据查询函数（中文命名版）
    :param 数据源: 要查询的原始数据（字典/列表）
    :param 路径列表: 查询路径步骤列表，支持字符串键、字典条件和数字索引
    :return: 查询结果或None（路径不存在时）
    """
    当前数据 = 数据源

    for 路径步骤 in 路径列表:
        if 当前数据 is None:
            return None

        # 处理字典键查询
        if isinstance(路径步骤, str):
            if isinstance(当前数据, dict):
                当前数据 = 当前数据.get(路径步骤)
            else:
                return None

        # 处理字典条件查询
        elif isinstance(路径步骤, dict):
            找到项 = None
            # 在列表中搜索符合条件的元素
            if isinstance(当前数据, list):
                for 列表项 in 当前数据:
                    if all(列表项.get(键) == 值 for 键, 值 in 路径步骤.items()):
                        找到项 = 列表项
                        break
            # 在字典中直接匹配条件
            elif isinstance(当前数据, dict):
                if all(当前数据.get(键) == 值 for 键, 值 in 路径步骤.items()):
                    找到项 = 当前数据
            当前数据 = 找到项

        # 处理数字索引查询
        elif isinstance(路径步骤, int):
            if isinstance(当前数据, list) and 0 <= 路径步骤 < len(当前数据):
                当前数据 = 当前数据[路径步骤]
            else:
                return None

        else:
            return None

    return 当前数据





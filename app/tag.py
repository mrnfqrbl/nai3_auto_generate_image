import random

class 提示词生成器:
    def __init__(self, *args, **kwargs):
        self.角色 = kwargs.get('角色', None)
        self.画风 = kwargs.get('画风', None)
        self.动作 = kwargs.get('动作', None)
        self.质量 = kwargs.get('质量', "best quality, amazing quality, very aesthetic, absurdres")
        self.角色_index = 0
        self.画风_index = 0
        self.动作_index = 0

    def 提示词组合(self, 是否随机=False):
    # 随机提取
        if 是否随机:
            提取的角色 = self.角色[str(random.randint(1, len(self.角色)))]
            提取的画风 = self.画风[str(random.randint(1, len(self.画风)))]
            提取的动作 = self.动作[str(random.randint(1, len(self.动作)))]
        else:
        # 按照顺序提取角色，画风，动作
            提取的角色 = self.角色[str(self.角色_index + 1)]
            提取的画风 = self.画风[str(self.画风_index + 1)]
            提取的动作 = self.动作[str(self.动作_index + 1)]

        # 更新索引顺序，确保顺序提取
            self.角色_index = (self.角色_index + 1) % len(self.角色)
            self.画风_index = (self.画风_index + 1) % len(self.画风)
            self.动作_index = (self.动作_index + 1) % len(self.动作)

    # 组合并返回
        parts = [提取的角色.strip(), 提取的画风.strip(), 提取的动作.strip(), self.质量.strip()]

    # 使用 filter() 过滤掉空字符串，然后用逗号拼接
        组合 = ', '.join([part for part in parts if part])  # 只拼接非空部分

        return 组合



if __name__ == "__main__":
    # 示例
    角色 = {
    "1": "角色A，sss，",
    "2": "角色B",
    "3": "角色C",
    "4": "角色D"
}

    画风 = {
    "1": "画风X",
    "2": "画风，dY",
    "3": "画风Z"
}

    动作 = {
    "1": "动作A",
    "2": "动作B",
    "3": "动作C"
}

    质量 = "高清"

# 创建提示词生成器实例
    生成器 = 提示词生成器()

# 获取提示词组合
    for _ in range(5):  # 获取5次组合示例
        print(生成器.提示词组合(角色=角色, 画风=画风, 动作=动作, 质量=质量, 是否随机=True))


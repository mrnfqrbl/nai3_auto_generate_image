import json
import random
from loguru import logger

class 提示词生成器:
    def __init__(self, *args, **kwargs):
        """
      初始化 提示词生成器 对象。

      参数：
          *args: 可变的位置参数，此处未使用。
          **kwargs: 可变的关键字参数，用于接收配置信息。

          角色 (dict, optional):
              角色字典，键为角色ID（字符串），值为角色描述文本。
              例如：{"1": "一个穿着红色连衣裙的女孩", "2": "一个拿着剑的战士"}
              默认为 None，表示不使用角色。

          画风 (dict or list, optional):
              画风字典或列表。
               如果为字典，键为画风ID（字符串），值为画风描述文本。
               例如：{"1": "水彩风格", "2": "油画风格"}
               如果为列表，则直接使用画风描述文本列表。
               例如：["by artgerm", "by wlop", "by greg rutkowski"]
               默认为 None，表示不使用画风。

          动作 (dict, optional):
              动作字典，键为动作ID（字符串），值为动作描述文本。
              例如：{"1": "正在跑步", "2": "正在微笑"}
              默认为 None，表示不使用动作。

          质量 (str, optional):
              图像质量描述字符串，默认为 "best quality, amazing quality, very aesthetic, absurdres"。
              例如："high quality, masterpiece, 8k"

          角色是否可无 (bool, optional):
              指示是否可以不使用角色，默认为 False。
              如果为 True，在生成提示词时，角色部分可能为空。

          是否固定画风 (bool or int, optional):
              指示是否固定画风。
               如果为 False，则不固定画风。
               如果为整数，则固定使用画风列表或字典中的序号为该整数的画风。
               如果画风为artist.json文件，则为画师在文件中的序号
               默认为 False。

          是否固定角色 (bool or int, optional):
              指示是否固定角色。
              如果为 False，则不固定角色。
              如果为整数，则固定使用角色字典中序号为该整数的角色。
              默认为 False。

          是否固定动作 (bool or int, optional):
              指示是否固定动作。
              如果为 False，则不固定动作。
               如果为整数，则固定使用动作字典中序号为该整数的动作。
              默认为 False。

          角色获取方式 (str, optional):
              指定角色获取方式，默认为 '随机'。
              可选值：'随机' 或 '顺序'。

          动作获取方式 (str, optional):
              指定动作获取方式，默认为 '随机'。
              可选值：'随机' 或 '顺序'。

          画风获取方式 (str, optional):
               指定画风获取方式，默认为 '随机'。
               可选值：'随机' 或 '顺序'。
               如果输入为 artist文件 则指定无效

      """
        self.root_dir=kwargs.get('root_dir', '')
        self.角色 = kwargs.get('角色', None)
        self.画风 = kwargs.get('画风', None)
        self.动作 = kwargs.get('动作', None)
        self.质量 = kwargs.get('质量', "best quality, amazing quality, very aesthetic, absurdres")
        self.角色是否可无 = kwargs.get('角色是否可无', False)
        self.是否指定画风 = kwargs.get('是否指定画风', False)
        #注固定类参数 值可以为 false和 数字 “数字位你需要固定的提示词在tags的序号，如果画风输入为artist文件则固定的是画师 数字为画师在artist。json的序号
        #self.是否指定角色 = str(kwargs.get('是否指定角色', False))
        self.是否指定角色 = kwargs.get('是否指定角色', False)
        #print(f"tag指定角色为：{self.是否指定角色}")
        #print(f"tag指定角色类型为：{type(self.是否指定角色)}")
        self.是否指定动作 = kwargs.get('是否指定动作', False)
        self.角色获取方式 = kwargs.get('角色获取方式', '随机')
        self.动作获取方式 = kwargs.get('动作获取方式', '随机')
        self.画风获取方式 = kwargs.get('动作获取方式', '随机')#如果输入为 artist文件 则指定无效


        # 如果 '画风' 参数是字典，则直接使用，否则尝试加载画风数据
        if self.画风:
            if isinstance(self.画风, dict):
                self.画风 = self.画风
            else:
                self.画风  = self._加载画师数据(f'{self.root_dir}/data/artist.json')
        else:
            self.画风 = self._加载画师数据(f'{self.root_dir}/data/artist.json')
        self.角色索引 = -1
        self.画风索引 = -1
        self.动作索引 = -1

    def _加载画师数据(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                #logger.info(f"加载画师数据成功！")
                #logger.info(f"画师数据：{data}")
                # 使用列表推导式提取每部字典的 'value' 值
                artist_values = [item['value'] for item in data]
                #logger.info(f"画师数据列表：{artist_values}")
                return artist_values
        except FileNotFoundError:

            raise FileNotFoundError(f"文件 '{filename}' 不存在。")
        except json.JSONDecodeError:

            raise ValueError(f"文件 '{filename}' 不是有效的 JSON 文件。")
        except Exception as e:
            raise e
    def 提示词组合(self):


        提取角色=self.角色提取()

        提取画风=self.画风提取()
        提取动作=self.动作提取()
        if self.角色是否可无:
            if random.random() > 0.3:  # 随机决定是否添加角色
                返回=f"{提取角色},{提取画风},{提取动作}，{self.质量}"
            else:
                返回=f"{提取画风},{提取动作}，{self.质量}"
        else:
            返回=f"{提取角色},{提取画风},{提取动作}，{self.质量}"
        return 返回


    def 角色提取(self):
        if self.角色:
            if isinstance(self.角色, dict):
                if isinstance(self.是否指定角色, int):
                    指定角色=str(self.是否指定角色)

                    key = 指定角色
                    if key in self.角色: # 检查键是否存在于字典中
                        #print(f"角色为字典，key：{key}")
                        self.提取的角色 = self.角色[key]
                        return self.提取的角色
                    else:
                        pass
                #print(f"tag角色为字典，未指定角色，获取方式为：{self.角色获取方式}")
                # 如果没有指定角色，或者指定的角色索引无效，则按照原逻辑提取
                if self.角色获取方式 == '随机':
                    self.提取的角色 = random.choice(list(self.角色.values()))
                elif self.角色获取方式 == '顺序':
                    self.角色索引 = (self.角色索引 + 1) % len(self.角色)
                    #logger.info(f"角色索引：{self.角色索引}")
                    self.提取的角色 = list(self.角色.values())[self.角色索引]
                else:
                    self.提取的角色 = random.choice(list(self.角色.values())) # 默认随机

            else:
                return None # 如果角色不是字典，返回None
        else:
            return None # 如果角色不存在，返回None

        return self.提取的角色
    def 画风提取(self):
        if self.画风:
            if isinstance(self.画风, list):
                随机数量=random.randint(3, 7)

                列表=random.sample(self.画风, 随机数量)
                #logger.info(f"列表{列表}")
                格式化后列表=[f"artist: {style}" for style in 列表]
                #logger.info(f"格式化后列表{格式化后列表}")
                self.提取的画风=  ", ".join(格式化后列表)
                #logger.info(f"提取的画风{self.提取的画风}")
                return self.提取的画风
            elif isinstance(self.画风, dict):
                if isinstance(self.是否指定画风, int):
                    指定画风序号=str(self.是否指定画风)
                    if 指定画风序号 in self.画风:
                        self.提取的画风 = self.画风[指定画风序号]
                        return self.提取的画风
                    else:
                        pass

                elif self.画风获取方式 == '随机':
                    pass
                elif self.画风获取方式 == '顺序':
                    self.画风索引 = (self.画风索引 + 1) % len(self.画风)
                    self.提取的画风 = list(self.画风.values())[self.画风索引]
                    return self.提取的画风
                else:
                    pass
                self.提取的画风 = random.choice(list(self.画风.values()))


            else:
                #logger.info(f"错误：画风数据 '{self.画风}' 不是有效的 JSON 格式。")
                return None
            return self.提取的画风
        else:
            #logger.info(f"错误：画风数据 '{self.画风}' 不是有效的 JSON 格式。")
            return None
    def 动作提取(self):
        if self.动作:
            if isinstance(self.动作, dict):
                if isinstance(self.是否指定动作, int):
                    指定动作序号=str(self.是否指定动作)
                    if 指定动作序号 in self.动作:
                        self.提取的动作 = self.动作[指定动作序号]
                        return self.提取的动作
                    else:
                        pass

                elif self.动作获取方式 == '随机':
                    pass
                elif self.动作获取方式 == '顺序':
                    self.动作索引 = (self.动作索引 + 1) % len(self.动作)
                    self.提取的动作 = list(self.动作.values())[self.动作索引]
                    return self.提取的动作
                else:
                    pass
                self.提取的动作 = random.choice(list(self.动作.values()))
                return self.提取的动作

            else:
                return None
        return None










if __name__ == "__main__":
    # 示例
    角色 = {
        "1": "角色A",
        "2": "角色B",
        "3": "角色C",
        "4": "角色D",
        "5": "角色E",
        "6": "角色F",
        "7": "角色G"
    }

    画风 = {
        "1": "画风A",
        "2": "画风B",
        "3": "画风C",
        "4": "画风D",
        "5": "画风E",
        "6": "画风F",
        "7": "画风G"
    }
    动作 = {
        "1": "动作A",
        "2": "动作B",
        "3": "动作C",
        "4": "动作D",
        "5": "动作E",
        "6": "动作F",
        "7": "动作G"
    }


    # 创建提示词生成器实例
    root_dir=r"D:\xm\nai3_auto_generate_image"
    #生成器 = 提示词生成器(角色=角色, 画风=画风, 动作=动作, 角色是否可无=True,角色获取方式='顺序',画风获取方式='顺序',动作获取方式='顺序')
    生成器= 提示词生成器(角色=角色,动作=动作,画风=画风, 角色是否可无=False,
                         角色获取方式='顺序',画风获取方式='顺序',动作获取方式='顺序',
                         root_dir=root_dir,是否指定角色=1,是否指定画风=1,
                         是否指定动作=1)
    # 获取提示词组合
    for _ in range(10):  # 获取5次组合示例
        print(生成器.提示词组合())






# class 提示词生成器:
#     """
#     一个用于生成图像生成提示词的类。
#     """
#
#     def __init__(self, *args, **kwargs):
#         """
#         初始化 提示词生成器 对象。
#
#         参数：
#             角色 (dict, optional): 角色字典，键为角色ID（字符串），值为角色描述文本。
#             画风 (dict or list, optional): 画风字典或列表。
#                  如果为字典，键为画风ID（字符串），值为画风描述文本。
#                  如果为列表，则直接使用画风描述文本列表。
#             动作 (dict, optional): 动作字典，键为动作ID（字符串），值为动作描述文本。
#             质量 (str, optional): 图像质量描述字符串，默认为 "best quality, amazing quality, very aesthetic, absurdres"。
#         """
#         self.角色 = kwargs.get('角色', None)
#         self.画风 = kwargs.get('画风', None)
#         self.动作 = kwargs.get('动作', None)
#         self.质量 = kwargs.get('质量', "best quality, amazing quality, very aesthetic, absurdres")
#
#         # 如果 '画风' 参数是字典，则直接使用，否则尝试加载画风数据
#         if isinstance(self.画风, dict):
#             self.画风 = self.画风
#         else:
#             self.画师数据 = self._加载画师数据('../../data/artist.json')
#             self.画风 = None  # 初始时设置为 None，后续可能被设置为加载的数据
#
#         self.角色索引 = 0
#         self.画风索引 = 0
#         self.动作索引 = 0
#
#
#     def 生成提示词(self, 是否随机=False):
#         """
#         生成提示词。
#
#         参数：
#             是否随机 (bool, optional): 是否随机选择角色、画风和动作。默认为 False。
#
#         返回：
#             str: 生成的提示词字符串。
#         """
#         if self.画风 is None:
#             self.画风 = self.画师数据  # 如果画风未加载，则使用加载的数据
#
#         if isinstance(self.画风, list):
#             # 从画风列表中随机选择几个画风
#             画师数量 = random.randint(3, 7)
#             选取的画风 = ", ".join(
#                 f"artist:{画师.strip()}" for 画师 in random.sample(self.画风, min(画师数量, len(self.画风)))
#             )
#             parts = [选取的画风, self.质量.strip()]
#         elif isinstance(self.画风, dict):
#             # 根据 是否随机 参数，选择随机或顺序提取
#             if 是否随机:
#                 选取的角色 = self.角色[str(random.randint(1, len(self.角色)))]
#                 选取的画风 = self.画风[str(random.randint(1, len(self.画风)))]
#                 选取的动作 = self.动作[str(random.randint(1, len(self.动作)))]
#             else:
#                 选取的角色 = self.角色[str(self.角色索引 + 1)]
#                 选取的画风 = self.画风[str(self.画风索引 + 1)]
#                 选取的动作 = self.动作[str(self.动作索引 + 1)]
#
#                 # 更新索引，实现顺序提取
#                 self.角色索引 = (self.角色索引 + 1) % len(self.角色)
#                 self.画风索引 = (self.画风索引 + 1) % len(self.画风)
#                 self.动作索引 = (self.动作索引 + 1) % len(self.动作)
#
#             parts = [选取的角色.strip(), 选取的画风.strip(), 选取的动作.strip(), self.质量.strip()]
#         else:
#             parts = [self.质量.strip()]
#
#         # 拼接非空部分
#         提示词 = ', '.join(filter(None, parts))
#         return 提示词
#
#
#     def _加载画师数据(self, 文件路径):
#         """
#         从指定文件加载画风数据。
#
#         参数：
#             文件路径 (str): 画风数据文件的路径。
#
#         返回：
#             list or None: 画风数据列表，如果加载失败则返回 None。
#         """
#         try:
#             with open(文件路径, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 # 假设数据结构是 [ { "id": 1, "value": "xxx" }, ... ]
#                 if isinstance(data, list):
#                     return [item["value"] for item in data]
#                 else:
#                     print(f"警告：画风数据文件 {文件路径} 格式不正确。")
#                     return None
#         except FileNotFoundError:
#             print(f"警告：找不到画风数据文件：{文件路径}。请确保文件存在并包含有效的 JSON 数据。")
#             return None
#         except json.JSONDecodeError:
#             print(f"警告：画风数据文件 {文件路径} 包含无效的 JSON 数据。")
#             return None
#

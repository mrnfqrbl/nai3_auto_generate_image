import random
from app.utils.log_config import logger


class 参数生成器:
    def __init__(self, **参数):
        """
        用于生成图像生成模型参数的类。

        注！！！！！==== 如果是期待布尔值的参数 ，则接收参数的数字0为False ，1为True 2为随机
        注！！！！！==== 如果是期待字符串的参数，则接收参数的 数字0为随机的意思
        注！！！！！==== 如果是期待int的参数，则接收参数的0 1等值一视同仁 无特殊含义

        :param 参数: 传递方式 为关键字参数，例如：尺寸="竖向", 采样=0, 提示词引导系数=6, 种子=0, smea=0
        或者：
           参数字典 = {"尺寸": "随机", "采样": 0}
           参数生成器实例 = 参数生成器(**参数字典)
        :尺寸 (str): 图片的尺寸类型，默认为 "竖向"。 可以是 "竖向", "竖", "纵向", "纵", "横向", "横", "正方形", "方形", "随机", "自适应", "任意"。
                      如果为 "随机", "自适应", "任意" 则会随机选择一个尺寸。如果未提供或者为无效值，则默认为 "竖向"。
        :采样 (int/str): 采样方法，默认为 0。 0 代表随机选择， 其他字符串则为对应的采样方法
        :提示词引导系数 (int): 提示词引导系数，默认为 6。取值范围为 4-7，超出范围则使用默认值 6。
        :种子 (int): 随机数种子，默认为 0。 如果种子大于100000000，则只在第一次生成时使用，后续随机生成
        :smea (int): smea 参数，默认为 0。 0 代表 False, 1 代表 True, 2 代表随机。
        """
        self.尺寸 = 参数.get("尺寸", "竖向")
        self.采样 = 参数.get("采样", 0)
        self.提示词引导系数 = 参数.get("提示词引导系数", 6)
        self.种子 = 参数.get("种子", 0)
        self.smea = 参数.get("smea", 0)
        self.尺寸映射 = {
            ("竖向", "竖", "纵向", "纵"): {"宽度": 832, "高度": 1216},
            ("横向", "横"): {"宽度": 1216, "高度": 832},
            ("正方形", "方形"): {"宽度": 1024, "高度": 1024},
        }

        self.随机尺寸 = list(self.尺寸映射.values())
        self.采样映射 = {
            "e": "k_euler",
            "ea": "k_euler_ancestral",
        }
        self.随机采样 = list(self.采样映射.values())

        self.缓存 = {
            "尺寸": None,
            "采样": None,
            "提示词引导系数": None,
            "种子": None,
            "smea": None
        }
        self.init()

    def 生成尺寸(self):
        for keys, value in self.尺寸映射.items():
            if self.尺寸 in keys:
                self.缓存["尺寸"] = value
                return value
        if self.尺寸 in ("随机", "自适应", "任意"):

            return random.choice(self.随机尺寸)
        # 如果尺寸无效，则返回竖向的尺寸
        logger.info(f"尺寸{self.尺寸}无效，已自动选择一个随机尺寸")
        self.缓存["尺寸"] = self.尺寸映射[("竖向", "竖", "纵向", "纵")]
        return self.缓存["尺寸"]

    def 生成采样(self):
        if isinstance(self.采样, str) and self.采样 in self.采样映射:
            self.缓存["采样"] = self.采样映射[self.采样]
            return self.缓存["采样"]
        elif self.采样 == 0:

            return  random.choice(self.随机采样)
        else:
            logger.info(f"采样方法{self.采样}无效，已自动选择默认采样方法 ea")
            self.缓存["采样"] = self.采样映射["ea"]
            return self.缓存["采样"]

    def 生成提示词引导系数(self):
        if not isinstance(self.提示词引导系数, int):
            logger.error(f"提示词引导系数 {self.提示词引导系数} 类型错误，应为 int 类型， 已设置为默认值 6")
            self.缓存["提示词引导系数"] = 6
            return 6
        if self.提示词引导系数 == 0:

            return random.randint(4, 7)
        elif self.提示词引导系数 < 4 or self.提示词引导系数 > 7:
            logger.warning(f"提示词引导系数 {self.提示词引导系数} 超出范围 (4-7), 已设置为默认值 6")
            self.缓存["提示词引导系数"] = 6
            return 6
        else:
            self.缓存["提示词引导系数"] = self.提示词引导系数
            return self.缓存["提示词引导系数"]

    def 生成种子(self):
        if isinstance(self.种子, int) and self.种子 >100000000:
            if self.种子 == self.缓存["种子"]:
                return random.randint(100000001, 1000000000)
            else:
                logger.info( f"种子{self.种子}重复，已自动生成一个随机种子")
                self.缓存["种子"]=self.种子

                return self.种子
        else:

            logger.debug( f"种子{self.种子}无效，已自动生成一个随机种子")
            return random.randint(100000001, 1000000000)
    def 生成smea(self):
        if self.smea == 1:
            self.缓存["smea"] = True
            return True
        elif self.smea == 0:
            self.缓存["smea"] = False
            return False
        elif self.smea == 2:
            return random.choice([True, False])
        else:
            logger.info(f"smea{self.smea}无效，默认关闭smea")
            self.缓存["smea"] = False
            return False

    def init(self):
        self.生成尺寸()
        self.生成采样()
        self.生成提示词引导系数()
        self.生成种子()
        self.生成smea()
        logger.debug(f"初始化参数完成：\n 缓存：{self.缓存}")

    def 获取参数(self):
        返回参数字典 = {}
        参数列表 = ["尺寸", "采样", "提示词引导系数", "smea"]
        生成方法映射 = {
            "尺寸": self.生成尺寸,
            "采样": self.生成采样,
            "提示词引导系数": self.生成提示词引导系数,
            "smea": self.生成smea,
        }
        for 参数 in 参数列表:
            if self.缓存.get(参数):
                返回参数字典[参数] = self.缓存[参数]
            else:
                返回参数字典[参数] = 生成方法映射[参数]()
        返回参数字典["种子"]=self.生成种子()
        return 返回参数字典


if __name__ == "__main__":
    print("实例11111111111")
    参数生成器实例 = 参数生成器(尺寸="随机", 采样="e", 提示词引导系数=0, 种子=123456789, smea=2)
    for i in range(100):
        print(参数生成器实例.获取参数())
        print ("-"*50)



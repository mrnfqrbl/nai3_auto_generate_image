import os
import zipfile
import random
import time


from app.tag import 提示词生成器

import json
from datetime import datetime
from io import BytesIO

from app.novelai_api import NovelAI_API
from app.config_manager import ConfigManager


class ImageGenerator:
    def __init__(self, config_path: str,):
        """
        初始化类，加载配置文件，实例化API。

        :param config_path: 配置文件路径
        :param sequence_file: 存储序号的文件路径
        """

        self.sequence_file = os.path.join(os.getcwd(), "data", "sequence.json")

        print(f"Sequence file path: {self.sequence_file}")  # 打印路径，调试时可以查看路径是否正确

        self.config_path = config_path
        self.token = ""
        self.negative_prompt = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], underwear"
        #默认生成图像数量为1
        self.quantity = 0
        # 加载配置
        self.config_load()

        # 初始化 API 实例
        self.api = NovelAI_API(self.token, self.negative_prompt)

        # 获取当前日期并初始化图像计数器
        self.current_date = datetime.now().strftime('%Y%m%d')
        self.image_counter = self.load_counter()

    def config_load(self):
        """
        加载配置文件并设置 token 和生成图像的数量等参数。
        """
        config_manager = ConfigManager(self.config_path)

        # 读取配置文件中的API token和生成图像数量
        self.token = config_manager.get("API", "token")
        self.quantity = config_manager.get_int("GENERATION", "quantity")

        print(f"API Token: {self.token}")
        print(f"总数量: {self.quantity}")

    def load_counter(self):
        """
        加载序号计数器，检查日期是否匹配，如果匹配则返回存储的序号，否则重置为1。
        如果文件不存在，创建新的文件并初始化计数器。
        """
        print(f"Checking if sequence file exists: {self.sequence_file}")  # 调试打印文件路径

        if os.path.exists(self.sequence_file):
            try:
                with open(self.sequence_file, 'r') as f:
                    data = json.load(f)
                    # 如果日期一致，返回存储的序号
                    if data.get('date') == self.current_date:
                        return data.get('counter', 1)
            except (json.JSONDecodeError, IOError):
                print("警告: 序号文件损坏或无法读取，正在重置计数器。")

        # 如果文件不存在或者损坏，则初始化文件
        self.initialize_counter()
        return 1  # 如果文件不存在或日期不匹配，返回初始序号 1

    def initialize_counter(self):
        """
        如果序号文件不存在或无法读取，则初始化文件并保存初始序号。
        """
        data = {
            'date': self.current_date,
            'counter': 1
        }
        # 确保目录存在
        data_folder = os.path.dirname(self.sequence_file)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # 创建并写入新的序号文件
        with open(self.sequence_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"初始化序号文件: {self.sequence_file}")


    def save_counter(self):
        """
        保存当前日期和序号到文件。
        """
        data = {
            'date': self.current_date,
            'counter': self.image_counter
        }
        with open(self.sequence_file, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_img(self, *args, **kwargs):
        # 获取或设置默认参数
        角色 = kwargs.get('角色', None)
        画风 = kwargs.get('画风', None)
        动作 = kwargs.get('动作', None)
        质量 = kwargs.get('质量', "best quality, amazing quality, very aesthetic, absurdres")
        proportional = kwargs.get('proportional', "竖向")

        提示词=提示词生成器(角色=角色, 画风=画风, 动作=动作, 质量=质量)
        # 使用每次循环时重新生成提示词
        for i in range(self.quantity):
            # 每次循环重新生成prompt
            prompt = 提示词.提示词组合(是否随机=True)
            # 使用随机种子
            seed = random.randint(1, 1000000)  # 随机种子
            print(f"第 {i + 1} 张图像生成中，种子: {seed}")

            print("提示词为:",prompt)
            # 调用API生成图像
            image_data = self.api.generate_image(prompt, seed=seed, proportional=proportional)

            if image_data:
               print(f"第 {i + 1} 张图像生成成功，已返回原始ZIP文件内容！")
               self.download_img(image_data, seed)  # 下载并保存图像
            else:
               print(f"第 {i + 1} 张图像生成失败。")
            #self.image_counter += 1

            # 每生成一张图像后延时1秒
            time.sleep(1)

    def get_filename(self, seed: int):
        """
        生成带有种子的文件名，并确保每次生成图像时序号递增。

        :param seed: 生成图像的种子
        :return: 返回生成的文件名
        """
        current_time = datetime.now().strftime('%H-%M-%S')
        filename = f"{self.image_counter:03d}---{current_time}---{seed}.png"

        # 更新序号
        self.image_counter += 1
        self.save_counter()
        return filename

    def download_img(self, img_data: bytes, seed: int, save_directory: str = None):
        """
        处理生成的图像数据，保存到本地文件。

        :param img_data: 图像数据
        :param seed: 生成图像的种子，附加到文件名
        :param save_directory: 可选，保存的目录，默认为 None，使用默认目录
        """
        if save_directory is None:
            root_path = os.getcwd()  # 获取当前工作目录
            save_directory = os.path.join(root_path, 'img')  # 默认保存路径为 root_path\img

        # 确保保存图像的目录存在
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # 创建 ZIP 文件对象
        try:
            with zipfile.ZipFile(BytesIO(img_data)) as zf:
                file_names = zf.namelist()

                if file_names:
                    image_filename = file_names[0]  # 获取第一个图像文件名

                    with zf.open(image_filename) as img_file:
                        img_data = img_file.read()

                        # 生成文件名，附加种子
                        filename = self.get_filename(seed)

                        date_folder = datetime.now().strftime('%Y%m%d')  # 获取当前日期（年月日）
                        image_path = os.path.join(save_directory, date_folder, filename)

                        # 确保保存图像的目录存在
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)

                        # 将图像数据保存为本地文件
                        with open(image_path, "wb") as f:
                            f.write(img_data)

                    print(f"图像已保存至: {image_path}")
                else:
                    print("ZIP文件中没有图像。")
        except Exception as e:
            print(f"下载图像时出错: {e}")




if __name__ == "__main__":
    # 配置文件路径
    config_path = "config.ini"

    # 创建图像生成器实例
    image_gen = ImageGenerator(config_path)
    角色={


        "1": "{ Shigure Kira  (Honkai Impact 3)}",
        "2": "bailu (honkai: star rail)，",
        "3": "Nachoneko",
        "4": "{{{ nachoneko （indie virtual youtuber）}}}",
        "5": "tashkent_(azur_lane)",
        "6": "{Cirno (Touhou Project)}",
        "7": "rosmontis (arknights)",
        "8": "koharu_(blue_archive)",
        "9": "{Serika (New Year) (blue archive)}",
        "10": "{ Kirara   (Genshin Impact)}",
        "11": "{Griseo (Honkai Impact 3)}",
        "12": "{Pardofelis_(honkai impact3rd)}",
        "13": "{nahida_(genshin_impact)}",
        "14": "{paimon_(genshin_impact)}",
        "15": "{yaoyao (genshin impact)}",
        "16": "{ssayu_(genshin_impact)}",
        "17": "{diona_(genshin_impact)}",
        "18": "{qiqi_(genshin_impact)}",
        "19": "{Grain Buds_(arknights)}",
        "20": "{Warmy_(arknights)}",
        "21": "{Muelsyse_(arknights)}",
        "22": "{yunjin_(genshin_impact)}",
        "23": "{Pudding_(arknights)}",
        "24": "{Aurora_(arknights)}",
        "25": "{Nine-Colored Deer_(arknights)}",
        "26": "{Kazemaru_(arknights)}",
        "27": "{Goldenglow_(arknights)}",
        "28": "{Amiya_(arknights)}",
        "29": "{Scene_(arknights)}",
        "30": "{Suzuran_(arknights)}",
        "31": "{Folinic_(arknights)}",
        "32": "{Catapult_(arknights)}",
        "33": "{Long Island_(Azur Lane )}",
        "34": "{Formidable_(Azur Lane )}",
        "35": "{Yukikaze_(Azur Lane )}",
        "36": "{Hatsushimo_(Azur Lane )}",
        "37": "{Akashi_(Azur Lane )}",
        "38": "{Shimakaze_(Azur Lane )}",
        "39": "{Kisaragi_(Azur Lane )}",
        "40": "{Kiyonami_(Azur Lane )}",
        "41": "{Hamakaze_(Azur Lane )}",
        "42": "{Arashio_(Azur Lane )}",
        "43": "{Laffey_(Azur Lane )}",
        "44": "{Makinami_(Azur Lane )}",
        "45": "{Kalk_(Azur Lane )}",
        "46": "{Stremitelny_(Azur Lane )}",
        "47": "{Kazagumo_(Diligent Domestic Discipline)_(Azur Lane )}",


    }
    画风={
        "1": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99],",
        "2": " [artist:weri],[artist:hiten],[artist:himitsu_()hi_mi_tsu_2)],[artist:chen bin],[artist:hong_bai],[artist:misheng_liu_yin],[artist:bigxixi]",
        "3": "[artist:ningen_mame], [artist:weri],[artist:hiten],[artist:himitsu_()hi_mi_tsu_2)],[artist:sho_(sho_lwlw)],[[artist:rhasta]], [artist:wlop],[artist:ke-ta]",
        "4": "[artist:henreader],[artist:rhasta],[[artist:allenes]],[artist:chen bin],[artist:shirosei_mochi]\n",
        "5": "[artist:ningen_mame], {{ciloranko}}, [artist:sho_(sho_lwlw)],[[artist:rhasta]], [artist:wlop],[artist:ke-ta],\n",
        "6": "artist:ciloranko, [artist:tianliang duohe fangdongye], [artist:sho_(sho_lwlw)], [artist:baku-p], [artist:tsubasa_tsubasa],"
    }
    质量="best quality, amazing quality, very aesthetic, absurdres"
    # 设置提示词
    动作={
        "1": "1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,green eyes,{loli},ahoge,looking at viewer,standing on one leg,blush,standing,parted lips,leg up, cowboy shot, {{close-up}}, ,no_panties,tuncensored,pussy ,{Sneakers},{{Pussy object  insertion}},{sex},{anus},{Very thick carrot},{Orgasm}, {shivering},{bedroom},Full body portrait",
        "2": "1girl,loli,ass focus,(see-through,white pantyhose),side lying,looking at viewer,from below,{{Cat ears}},{sex},{nsfw},{no panties},Pussy, anus,{ Thick Tentacles}, {{Anal insertion}},{No tail},{{Tentacle anal insertion}},clothes_pull,",
        "3": "1girl, navel, clothes lift, lying,  closed eyes, from below,clothes pull,blush, thighs, shirt lift, on bed, open mouth, underboob, pillow, 1boy, sleeping, indoors, skirt lift,sundress,ong hair,cat ear fluff,cat ears,lightblue hair,(loli:1.1),ahoge,blush,two side up，night,pussy，spread legs,nsfw, best quality, amazing quality, very aesthetic, absurdres,Full body portrait",
        "4": " {{white stockings}}, {{no underwear}},{No obstruction}, amazing quality, very aesthetic, absurdres, girl, solo, loli, cozy anime bedroom, pastel pink, lavender, and mint green tones, modern furniture with anime-inspired details,  warm and inviting vibe, {no trademark}}, {{no text}}, {{no copyright mark}},{{sitting position}},{spread legs}，{Look at the audience},{sex},{{masturbation}},{Clitoris}, {Anus},{{Shy}},{{ angry}}, {{endure}}, {{pain}}, {{cry}}, {{heartbroken}},{{desperation}},{{Sex toys}}",
        "5": "1girl,solo,long hair,cat ear fluff,cat ears,(loli:1.1),ahoge ,[[[two side up]]],underwear,bra,ass,white bra,panties,blush,bow,open mouth,braid,bottomless,trembling,white panties,indoors,female pervert,hair bow,pervert,holding,sweat,sideboob,dutch angle,wavy mouth,panties removed,standing,pink shirt,from side,side braid,shirt,underwear only, best quality, amazing quality, very aesthetic, absurdres",
        "6": "eyes_closed,pussy,1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,(loli:1.1),ahoge,[[[two side up]]],1girl,t-shirt,nsfw,cameltoe,\n",
        "7": "1girl,solo,long hair,cat ear fluff,cat ears,(loli:1.1),ahoge,blush,white t-shirt,{{Masturbation}},[[[two side up]]],lie prone on the sofa,clothes are littered,best quality, amazing quality, very aesthetic, absurdres,{Orgasm}, {trembling}, {blushing},{open clothes},pussy, anus,{Urine leaks from the vagina}, {{Semen flows out of the anus}},",
        "8": "1girl,solo,long hair,cat ear fluff,cat ears,(loli:1.1),ahoge ,[[[two side up]]],anus,ass,black_legwear,blurry_background,book,bookshelf,clothes_pull,feet,legs,legs_up,library,multiple_girls,no_panties,no_shoes,pantyhose,pleated_skirt,pussy,sitting,skirt,soles,thighs,toes,uncensored",
        "9": "1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,green eyes,{loli},ahoge ,[[[two side up]]],anus,legs_up,no_panties,pussy,sitting,tuncensored, White silk stockings,{{All fours}},{{View from the back}},{{look behind}}, {{Very thick tentacle}}, {{  tentacle anal insertion}},{sex},{{depth insert}},Bedroom,night,pleated_skirt,{Trembling}, {crying}, {scared},{blush},{extremely painful},{{extremely painful expression}},Insert slowly",
        "10": "{{all fours}},white stockings, {no underwear}},amazing quality, very aesthetic, absurdres,A girl, solo, loli, {{White socks}},{{sneakers}},{{tentacles}},{{nsfw}},{{All fours}},{{sexual intercourse}}, {{anal sex}},{{back view}}, {{naked lower body}},",
        "11": "1girl, naked shirt,fake animal ears,pink panties,off-shoulder shirt, smile,shy,blush,looking at viewer, lying,face focus, pov, indoors,stuffed animal,stuffed toy,chick,sunlight,\n",
        "12": "A girl, solo, loli, bedroom, Small leg lift, White silk socks, {Pink underwear}, Leg slightly rais"

    }


    # 生成图像

    image_gen.generate_img(proportional="竖向",角色=角色,画风=画风,动作=动作,质量=质量,)

import json
import sys
import os
from loguru import logger
#项目模块导入

from app.utils.fozu import 佛祖保佑
from app.utils.tag import 提示词生成器
from app.utils.load_ai_tags import 加载提示词组
def init_log(level):
    # 日志配置

    logger.remove()
    logger.add(sys.stdout, level=level)
class mainapi:
    def __init__(self,**参数):
        self.root_dir=os.getcwd()
        logger.info(f"当前路径: {self.root_dir}")
        # 从参数获取各项配置

        角色 = 参数.get("角色", None)
        质量 = 参数.get("质量",None)
        动作 = 参数.get("动作",None)
        画风 = 参数.get("画风", None)

        角色是否可无 = 参数.get("角色是否可无", False)
        角色获取方式 = 参数.get("角色获取方式", "随机")
        动作获取方式 = 参数.get("动作获取方式", "随机")
        画风获取方式 = 参数.get("画风获取方式", "随机")
        是否指定画风 = 参数.get("是否指定画风", False)
        是否指定角色 = 参数.get("是否指定角色", False)
        是否指定动作 = 参数.get("是否指定动作", False)
        # 是否撞库画师 = 参数.get("是否撞库画师", False)
        # 完整提示词组列表 = 参数.get("完整提示词组列表", None)
        提示词组_缓存 = 参数.get("提示词组_缓存", False)
        提示词生成参数= {
            "角色是否可无":角色是否可无,
            "角色获取方式":角色获取方式,
            "动作获取方式":动作获取方式,
            "画风获取方式":画风获取方式,
            "是否指定画风":是否指定画风,
            "是否指定角色":是否指定角色,
            "是否指定动作":是否指定动作,
            "是否撞库画师":是否撞库画师,
            "质量":质量,
            "画风":画风,
            "root_dir":self.root_dir,
         }
        if 角色:
            提示词生成参数["角色"]=角色
        if 动作:
            提示词生成参数["动作"]=动作

        if 完整提示词组列表:
            提示词生成参数["完整提示词组"]=完整提示词组列表
        if 提示词组_缓存:
            提示词生成参数["提示词组_缓存"]=提示词组_缓存
        logger.info(f"提示词生成参数:{提示词生成参数}")
        self.提示词生成器实例= 提示词生成器(**提示词生成参数)








    def main(self,参数,test=False):
        if test:
            from app.comfyui_api.comfyui_api_t import ComfyUI_API as comfyui_api,多实例多URL批量生成
        else:
            from app.comfyui_api.comfyui_api import ComfyUI_API as comfyui_api,多实例多URL批量生成
            if not 多实例多URL批量生成:
                exit(114514)


        佛祖保佑()
        # api=comfyui_api(self.提示词生成器实例,"mrnf-api",根目录=self.root_dir)
        # from app.comfyui_api.comfyui_api_t import 多实例多URL批量生成
        # api.批量生成(url="https://declared-cambridge-hostel-acceptance.trycloudflare.com/api/prompt",批量生成次数=3)
        多实例多URL批量生成(参数)


if __name__ == '__main__':
    使用ai_tags=True
    test= True

    if test:
        init_log("DEBUG")
    else:
        init_log("INFO")

    是否撞库画师 = False

    佛祖保佑()

    tags位置 = f"./data/tags.json"
    # tags位置 = f"./data/ai-tags.json"
    tags_file_path = tags位置
    完整提示词组列表= []
    ai_t_path = r"D:\xm\nai3_auto_generate_image\data\tags"
    加载提示词组(ai_t_path, 完整提示词组列表=完整提示词组列表)
    # logger.info(f"完整提示词组:{str(完整提示词组列表)[:1000]}")
    with open(tags_file_path, "r", encoding="utf-8") as file:
        tags = json.load(file)
        角色 = tags['角色']
        画风 = tags['画风']
        动作 = tags['动作']
        质量 = tags['质量']
    if 使用ai_tags:
        参数={
              "画风":画风,
              "质量":质量,
              "角色是否可无":False,
              "角色获取方式":"随机",
              "动作获取方式":"随机",
              "画风获取方式":"随机",
              "是否指定画风":False,
              "是否指定角色":False,
              "是否指定动作":False,
              "是否撞库画师":是否撞库画师,
              "完整提示词组":完整提示词组列表,
              "提示词组_缓存":True,
        }
    else:
        参数={"角色":角色,
              "画风":画风,
              "质量":质量,
              "动作":动作,
              "角色是否可无":False,
              "角色获取方式":"随机",
              "动作获取方式":"随机",
              "画风获取方式":"随机",
              "是否指定画风":False,
              "是否指定角色":False,
              "是否指定动作":False,
              "是否撞库画师":是否撞库画师,
              }
    main=mainapi(**参数)
    输入1={
        "画风":"tsubasa tsubasa",
        # "画风":"tsubasa tsubasa ,chen_bin,tianliang_duohe_fangdongye",
        # "画风":"artist:ciloranko, [artist:tianliang duohe fangdongye], [artist:sho_(sho_lwlw)], [artist:baku-p], [artist:tsubasa_tsubasa]",
        # "角色":r"laffey ii \\(azur lane\\),long_hair,white hair,red eyes,blue hairband, blue ribbon,",
        # "动作权重":True
    }
    输入2={
        # "角色":"1girl, solo, loli, petite, child, (black long hair:1.3), almond eyes, upturned eyes, bangs, (light blue short transparent Hanfu:1.2), white lining, bamboo leaf embroidery, pink leather belt, wooden amulet (bamboo leaf pattern), bamboo bracelet (left wrist), (green and white sneakers:1.2), delicate face, tiny hands, (skin texture visible through hanfu:1.1), hair luster, realism, rich details, cinematic lighting, violet eyes, mole under left eye, sword brooch, jade pendant, bandage (knee or elbow), highly detailed face, highly detailed eyes, youthful appearance,Dull skin, delicate skin, (sneaker details: textured rubber sole, breathable mesh upper, visible stitching, subtle logo),skin texture,  delicate face, small hands," ,
        # "角色":"1girl, solo, loli, petite, black long hair, almond eyes, bangs, wide sleeves, sleeves fluttering, white, delicate face, small hands,, skin texture, hair luster,child,(Light Green short transparent Hanfu:1.2),white lining,bamboo leaf embroidery,pink leather belt,wooden amulet (bamboo leaf pattern),bamboo bracelet (left wrist),(green and white sneakers:1.2),delicate face,tiny hands,(skin texture visible through hanfu:1.1),hair luster,realism,rich details,cinematic lighting,violet eyes,mole under left eye,sword brooch,jade pendant,bandage (knee or elbow),highly detailed face,highly detailed eyes,youthful appearance,Dull skin,delicate skin,(sneaker details: textured rubber sole,breathable mesh upper,visible stitching,subtle logo),",
        # "角色":"1girl, solo, loli, petite,child,, black long hair, almond eyes, bangs,  bamboo leaf embroidery, wide sleeves, sleeves fluttering, , delicate face, small hands, skin texture, hair luster, (light blue short transparent Hanfu:1.2), white lining, , pink leather belt, wooden amulet (bamboo leaf pattern), bamboo bracelet (left wrist), (green and white sneakers:1.2), delicate face, tiny hands, (skin texture visible through hanfu:1.1), hair luster, realism, rich details, cinematic lighting, violet eyes, mole under left eye, bamboo sword brooch, jade pendant, jade hairpin, bandage (knee or elbow), highly detailed face, highly detailed eyes, youthful appearance,Dull skin, delicate skin, (sneaker details: textured rubber sole, breathable mesh upper, visible stitching, subtle logo), ",
        "画风":"tsubasa tsubasa",
        # "画风":"tsubasa tsubasa ,chen_bin,tianliang_duohe_fangdongye",

        # "画风":"artist:ciloranko, [artist:tianliang duohe fangdongye], [artist:sho_(sho_lwlw)], [artist:baku-p], [artist:tsubasa_tsubasa]",
        # "动作权重":True
    }
    输入3={
        "画风":"tsubasa tsubasa",
        # "画风":"tsubasa tsubasa ,chen_bin,tianliang_duohe_fangdongye",

        # "画风":"artist:ciloranko, [artist:tianliang duohe fangdongye], [artist:sho_(sho_lwlw)], [artist:baku-p], [artist:tsubasa_tsubasa]",
        # "动作权重":True

    }

    参数={
        "客户端id":"mrnf-api",
        "根目录":main.root_dir,
        "提示词生成器实例":main.提示词生成器实例,
        "实例输入":[
            {
                "url":"https://programme-migration-stocks-fail.trycloudflare.com/api/prompt",
                "数量":10,
                "输入":输入1,
                # "工作流模板":"noobai-lora.json",
                "工作流模板":"ntr.json",
                "保存目录": "1号",
                # "单批次数":2
            },

            {
                "url":"https://cio-judges-segment-morrison.trycloudflare.com/api/prompt",
                "数量":20,
                "输入":输入2,
                "工作流模板":"ntr.json",
                "保存目录":"2号",
                # "单批次数":2
            },
            {
                "url":"https://subscriber-disclaimers-brand-seasons.trycloudflare.com/api/prompt",
                "数量":10,
                "输入":输入3,
                "工作流模板":"ntr.json",
                "保存目录":"3号",
                # "单批次数":2


            }

        ]
    }
    import hashlib
    import os
    def 生成目录名称(url):
        """
        根据 URL 生成一个 32 位以内、文本形式、唯一且相同输入相同输出的目录名称。
        """
        url_哈希 = hashlib.sha256(url.encode('utf-8')).hexdigest()  # 使用 SHA256，生成 64 位十六进制字符串
        目录名称 = url_哈希[:5]  # 截断到 32 位
        目录名称 = f"mrnf-{目录名称}"
        return 目录名称
    # 遍历实例输入，生成或读取目录名称
    for item in 参数["实例输入"]:
        item["保存目录"] = 生成目录名称(item["url"])


    main.main(参数,test=test)
    # main.提示词生成器实例.提示词组合(sd=True,**输入1)











    # animal ears, socks, pussy, loli, anus,blush, long hair, feet, looking at viewer, Take off your shoes,Shoes are steaming, soles,White stockings,  uncensored, closed mouth, animal ear fluff, cleft of venus, ass, legs, bangs, sweat, no panties, thighs, toes, very long hair, smile,, small breasts, breasts, legs up, kneehighs，best quality, amazing quality, very aesthetic, absurdres

##1girl,1boy,sex,nose blush,crying,streaming tears,open mouth,tongue out,head back,spread legs,nude,nipples,trembling,heart,from side,torso grab,motion lines,motion blur,indoors,on bed,living room,curtains


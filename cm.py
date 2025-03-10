import json
import os

from loguru import logger
from app.utils.fozu import 佛祖保佑
from app.utils.tag import 提示词生成器
from app.comfyui_api.comfyui_api import comfyui_api
class mainapi:
    def __init__(self,**参数):
        self.root_dir=os.getcwd()
        logger.info(f"当前路径: {self.root_dir}")
        # 从参数获取各项配置

        角色 = 参数.get("角色")
        质量 = 参数.get("质量")
        动作 = 参数.get("动作", "")
        角色是否可无 = 参数.get("角色是否可无", False)
        角色获取方式 = 参数.get("角色获取方式", "随机")
        动作获取方式 = 参数.get("动作获取方式", "随机")
        画风获取方式 = 参数.get("画风获取方式", "随机")
        是否指定画风 = 参数.get("是否指定画风", False)
        是否指定角色 = 参数.get("是否指定角色", False)
        是否指定动作 = 参数.get("是否指定动作", False)

        # 生成提示词
        self.提示词生成器实例 = 提示词生成器(
            角色=角色, 质量=质量, 动作=动作,
            角色是否可无=角色是否可无,
            角色获取方式=角色获取方式,
            动作获取方式=动作获取方式,
            画风获取方式=画风获取方式,
            root_dir=self.root_dir,
            是否指定画风=是否指定画风,
            是否指定角色=是否指定角色,
            是否指定动作=是否指定动作
        )
    def main(self,参数):
        api=comfyui_api(self.提示词生成器实例,"mrnf-api",root_dir=self.root_dir)

        # api.批量生成(url="https://declared-cambridge-hostel-acceptance.trycloudflare.com/api/prompt",批量生成次数=3)
        api.多url批量生成(参数)


if __name__ == '__main__':

    佛祖保佑()
    tags位置 = f"./data/tags.json"
    tags_file_path = tags位置
    with open(tags_file_path, "r", encoding="utf-8") as file:
        tags = json.load(file)
        角色 = tags['角色']
        画风 = tags['画风']
        动作 = tags['动作']
        质量 = tags['质量']
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
              }

    main=mainapi(**参数)
    参数=[
        {
            "url":"https://replica-voltage-insider-versus.trycloudflare.com/api/prompt",
            "数量":10
        },
        {
            "url":"https://efforts-subsidiary-habits-affiliation.trycloudflare.com/api/prompt",
            "数量":10
        },
        {
            "url":"https://declared-cambridge-hostel-acceptance.trycloudflare.com/api/prompt",
            "数量":10
        }
    ]
    main.main(参数)



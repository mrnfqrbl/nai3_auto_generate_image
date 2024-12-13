### novelai 自动生成图片 支持随机角色 动作 艺术家等
### 提示 bug未知我用着没问题  有可能bug会导致点数额外消耗   目前我使用着没问题  tags.json文件不会导致额外点数消耗 只负责存储提示词
### 乱改可能会导致额外点数消耗
### 正常使用暂时未发现点数额外消耗问题(除了一开始测试填错api参数消耗了100点数)
### 重要提示 切记不要乱改 novelai_api.py  以及main中调用 novelai_api.py 的部分 
首次 启动生成 cofig.ini和 tags.json
修改后启动

## 使用方法

# 1.cmd 安装依赖

```cmd
pip install -r requirements.txt
```

或者

```cmd
python -m pip install -r requirements.txt
```

# 2.配置文件

先运行 main.py

```cmd
python main.py
```

然后配置congif.ini中的参数
ini配置 ：
```ini
[API]
# 这里填novelai令牌
token = 你的api令牌
      
[GENERATION]
# 这里生成的总次数，同时只能生成一张 同时2需要额外点数 
如果不是无限小图的订阅不要设置太大的数量
quantity = 10
```

# 3.配置tags.json

示例 注意：tags.josn 内容保持默认无法启动 起码修改一下

```json
{
  "__注释": "角色：为你喜欢的角色格式如下，画风：为艺术家组合同下，动作：为除开角色画风的其余部分包括服装动作等以及需要叠加覆盖的人物特征，质量：指定生成图片质量的一般不需要改",
  "角色": {
    "1": "{yaoyao (genshin impact)}",
    "2": "bailu (honkai: star rail)",
    "3": "bailu (honkai: star rail)"
  },
  "画风": {
    "1": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]",
    "2": "[artist:sho_(sho_lwlw)], artist:wlop, [artist:aki99]"
  },
  "动作": {
    "1": "1girl,solo,long hair,cat ear fluff,cat ears,lightblue hair,green eyes,{loli},ahoge,looking at viewer,standing on one leg,blush,standing,parted lips,leg up, cowboy shot, {{close-up}}, ,no_panties,tuncensored,pussy ,{Sneakers},{{Pussy object  insertion}},{sex},{anus},{Very thick carrot},{Orgasm}, {shivering},{bedroom},Full body portrait",
    "2": "1girl,loli,ass focus,(see-through,white pantyhose),side lying,looking at viewer,from below,{{Cat ears}},{sex},{nsfw},{no panties},Pussy, anus,{ Thick Tentacles}, {{Anal insertion}},{No tail},{{Tentacle anal insertion}},clothes_pull,"
  },
  "质量": "best quality, amazing quality, very aesthetic, absurdres"
}
```

# 4.运行

```cmd  
python main.py
```



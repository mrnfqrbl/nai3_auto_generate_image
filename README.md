### novelai 自动生成图片 支持随机角色 动作 艺术家等
### 提示 bug未知我用着没问题  有可能bug会导致点数额外消耗   目前我使用着没问题  tags.json文件不会导致额外点数消耗 只负责存储提示词
### 乱改可能会导致额外点数消耗
### 重要提示 切记不要乱改 novelai_api.py  以及main中调用 novelai_api.py 的部分 
首次 启动生成 cofig.ini和 tags.json
修改后启动
ini配置 
[API]
# 这里填novelai令牌
token = 你的api令牌

[GENERATION]
# 这里生成的总次数，同时只能生成一张 同时2需要额外点数 
如果不是无限小图的订阅不要设置太大的数量
quantity = 10

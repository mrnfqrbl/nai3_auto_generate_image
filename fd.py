import asyncio
import os.path

from app.api.Api_Operation import ApiOperation

def mian():
    api=ApiOperation(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj",环境="正式")
    图片所在目录=r"W:\放大输入sd"
    保存路径=r"W:\放大输出sd"
    if not os.path.exists(保存路径):
        os.mkdir(保存路径)
    放大倍数=4


    asyncio.run(api.批量放大图片(**{"放大倍数":放大倍数,"图片所在目录":图片所在目录,"保存路径":保存路径,"成功后是否删除原图":True}))




if __name__ == '__main__':
    mian()
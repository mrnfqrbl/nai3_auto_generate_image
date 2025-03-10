import asyncio


from api import NovelAIAPI

api=NovelAIAPI(__token="pst-YUJeMro0TENiUqkk76EcANMQpNKvbXkCiMtXRa8kPdWtNLr8ZSha5oKeY6gUQrCj",环境="代理" )
userdata=asyncio.run(api.api_get_user_data())
print(f"用户数据：{userdata}")
json={
"input": "1girl,loli,ke qinng(genshin-impart)，nekd",
"model": "nai-diffusion-3",
"action": "generate",
"parameters": {
"width": 832,
"height": 1216,
"scale": 5,
"sampler": "k_euler_ancestral",
"steps": 28,
"seed": 0,
"n_samples": 1,
"negative_prompt": "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], underwear",
"qualityToggle": True,
"sm": False,
"sm_dyn": False,
"dynamic_thresholding": False,
"legacy": False,
"cfg_rescale": 0,
"controlnet_strength": 1,
"noise_schedule": "karras",
"legacy_v3_extend": False,
"skip_cfg_above_sigma": None
}
}

imgdata=asyncio.run(api.api_generate_image(json))
from app.utils.utils import save_image
save_image(imgdata,"./dev_img", "555.png")


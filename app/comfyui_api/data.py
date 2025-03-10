# -*- coding: utf-8 -*-
data = {
    "client_id": "ab78ba85e6e74d188d5fdd68b367da83",
    "prompt": {
        "4": {
            "inputs": {
                "text": "Scene_(arknights),(artist: shpo:0.7),(artist: mikaze_oto:0.6),(artist: ponytail_korosuke:0.7),(:0.6),(toddler:1.4),Sitting on the bed,hospital_(place),1girl,loli,petite,Lolita,(white stockings:1.1),(be shy:1.2),light blush,(😆:1.1),(sweating:1.5),foot focus,(Sweaty feet:1.4),quality,amazing quality,very aesthetic,(absurdres:1.3),reverse light,golden light,(:1.2)，best quality, amazing quality, very aesthetic, absurdres",
                "clip": [
                    "17",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP文本编码"
            }
        },
        "5": {
            "inputs": {
                "text": "worst quality, low quality, normal quality, low contrast, blurry, pixelated, overcompressed,underwear,Wrong number of fingers, stuck fingers, twisted limbs, wrong limbs, wrong eyes, asymmetrical eyes,Skin reflection, skin radiance,logo,text,\n",
                "clip": [
                    "17",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP文本编码"
            }
        },
        "8": {
            "inputs": {
                "samples": [
                    "53",
                    0
                ],
                "vae": [
                    "17",
                    2
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE解码"
            }
        },
        "15": {
            "inputs": {
                "width": [
                    "95",
                    0
                ],
                "height": [
                    "84",
                    0
                ],
                "batch_size": 2
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
                "title": "空Latent图像"
            }
        },
        "17": {
            "inputs": {
                "ckpt_name": "ntrMIXIllustriousXL_xiii.safetensors"
            },
            "class_type": "unCLIPCheckpointLoader",
            "_meta": {
                "title": "unCLIPCheckpoint加载器"
            }
        },
        "39": {
            "inputs": {
                "filename_prefix": "线程1",
                "filename_keys": "%H-%M-%S",
                "foldername_prefix": "",
                "foldername_keys": "%F",
                "delimiter": "-",
                "save_job_data": "disabled",
                "job_data_per_image": false,
                "job_custom_text": "",
                "save_metadata": true,
                "counter_digits": 4,
                "counter_position": "first",
                "one_counter_per_folder": true,
                "image_preview": true,
                "output_ext": ".png",
                "quality": 90,
                "named_keys": false,
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImageExtended",
            "_meta": {
                "title": "💾 保存图像扩展 2.83"
            }
        },
        "53": {
            "inputs": {
                "seed": 998081383335724,
                "steps": 35,
                "cfg": 5,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "17",
                    0
                ],
                "positive": [
                    "77",
                    0
                ],
                "negative": [
                    "78",
                    0
                ],
                "latent_image": [
                    "15",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "K采样器"
            }
        },
        "68": {
            "inputs": {
                "control_net_name": "XL_Thibaud姿势.safetensors"
            },
            "class_type": "ControlNetLoader",
            "_meta": {
                "title": "加载ControlNet模型"
            }
        },
        "69": {
            "inputs": {
                "strength": 1.01,
                "start_percent": 0,
                "end_percent": 1,
                "positive": [
                    "4",
                    0
                ],
                "negative": [
                    "5",
                    0
                ],
                "control_net": [
                    "68",
                    0
                ],
                "vae": [
                    "17",
                    2
                ],
                "image": [
                    "71",
                    0
                ]
            },
            "class_type": "ControlNetApplySD3",
            "_meta": {
                "title": "应用ControlNet"
            }
        },
        "71": {
            "inputs": {
                "image": "ComfyUI_OpenPose_71.png",
                "savedPose": "{\n    \"width\": 512,\n    \"height\": 512,\n    \"keypoints\": [\n        [\n            [\n                230.96099290780137,\n                97.82624113475183\n            ],\n            [\n                230.96099290780137,\n                141.73404255319156\n            ],\n            [\n                180.96099290780137,\n                138.82624113475183\n            ],\n            [\n                166.96099290780137,\n                203.82624113475183\n            ],\n            [\n                73.98226950354606,\n                146.64184397163126\n            ],\n            [\n                287.96099290780137,\n                138.82624113475183\n            ],\n            [\n                306.96099290780137,\n                202.82624113475183\n            ],\n            [\n                382.7836879432624,\n                128.74822695035468\n            ],\n            [\n                214.96099290780137,\n                261.82624113475185\n            ],\n            [\n                208.40780141843965,\n                320.81914893617034\n            ],\n            [\n                205.86879432624107,\n                442.1453900709221\n            ],\n            [\n                259.96099290780137,\n                260.82624113475185\n            ],\n            [\n                266.5141843971631,\n                328.17375886524826\n            ],\n            [\n                265.06737588652476,\n                445.9609929078015\n            ],\n            [\n                221.96099290780137,\n                79.82624113475183\n            ],\n            [\n                242.96099290780137,\n                80.82624113475183\n            ],\n            [\n                214.96099290780137,\n                90.82624113475183\n            ],\n            [\n                249.96099290780137,\n                92.82624113475183\n            ]\n        ]\n    ]\n}",
                "open editor": "image"
            },
            "class_type": "OpenPoseEditorAdv",
            "_meta": {
                "title": "OpenPoseEditorAdv"
            }
        },
        "77": {
            "inputs": {
                "boolean": false,
                "on_true": [
                    "69",
                    0
                ],
                "on_false": [
                    "4",
                    0
                ]
            },
            "class_type": "Switch conditioning [Crystools]",
            "_meta": {
                "title": "🪛 Switch conditioning"
            }
        },
        "78": {
            "inputs": {
                "boolean": false,
                "on_true": [
                    "69",
                    1
                ],
                "on_false": [
                    "5",
                    0
                ]
            },
            "class_type": "Switch conditioning [Crystools]",
            "_meta": {
                "title": "🪛 Switch conditioning"
            }
        },
        "84": {
            "inputs": {
                "boolean": [
                    "97",
                    0
                ],
                "on_true": [
                    "96",
                    0
                ],
                "on_false": [
                    "94",
                    0
                ]
            },
            "class_type": "Switch any [Crystools]",
            "_meta": {
                "title": "🪛 Switch any"
            }
        },
        "94": {
            "inputs": {
                "int": 1000
            },
            "class_type": "Primitive integer [Crystools]",
            "_meta": {
                "title": "🪛 Primitive integer"
            }
        },
        "95": {
            "inputs": {
                "boolean": [
                    "97",
                    0
                ],
                "on_true": [
                    "94",
                    0
                ],
                "on_false": [
                    "96",
                    0
                ]
            },
            "class_type": "Switch any [Crystools]",
            "_meta": {
                "title": "🪛 Switch any"
            }
        },
        "96": {
            "inputs": {
                "int": 1464
            },
            "class_type": "Primitive integer [Crystools]",
            "_meta": {
                "title": "🪛 Primitive integer"
            }
        },
        "97": {
            "inputs": {
                "boolean": true
            },
            "class_type": "Primitive boolean [Crystools]",
            "_meta": {
                "title": "尺寸，true为竖向"
            }
        },
        "98": {
            "inputs": {
                "text": "Hitori Gotoh  (Bocchi the Rock),(artist:ciloranko:0.6),(artist:tianliang duohe fangdongye:0.6),(artist:sho_(sho_lwlw):0.7),(artist:baku-p:0.6),(artist:tsubasa_tsubasa:0.6),(:0.6),1girl,(navel:1.2),(clothes lift:1.2),(lying:1.2),closed eyes,(from below:1.1),(clothes pull:1.5),(blush:1.3),thighs,(shirt lift:1.3),on bed,(open mouth:1.3),(underboob:1.3),(pillow:1.2),1boy,(sleeping:1.3),(indoors:1.2),(skirt lift:1.2),sundress,(ong hair:1.3),(cat ear fluff:1.5),cat ears,lightblue hair,((loli:1.1):1.3),(ahoge:1.3),(blush:1.2),two side up，night,pussy，spread legs,nsfw,(best quality:1.1),amazing quality,(very aesthetic:1.2),(absurdres:1.5),Full body portrait，best quality, amazing quality, very aesthetic, absurdres",
                "clip": [
                    "17",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP文本编码"
            }
        },
        "99": {
            "inputs": {
                "seed": 251910039712713,
                "steps": 35,
                "cfg": 5,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "17",
                    0
                ],
                "positive": [
                    "98",
                    0
                ],
                "negative": [
                    "5",
                    0
                ],
                "latent_image": [
                    "15",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "K采样器"
            }
        },
        "100": {
            "inputs": {
                "samples": [
                    "99",
                    0
                ],
                "vae": [
                    "17",
                    2
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE解码"
            }
        },
        "101": {
            "inputs": {
                "filename_prefix": "线程2",
                "filename_keys": "%H-%M-%S",
                "foldername_prefix": "",
                "foldername_keys": "%F",
                "delimiter": "-",
                "save_job_data": "disabled",
                "job_data_per_image": false,
                "job_custom_text": "",
                "save_metadata": true,
                "counter_digits": 4,
                "counter_position": "first",
                "one_counter_per_folder": true,
                "image_preview": true,
                "output_ext": ".png",
                "quality": 90,
                "named_keys": false,
                "images": [
                    "100",
                    0
                ]
            },
            "class_type": "SaveImageExtended",
            "_meta": {
                "title": "💾 保存图像扩展 2.83"
            }
        }
    },
    "extra_data": {
        "extra_pnginfo": {
            "workflow": {
                "last_node_id": 101,
                "last_link_id": 127,
                "nodes": [
                    {
                        "id": 4,
                        "type": "CLIPTextEncode",
                        "pos": [
                            -259.67694091796875,
                            -51.28164291381836
                        ],
                        "size": [
                            400,
                            200
                        ],
                        "flags": {},
                        "order": 8,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "clip",
                                "type": "CLIP",
                                "link": 66
                            }
                        ],
                        "outputs": [
                            {
                                "name": "CONDITIONING",
                                "type": "CONDITIONING",
                                "links": [
                                    89,
                                    99
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "CLIPTextEncode"
                        },
                        "widgets_values": [
                            "Scene_(arknights),(artist: shpo:0.7),(artist: mikaze_oto:0.6),(artist: ponytail_korosuke:0.7),(:0.6),(toddler:1.4),Sitting on the bed,hospital_(place),1girl,loli,petite,Lolita,(white stockings:1.1),(be shy:1.2),light blush,(😆:1.1),(sweating:1.5),foot focus,(Sweaty feet:1.4),quality,amazing quality,very aesthetic,(absurdres:1.3),reverse light,golden light,(:1.2)，best quality, amazing quality, very aesthetic, absurdres"
                        ]
                    },
                    {
                        "id": 5,
                        "type": "CLIPTextEncode",
                        "pos": [
                            -256.6614990234375,
                            205.33236694335938
                        ],
                        "size": [
                            400,
                            200
                        ],
                        "flags": {},
                        "order": 7,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "clip",
                                "type": "CLIP",
                                "link": 65
                            }
                        ],
                        "outputs": [
                            {
                                "name": "CONDITIONING",
                                "type": "CONDITIONING",
                                "links": [
                                    90,
                                    102,
                                    122
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "CLIPTextEncode"
                        },
                        "widgets_values": [
                            "worst quality, low quality, normal quality, low contrast, blurry, pixelated, overcompressed,underwear,Wrong number of fingers, stuck fingers, twisted limbs, wrong limbs, wrong eyes, asymmetrical eyes,Skin reflection, skin radiance,logo,text,\n"
                        ]
                    },
                    {
                        "id": 8,
                        "type": "VAEDecode",
                        "pos": [
                            1280.364013671875,
                            328.89813232421875
                        ],
                        "size": [
                            210,
                            46
                        ],
                        "flags": {
                            "collapsed": false
                        },
                        "order": 19,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "samples",
                                "type": "LATENT",
                                "link": 82
                            },
                            {
                                "name": "vae",
                                "type": "VAE",
                                "link": 23
                            }
                        ],
                        "outputs": [
                            {
                                "name": "IMAGE",
                                "type": "IMAGE",
                                "links": [
                                    58
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "VAEDecode"
                        },
                        "widgets_values": []
                    },
                    {
                        "id": 15,
                        "type": "EmptyLatentImage",
                        "pos": [
                            -589.6838989257812,
                            256.5370178222656
                        ],
                        "size": [
                            315,
                            106
                        ],
                        "flags": {},
                        "order": 13,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "width",
                                "type": "INT",
                                "link": 108,
                                "widget": {
                                    "name": "width"
                                }
                            },
                            {
                                "name": "height",
                                "type": "INT",
                                "link": 107,
                                "widget": {
                                    "name": "height"
                                }
                            }
                        ],
                        "outputs": [
                            {
                                "name": "LATENT",
                                "type": "LATENT",
                                "links": [
                                    63,
                                    124
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "EmptyLatentImage"
                        },
                        "widgets_values": [
                            1000,
                            1464,
                            2
                        ]
                    },
                    {
                        "id": 17,
                        "type": "unCLIPCheckpointLoader",
                        "pos": [
                            -593.1478881835938,
                            100.24862670898438
                        ],
                        "size": [
                            315,
                            118
                        ],
                        "flags": {},
                        "order": 4,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "MODEL",
                                "type": "MODEL",
                                "links": [
                                    71,
                                    123
                                ],
                                "slot_index": 0
                            },
                            {
                                "name": "CLIP",
                                "type": "CLIP",
                                "links": [
                                    65,
                                    66,
                                    120
                                ],
                                "slot_index": 1
                            },
                            {
                                "name": "VAE",
                                "type": "VAE",
                                "links": [
                                    23,
                                    93,
                                    127
                                ],
                                "slot_index": 2
                            },
                            {
                                "name": "CLIP_VISION",
                                "type": "CLIP_VISION",
                                "links": null
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "unCLIPCheckpointLoader"
                        },
                        "widgets_values": [
                            "ntrMIXIllustriousXL_xiii.safetensors"
                        ]
                    },
                    {
                        "id": 39,
                        "type": "SaveImageExtended",
                        "pos": [
                            1691.932861328125,
                            244.24986267089844
                        ],
                        "size": [
                            400,
                            722
                        ],
                        "flags": {},
                        "order": 21,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "images",
                                "type": "IMAGE",
                                "link": 58
                            },
                            {
                                "name": "positive_text_opt",
                                "type": "STRING",
                                "link": null,
                                "widget": {
                                    "name": "positive_text_opt"
                                },
                                "shape": 7
                            },
                            {
                                "name": "negative_text_opt",
                                "type": "STRING",
                                "link": null,
                                "widget": {
                                    "name": "negative_text_opt"
                                },
                                "shape": 7
                            }
                        ],
                        "outputs": [],
                        "title": "💾 保存图像扩展 2.83",
                        "properties": {
                            "Node name for S&R": "SaveImageExtended"
                        },
                        "widgets_values": [
                            "线程1",
                            "%H-%M-%S",
                            "",
                            "%F",
                            "-",
                            "disabled",
                            false,
                            "",
                            true,
                            4,
                            "first",
                            true,
                            true,
                            ".png",
                            90,
                            false,
                            "",
                            ""
                        ]
                    },
                    {
                        "id": 53,
                        "type": "KSampler",
                        "pos": [
                            155.623291015625,
                            165.69898986816406
                        ],
                        "size": [
                            315,
                            262
                        ],
                        "flags": {},
                        "order": 17,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "model",
                                "type": "MODEL",
                                "link": 71
                            },
                            {
                                "name": "positive",
                                "type": "CONDITIONING",
                                "link": 97
                            },
                            {
                                "name": "negative",
                                "type": "CONDITIONING",
                                "link": 103
                            },
                            {
                                "name": "latent_image",
                                "type": "LATENT",
                                "link": 63
                            }
                        ],
                        "outputs": [
                            {
                                "name": "LATENT",
                                "type": "LATENT",
                                "links": [
                                    82
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "KSampler"
                        },
                        "widgets_values": [
                            998081383335724,
                            "randomize",
                            35,
                            5,
                            "euler",
                            "normal",
                            1
                        ]
                    },
                    {
                        "id": 68,
                        "type": "ControlNetLoader",
                        "pos": [
                            -593.1876220703125,
                            5.6874823570251465
                        ],
                        "size": [
                            315,
                            58
                        ],
                        "flags": {},
                        "order": 1,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "CONTROL_NET",
                                "type": "CONTROL_NET",
                                "links": [
                                    88
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "ControlNetLoader"
                        },
                        "widgets_values": [
                            "XL_Thibaud姿势.safetensors"
                        ]
                    },
                    {
                        "id": 69,
                        "type": "ControlNetApplySD3",
                        "pos": [
                            488.5636291503906,
                            -163.13917541503906
                        ],
                        "size": [
                            315,
                            186
                        ],
                        "flags": {},
                        "order": 12,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "positive",
                                "type": "CONDITIONING",
                                "link": 89
                            },
                            {
                                "name": "negative",
                                "type": "CONDITIONING",
                                "link": 90
                            },
                            {
                                "name": "control_net",
                                "type": "CONTROL_NET",
                                "link": 88
                            },
                            {
                                "name": "vae",
                                "type": "VAE",
                                "link": 93
                            },
                            {
                                "name": "image",
                                "type": "IMAGE",
                                "link": 94
                            }
                        ],
                        "outputs": [
                            {
                                "name": "positive",
                                "type": "CONDITIONING",
                                "links": [
                                    98
                                ],
                                "slot_index": 0
                            },
                            {
                                "name": "negative",
                                "type": "CONDITIONING",
                                "links": [
                                    101
                                ],
                                "slot_index": 1
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "ControlNetApplySD3"
                        },
                        "widgets_values": [
                            1.01,
                            0,
                            1
                        ]
                    },
                    {
                        "id": 71,
                        "type": "OpenPoseEditorAdv",
                        "pos": [
                            208.2445068359375,
                            -287.90838623046875
                        ],
                        "size": [
                            210,
                            314
                        ],
                        "flags": {},
                        "order": 0,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "IMAGE",
                                "type": "IMAGE",
                                "links": [
                                    94
                                ],
                                "slot_index": 0
                            },
                            {
                                "name": "MASK_POSE_1",
                                "type": "MASK",
                                "links": null
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "OpenPoseEditorAdv",
                            "savedPose": "{\n    \"width\": 512,\n    \"height\": 512,\n    \"keypoints\": [\n        [\n            [\n                230.96099290780137,\n                97.82624113475183\n            ],\n            [\n                230.96099290780137,\n                141.73404255319156\n            ],\n            [\n                180.96099290780137,\n                138.82624113475183\n            ],\n            [\n                166.96099290780137,\n                203.82624113475183\n            ],\n            [\n                73.98226950354606,\n                146.64184397163126\n            ],\n            [\n                287.96099290780137,\n                138.82624113475183\n            ],\n            [\n                306.96099290780137,\n                202.82624113475183\n            ],\n            [\n                382.7836879432624,\n                128.74822695035468\n            ],\n            [\n                214.96099290780137,\n                261.82624113475185\n            ],\n            [\n                208.40780141843965,\n                320.81914893617034\n            ],\n            [\n                205.86879432624107,\n                442.1453900709221\n            ],\n            [\n                259.96099290780137,\n                260.82624113475185\n            ],\n            [\n                266.5141843971631,\n                328.17375886524826\n            ],\n            [\n                265.06737588652476,\n                445.9609929078015\n            ],\n            [\n                221.96099290780137,\n                79.82624113475183\n            ],\n            [\n                242.96099290780137,\n                80.82624113475183\n            ],\n            [\n                214.96099290780137,\n                90.82624113475183\n            ],\n            [\n                249.96099290780137,\n                92.82624113475183\n            ]\n        ]\n    ]\n}"
                        },
                        "widgets_values": [
                            "ComfyUI_OpenPose_71.png",
                            "{\n    \"width\": 512,\n    \"height\": 512,\n    \"keypoints\": [\n        [\n            [\n                230.96099290780137,\n                97.82624113475183\n            ],\n            [\n                230.96099290780137,\n                141.73404255319156\n            ],\n            [\n                180.96099290780137,\n                138.82624113475183\n            ],\n            [\n                166.96099290780137,\n                203.82624113475183\n            ],\n            [\n                73.98226950354606,\n                146.64184397163126\n            ],\n            [\n                287.96099290780137,\n                138.82624113475183\n            ],\n            [\n                306.96099290780137,\n                202.82624113475183\n            ],\n            [\n                382.7836879432624,\n                128.74822695035468\n            ],\n            [\n                214.96099290780137,\n                261.82624113475185\n            ],\n            [\n                208.40780141843965,\n                320.81914893617034\n            ],\n            [\n                205.86879432624107,\n                442.1453900709221\n            ],\n            [\n                259.96099290780137,\n                260.82624113475185\n            ],\n            [\n                266.5141843971631,\n                328.17375886524826\n            ],\n            [\n                265.06737588652476,\n                445.9609929078015\n            ],\n            [\n                221.96099290780137,\n                79.82624113475183\n            ],\n            [\n                242.96099290780137,\n                80.82624113475183\n            ],\n            [\n                214.96099290780137,\n                90.82624113475183\n            ],\n            [\n                249.96099290780137,\n                92.82624113475183\n            ]\n        ]\n    ]\n}",
                            "image"
                        ]
                    },
                    {
                        "id": 77,
                        "type": "Switch conditioning [Crystools]",
                        "pos": [
                            597.1011962890625,
                            201.22518920898438
                        ],
                        "size": [
                            315,
                            78
                        ],
                        "flags": {},
                        "order": 14,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "on_true",
                                "type": "CONDITIONING",
                                "link": 98
                            },
                            {
                                "name": "on_false",
                                "type": "CONDITIONING",
                                "link": 99
                            },
                            {
                                "name": "boolean",
                                "type": "BOOLEAN",
                                "link": 105,
                                "widget": {
                                    "name": "boolean"
                                }
                            }
                        ],
                        "outputs": [
                            {
                                "name": "conditioning",
                                "type": "CONDITIONING",
                                "links": [
                                    97
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Switch conditioning [Crystools]"
                        },
                        "widgets_values": [
                            false
                        ]
                    },
                    {
                        "id": 78,
                        "type": "Switch conditioning [Crystools]",
                        "pos": [
                            594.0582275390625,
                            336.812744140625
                        ],
                        "size": [
                            315,
                            78
                        ],
                        "flags": {},
                        "order": 15,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "on_true",
                                "type": "CONDITIONING",
                                "link": 101
                            },
                            {
                                "name": "on_false",
                                "type": "CONDITIONING",
                                "link": 102
                            },
                            {
                                "name": "boolean",
                                "type": "BOOLEAN",
                                "link": 104,
                                "widget": {
                                    "name": "boolean"
                                }
                            }
                        ],
                        "outputs": [
                            {
                                "name": "conditioning",
                                "type": "CONDITIONING",
                                "links": [
                                    103
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Switch conditioning [Crystools]"
                        },
                        "widgets_values": [
                            false
                        ]
                    },
                    {
                        "id": 80,
                        "type": "PrimitiveNode",
                        "pos": [
                            157.93997192382812,
                            69.55290222167969
                        ],
                        "size": [
                            210,
                            58
                        ],
                        "flags": {},
                        "order": 2,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "BOOLEAN",
                                "type": "BOOLEAN",
                                "links": [
                                    104,
                                    105
                                ],
                                "slot_index": 0,
                                "widget": {
                                    "name": "boolean"
                                }
                            }
                        ],
                        "title": "启用cont",
                        "properties": {
                            "Run widget replace on values": false
                        },
                        "widgets_values": [
                            false
                        ]
                    },
                    {
                        "id": 84,
                        "type": "Switch any [Crystools]",
                        "pos": [
                            -1006.738525390625,
                            231.14041137695312
                        ],
                        "size": [
                            315,
                            78
                        ],
                        "flags": {},
                        "order": 10,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "on_true",
                                "type": "*",
                                "link": 111
                            },
                            {
                                "name": "on_false",
                                "type": "*",
                                "link": 112
                            },
                            {
                                "name": "boolean",
                                "type": "BOOLEAN",
                                "link": 118,
                                "widget": {
                                    "name": "boolean"
                                }
                            }
                        ],
                        "outputs": [
                            {
                                "name": "*",
                                "type": "*",
                                "links": [
                                    107
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Switch any [Crystools]"
                        },
                        "widgets_values": [
                            true
                        ]
                    },
                    {
                        "id": 94,
                        "type": "Primitive integer [Crystools]",
                        "pos": [
                            -1524.103759765625,
                            146.18492126464844
                        ],
                        "size": [
                            315,
                            58
                        ],
                        "flags": {},
                        "order": 5,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "int",
                                "type": "INT",
                                "links": [
                                    109,
                                    112
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Primitive integer [Crystools]"
                        },
                        "widgets_values": [
                            1000
                        ]
                    },
                    {
                        "id": 95,
                        "type": "Switch any [Crystools]",
                        "pos": [
                            -1007.3460083007812,
                            106.38915252685547
                        ],
                        "size": [
                            315,
                            78
                        ],
                        "flags": {},
                        "order": 11,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "on_true",
                                "type": "*",
                                "link": 109
                            },
                            {
                                "name": "on_false",
                                "type": "*",
                                "link": 116
                            },
                            {
                                "name": "boolean",
                                "type": "BOOLEAN",
                                "link": 119,
                                "widget": {
                                    "name": "boolean"
                                }
                            }
                        ],
                        "outputs": [
                            {
                                "name": "*",
                                "type": "*",
                                "links": [
                                    108
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Switch any [Crystools]"
                        },
                        "widgets_values": [
                            true
                        ]
                    },
                    {
                        "id": 96,
                        "type": "Primitive integer [Crystools]",
                        "pos": [
                            -1524.1036376953125,
                            253.1849365234375
                        ],
                        "size": [
                            315,
                            58
                        ],
                        "flags": {},
                        "order": 6,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "int",
                                "type": "INT",
                                "links": [
                                    111,
                                    116
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "Primitive integer [Crystools]"
                        },
                        "widgets_values": [
                            1464
                        ]
                    },
                    {
                        "id": 97,
                        "type": "Primitive boolean [Crystools]",
                        "pos": [
                            -601.2947998046875,
                            405.48101806640625
                        ],
                        "size": [
                            315,
                            58
                        ],
                        "flags": {},
                        "order": 3,
                        "mode": 0,
                        "inputs": [],
                        "outputs": [
                            {
                                "name": "boolean",
                                "type": "BOOLEAN",
                                "links": [
                                    118,
                                    119
                                ],
                                "slot_index": 0
                            }
                        ],
                        "title": "尺寸，true为竖向",
                        "properties": {
                            "Node name for S&R": "Primitive boolean [Crystools]"
                        },
                        "widgets_values": [
                            true
                        ]
                    },
                    {
                        "id": 98,
                        "type": "CLIPTextEncode",
                        "pos": [
                            -259.5383605957031,
                            442.7599182128906
                        ],
                        "size": [
                            400,
                            200
                        ],
                        "flags": {},
                        "order": 9,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "clip",
                                "type": "CLIP",
                                "link": 120
                            }
                        ],
                        "outputs": [
                            {
                                "name": "CONDITIONING",
                                "type": "CONDITIONING",
                                "links": [
                                    121
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "CLIPTextEncode"
                        },
                        "widgets_values": [
                            "Hitori Gotoh  (Bocchi the Rock),(artist:ciloranko:0.6),(artist:tianliang duohe fangdongye:0.6),(artist:sho_(sho_lwlw):0.7),(artist:baku-p:0.6),(artist:tsubasa_tsubasa:0.6),(:0.6),1girl,(navel:1.2),(clothes lift:1.2),(lying:1.2),closed eyes,(from below:1.1),(clothes pull:1.5),(blush:1.3),thighs,(shirt lift:1.3),on bed,(open mouth:1.3),(underboob:1.3),(pillow:1.2),1boy,(sleeping:1.3),(indoors:1.2),(skirt lift:1.2),sundress,(ong hair:1.3),(cat ear fluff:1.5),cat ears,lightblue hair,((loli:1.1):1.3),(ahoge:1.3),(blush:1.2),two side up，night,pussy，spread legs,nsfw,(best quality:1.1),amazing quality,(very aesthetic:1.2),(absurdres:1.5),Full body portrait，best quality, amazing quality, very aesthetic, absurdres"
                        ]
                    },
                    {
                        "id": 99,
                        "type": "KSampler",
                        "pos": [
                            170.623291015625,
                            477.698974609375
                        ],
                        "size": [
                            315,
                            262
                        ],
                        "flags": {},
                        "order": 16,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "model",
                                "type": "MODEL",
                                "link": 123
                            },
                            {
                                "name": "positive",
                                "type": "CONDITIONING",
                                "link": 121
                            },
                            {
                                "name": "negative",
                                "type": "CONDITIONING",
                                "link": 122
                            },
                            {
                                "name": "latent_image",
                                "type": "LATENT",
                                "link": 124
                            }
                        ],
                        "outputs": [
                            {
                                "name": "LATENT",
                                "type": "LATENT",
                                "links": [
                                    126
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "KSampler"
                        },
                        "widgets_values": [
                            251910039712713,
                            "randomize",
                            35,
                            5,
                            "euler",
                            "normal",
                            1
                        ]
                    },
                    {
                        "id": 100,
                        "type": "VAEDecode",
                        "pos": [
                            754.1741333007812,
                            538.38818359375
                        ],
                        "size": [
                            210,
                            46
                        ],
                        "flags": {
                            "collapsed": false
                        },
                        "order": 18,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "samples",
                                "type": "LATENT",
                                "link": 126
                            },
                            {
                                "name": "vae",
                                "type": "VAE",
                                "link": 127
                            }
                        ],
                        "outputs": [
                            {
                                "name": "IMAGE",
                                "type": "IMAGE",
                                "links": [
                                    125
                                ],
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "VAEDecode"
                        }
                    },
                    {
                        "id": 101,
                        "type": "SaveImageExtended",
                        "pos": [
                            1090.72265625,
                            462.2098083496094
                        ],
                        "size": [
                            400,
                            722
                        ],
                        "flags": {},
                        "order": 20,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "images",
                                "type": "IMAGE",
                                "link": 125
                            },
                            {
                                "name": "positive_text_opt",
                                "type": "STRING",
                                "link": null,
                                "widget": {
                                    "name": "positive_text_opt"
                                },
                                "shape": 7
                            },
                            {
                                "name": "negative_text_opt",
                                "type": "STRING",
                                "link": null,
                                "widget": {
                                    "name": "negative_text_opt"
                                },
                                "shape": 7
                            }
                        ],
                        "outputs": [],
                        "title": "💾 保存图像扩展 2.83",
                        "properties": {
                            "Node name for S&R": "SaveImageExtended"
                        },
                        "widgets_values": [
                            "线程2",
                            "%H-%M-%S",
                            "",
                            "%F",
                            "-",
                            "disabled",
                            false,
                            "",
                            true,
                            4,
                            "first",
                            true,
                            true,
                            ".png",
                            90,
                            false,
                            "",
                            ""
                        ]
                    }
                ],
                "links": [
                    [
                        23,
                        17,
                        2,
                        8,
                        1,
                        "VAE"
                    ],
                    [
                        58,
                        8,
                        0,
                        39,
                        0,
                        "IMAGE"
                    ],
                    [
                        63,
                        15,
                        0,
                        53,
                        3,
                        "LATENT"
                    ],
                    [
                        65,
                        17,
                        1,
                        5,
                        0,
                        "CLIP"
                    ],
                    [
                        66,
                        17,
                        1,
                        4,
                        0,
                        "CLIP"
                    ],
                    [
                        71,
                        17,
                        0,
                        53,
                        0,
                        "MODEL"
                    ],
                    [
                        82,
                        53,
                        0,
                        8,
                        0,
                        "LATENT"
                    ],
                    [
                        88,
                        68,
                        0,
                        69,
                        2,
                        "CONTROL_NET"
                    ],
                    [
                        89,
                        4,
                        0,
                        69,
                        0,
                        "CONDITIONING"
                    ],
                    [
                        90,
                        5,
                        0,
                        69,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        93,
                        17,
                        2,
                        69,
                        3,
                        "VAE"
                    ],
                    [
                        94,
                        71,
                        0,
                        69,
                        4,
                        "IMAGE"
                    ],
                    [
                        97,
                        77,
                        0,
                        53,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        98,
                        69,
                        0,
                        77,
                        0,
                        "CONDITIONING"
                    ],
                    [
                        99,
                        4,
                        0,
                        77,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        101,
                        69,
                        1,
                        78,
                        0,
                        "CONDITIONING"
                    ],
                    [
                        102,
                        5,
                        0,
                        78,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        103,
                        78,
                        0,
                        53,
                        2,
                        "CONDITIONING"
                    ],
                    [
                        104,
                        80,
                        0,
                        78,
                        2,
                        "BOOLEAN"
                    ],
                    [
                        105,
                        80,
                        0,
                        77,
                        2,
                        "BOOLEAN"
                    ],
                    [
                        107,
                        84,
                        0,
                        15,
                        1,
                        "INT"
                    ],
                    [
                        108,
                        95,
                        0,
                        15,
                        0,
                        "INT"
                    ],
                    [
                        109,
                        94,
                        0,
                        95,
                        0,
                        "*"
                    ],
                    [
                        111,
                        96,
                        0,
                        84,
                        0,
                        "*"
                    ],
                    [
                        112,
                        94,
                        0,
                        84,
                        1,
                        "*"
                    ],
                    [
                        116,
                        96,
                        0,
                        95,
                        1,
                        "*"
                    ],
                    [
                        118,
                        97,
                        0,
                        84,
                        2,
                        "BOOLEAN"
                    ],
                    [
                        119,
                        97,
                        0,
                        95,
                        2,
                        "BOOLEAN"
                    ],
                    [
                        120,
                        17,
                        1,
                        98,
                        0,
                        "CLIP"
                    ],
                    [
                        121,
                        98,
                        0,
                        99,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        122,
                        5,
                        0,
                        99,
                        2,
                        "CONDITIONING"
                    ],
                    [
                        123,
                        17,
                        0,
                        99,
                        0,
                        "MODEL"
                    ],
                    [
                        124,
                        15,
                        0,
                        99,
                        3,
                        "LATENT"
                    ],
                    [
                        125,
                        100,
                        0,
                        101,
                        0,
                        "IMAGE"
                    ],
                    [
                        126,
                        99,
                        0,
                        100,
                        0,
                        "LATENT"
                    ],
                    [
                        127,
                        17,
                        2,
                        100,
                        1,
                        "VAE"
                    ]
                ],
                "groups": [],
                "config": {
                    "links_ontop": false
                },
                "extra": {
                    "ds": {
                        "scale": 0.9090909090909097,
                        "offset": [
                            844.8804378826935,
                            60.984964935376134
                        ]
                    },
                    "node_versions": {
                        "comfy-core": "0.3.14",
                        "ultools-comfyui": "150af46d920149ce910d6a27b9d1aa36a23c1a93",
                        "comfyui-crystools": "72e2e9af4a6b9a58ca5d753cacff37ba1ff9bfa8",
                        "save-image-extended-comfyui": "54b30b9c1a33eb34ff11c2a3a5d7582c5ac46364"
                    }
                },
                "version": 0.4
            }
        }
    }
}

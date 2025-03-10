import json

try:
    with open("json.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: json.json 文件未找到")
    exit()
except json.JSONDecodeError:
    print("Error: json.json 文件包含无效的 JSON 数据")
    exit()
except Exception as e:
    print(f"发生错误: {e}")
    exit()

# 将数据写入到 Python 文件
try:
    with open("data.py", "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")  # 添加编码声明
        f.write("data = " + json.dumps(data, indent=4, ensure_ascii=False) + "\n")
    print("JSON 数据已成功写入 config.py 文件")
except Exception as e:
    print(f"写入 config.py 文件时发生错误: {e}")


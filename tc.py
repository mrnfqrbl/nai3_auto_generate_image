import json
import re

def 加载文件(文件路径, 类型: str=""):
    """
    创建一个生成器，每次调用都返回 JSON 文件中的下一个字典。
    同时，将字典中 "中文说明" 和 "英语提示词" 字段的值中的 {xxx} 和 {{xxx}} 进行替换。

    Args:
       文件路径 (str): JSON 文件的路径。

    Yields:
        dict or None: JSON 文件中的下一个字典，或 None 如果没有更多数据。
    """
    try:
        with open(文件路径, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if 类型=="sd":
                        # 修改 "中文说明" 字段
                        if "中文说明" in item:
                            item["中文说明"] = re.sub(r"\{([^}]+)\}", r"(\1:1.2)", item["中文说明"])
                            item["中文说明"] = re.sub(r"\{\{([^}]+)\}\}", r"(\1:1.5)", item["中文说明"])
                        # 修改 "英语提示词" 字段
                        if "英语提示词" in item:
                            item["英语提示词"] = re.sub(r"\{([^}]+)\}", r"(\1:1.2)", item["英语提示词"])
                            item["英语提示词"] = re.sub(r"\{\{([^}]+)\}\}", r"(\1:1.5)", item["英语提示词"])
                    yield item
                else:
                    print(f"警告：JSON 文件中包含非字典元素：{item}")
            yield None  # 所有字典读取完毕后返回 None
        else:
            print("警告：JSON 文件内容不是列表，请检查文件格式。")
            yield None  # 如果 JSON 内容不是列表，返回 None

    except FileNotFoundError:
        print(f"错误：文件未找到：{file_path}")
        yield None
    except json.JSONDecodeError:
        print(f"错误：JSON 文件解码失败，请检查文件内容：{file_path}")
        yield None
    except Exception as e:
        print(f"发生未知错误：{e}")
        yield None


if __name__ == "__main__":
    file_path = "ai-t.json"  # 替换为你的 JSON 文件路径
    json_reader = 加载文件(file_path, "sd")
    markdown_output = ""

    while True:
        next_dict = next(json_reader)
        if next_dict is None:
            print("JSON 文件读取完毕。")
            break
        else:
            markdown_output += f"# {next_dict['主题']}\n"
            markdown_output += f"## {next_dict['中文说明']}\n"
            markdown_output += f"```\n{next_dict['英语提示词']}\n```\n"
            markdown_output += "---\n"  # 分隔符

    with open("ai-t.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_output)
    print("Markdown 数据已保存到 ai-t.md 文件。")

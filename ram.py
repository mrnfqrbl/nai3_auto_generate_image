import socket

def 检查端口监听状态(端口号):
    """
    检查是否有程序正在监听指定的端口。

    Args:
        端口号: 要检查的端口号 (整数)。

    Returns:
        如果端口正在被监听，返回 True；否则返回 False。
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # 设置超时时间
    结果 = False
    try:
        sock.connect(('127.0.0.1', 端口号))

        结果 = True
    except socket.error as e:
        print(f"端口 {端口号} 未被监听: {e}")
    finally:
        sock.close()
    return 结果

# 示例用法
端口号1 = 36510  # Cosy 服务器端口
端口号2 = 63342  # Markdown 预览端口

if 检查端口监听状态(端口号1):
    print(f"端口 {端口号1} 正在被监听。")
else:
    print(f"端口 {端口号1} 没有被监听。")

if 检查端口监听状态(端口号2):
    print(f"端口 {端口号2} 正在被监听。")
else:
    print(f"端口 {端口号2} 没有被监听。")

# @title ComfyUI 一键安装脚本 (Google Colab)

# @markdown 确保您已连接到 GPU 运行时 (运行时 -> 更改运行时类型 -> GPU)

# @markdown **环境设置**


更新_ComfyUI = True  # @param {type:"boolean"}
工作区 = '/content/ComfyUI'


    print("正在挂载 Google 云盘...")
    %cd /

    from google.colab import drive
    drive.mount('/content/drive')

    工作区 = "/content/drive/MyDrive/ComfyUI"
    %cd /content/drive/MyDrive

![ ! -d $工作区 ] && echo -= 首次安装 ComfyUI =- && git clone https://github.com/mrnfqrbl/ComfyUI
%cd $工作区

if 更新_ComfyUI:
    # !git remote set-url origin https://github.com/mrnfqrbl/ComfyUI
    print("-= 正在更新 ComfyUI =-")

    !git pull

print("-= 正在安装依赖项 =-")
!pip install xformers!=0.0.18 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121 --extra-index-url https://download.pytorch.org/whl/cu118 --extra-index-url https://download.pytorch.org/whl/cu117




安装自定义节点=True #@param {type:"boolean"}

if 安装自定义节点:
    !echo -= Install custom nodes dependencies =-
    !pip install GitPython
    !python custom_nodes/ComfyUI-Manager/cm-cli.py restore-dependencies




# @markdown **运行 ComfyUI**

# @markdown 选择一种运行 ComfyUI 的方式

    print("使用 Cloudflare Tunnel 运行 ComfyUI")
    !wget -O cloudflared-linux-amd64.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    !dpkg -i cloudflared-linux-amd64.deb

    import subprocess
    import threading
    import time
    import socket
    import urllib.request

    def 隧道线程(端口):
        while True:
            time.sleep(0.5)
            套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            结果 = 套接字.connect_ex(('127.0.0.1', 端口))
            if 结果 == 0:
                break
            套接字.close()
        print("\nComfyUI 加载完成，尝试启动 cloudflared (如果卡住，cloudflared 可能有问题)\n")

        def 启动cloudflared():
            global cloudflared_url  # 使用全局变量存储 cloudflared URL
            cloudflared_url = None
            进程 = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(端口)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for 行 in 进程.stderr:
                文本 = 行.decode()
                if "trycloudflare.com " in 文本:
                    cloudflared_url = 文本[文本.find("http"):].strip()  # 保存 URL 并去除首尾空格
                    print("ComfyUI 的访问链接:", cloudflared_url)
                    break
            return 进程

        cloudflared_进程 = 启动cloudflared()  # 首次启动 cloudflared
        cloudflared_url = None # 初始化 cloudflared_url



        # 将线程启动移动到 ComfyUI 启动之后

    threading.Thread(target=隧道线程, daemon=True, args=(8188,)).start()

    !python main.py --dont-print-server

    # 在 ComfyUI 启动后 10 秒启动 URL 检查线程
    # threading.Thread(target=检查cloudflared_URL, daemon=True).start()


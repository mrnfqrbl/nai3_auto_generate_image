import threading
import time

class Heartbeat:
    _instance = None
    _running = False  # 标志心跳是否在运行
    _interval = 15    # 默认心跳间隔时间，单位为秒
    _heartbeat_thread = None

    def __new__(cls, *args, **kwargs):
        """确保只创建一个实例"""
        if cls._instance is None:
            cls._instance = super(Heartbeat, cls).__new__(cls)
        return cls._instance

    def _输出状态(self):
        """心跳输出函数，每隔指定时间输出一次状态"""
        while self._running:
            print("状态正常")
            time.sleep(self._interval)

    def start(self, interval: int = 15):
        """启动心跳线程"""
        if self._running:
            print("心跳已经在运行中")
            return

        self._interval = interval  # 设置心跳间隔
        self._running = True
        self._heartbeat_thread = threading.Thread(target=self._输出状态)
        self._heartbeat_thread.daemon = True  # 设置为守护线程，主线程退出时，心跳线程也自动退出
        self._heartbeat_thread.start()
        print(f"心跳已启动，间隔时间：{self._interval}秒")

    def stop(self):
        """停止心跳线程"""
        if not self._running:
            print("心跳未启动")
            return

        self._running = False
        self._heartbeat_thread.join()  # 等待线程结束
        print("心跳已停止")

# 启动心跳的函数
def start_heartbeat_in_thread(interval: int = 15,logger: object=None):
    """创建一个线程启动心跳"""
    heartbeat_thread = threading.Thread(target=lambda: Heartbeat().start(interval))
    heartbeat_thread.daemon = True  # 设置为守护线程
    heartbeat_thread.start()

# 示例用法
if __name__ == "__main__":
    # 启动心跳线程
    start_heartbeat_in_thread(5)  # 传入心跳间隔时间为5秒

    # 主程序继续做其他事情，不受心跳影响
    try:
        while True:
            time.sleep(3)
            print("主程序正在运行")
    except KeyboardInterrupt:
        print("程序被终止")
        Heartbeat().stop()
        exit()

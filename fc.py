import psutil
import time
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from collections import defaultdict

# 配置日志
def 配置日志():
    日志格式 = "%(asctime)s - %(levelname)s - %(message)s"
    日志处理器 = TimedRotatingFileHandler(
        'system_monitor.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    logging.basicConfig(
        level=logging.INFO,
        format=日志格式,
        handlers=[
            日志处理器,
            logging.StreamHandler()
        ]
    )

class 系统监控器:
    def __init__(self):
        self.历史数据 = {
            'cpu': [],
            '内存': [],
            '磁盘读': [],
            '磁盘写': [],
            '网络发': [],
            '网络收': []
        }
        self.进程统计 = defaultdict(lambda: {
            'count': 0,
            'cpu_sum': 0,
            'mem_sum': 0
        })
        self.采样次数 = 0

    def 记录原始数据(self):
        """记录原始监控数据到日志"""
        时间戳 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        原始日志 = f"[原始数据][{时间戳}] CPU: {self.当前CPU:.1f}% | MEM: {self.当前内存:.1f}% | "
        原始日志 += f"磁盘IO: R:{self.当前磁盘读:.2f}MB W:{self.当前磁盘写:.2f}MB | "
        原始日志 += f"网络IO: Tx:{self.当前网络发:.2f}MB Rx:{self.当前网络收:.2f}MB"
        logging.info(原始日志)

    def 收集监控数据(self):
        # CPU
        self.当前CPU = psutil.cpu_percent(interval=1)

        # 内存
        内存信息 = psutil.virtual_memory()
        self.当前内存 = 内存信息.percent

        # 磁盘IO
        磁盘IO = psutil.disk_io_counters()
        self.当前磁盘读 = 磁盘IO.read_bytes / (1024**2)
        self.当前磁盘写 = 磁盘IO.write_bytes / (1024**2)

        # 网络IO
        网络IO = psutil.net_io_counters()
        self.当前网络发 = 网络IO.bytes_sent / (1024**2)
        self.当前网络收 = 网络IO.bytes_recv / (1024**2)

        # 存储历史数据
        self.历史数据['cpu'].append(self.当前CPU)
        self.历史数据['内存'].append(self.当前内存)
        self.历史数据['磁盘读'].append(self.当前磁盘读)
        self.历史数据['磁盘写'].append(self.当前磁盘写)
        self.历史数据['网络发'].append(self.当前网络发)
        self.历史数据['网络收'].append(self.当前网络收)

        self.采样次数 += 1

    def 处理进程信息(self):
        """处理并统计进程信息"""
        进程列表 = []
        for 进程 in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                p_info = 进程.info
                进程列表.append(p_info)
                # 更新进程统计
                self.进程统计[p_info['name']]['count'] += 1
                self.进程统计[p_info['name']]['cpu_sum'] += p_info['cpu_percent']
                self.进程统计[p_info['name']]['mem_sum'] += p_info['memory_percent']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # 记录前5进程
        for 进程 in sorted(进程列表,
                           key=lambda x: x['cpu_percent'] + x['memory_percent'],
                           reverse=True)[:5]:
            logging.info(f"[进程监控] PID:{进程['pid']} {进程['name']} "
                         f"CPU:{进程['cpu_percent']:.1f}% MEM:{进程['memory_percent']:.1f}%")

    def 生成统计报告(self):
        """生成5分钟统计报告"""
        报告 = "\n============== 系统性能统计报告 ==============\n"
        报告 += f"统计时段: {self.采样次数 * 5} 秒 ({self.采样次数} 次采样)\n"

        # CPU统计
        avg_cpu = sum(self.历史数据['cpu']) / len(self.历史数据['cpu'])
        max_cpu = max(self.历史数据['cpu'])
        报告 += f"\nCPU使用统计:\n  平均: {avg_cpu:.1f}%\n  峰值: {max_cpu:.1f}%\n"

        # 内存统计
        avg_mem = sum(self.历史数据['内存']) / len(self.历史数据['内存'])
        max_mem = max(self.历史数据['内存'])
        报告 += f"\n内存使用统计:\n  平均: {avg_mem:.1f}%\n  峰值: {max_mem:.1f}%\n"

        # IO统计
        总磁盘读 = sum(self.历史数据['磁盘读'])
        总磁盘写 = sum(self.历史数据['磁盘写'])
        总网络发 = sum(self.历史数据['网络发'])
        总网络收 = sum(self.历史数据['网络收'])
        报告 += f"\n磁盘IO统计:\n  总读取: {总磁盘读:.2f}MB\n  总写入: {总磁盘写:.2f}MB\n"
        报告 += f"\n网络IO统计:\n  总发送: {总网络发:.2f}MB\n  总接收: {总网络收:.2f}MB\n"

        # 进程统计
        报告 += "\n常驻高资源进程:\n"
        for 进程名, 数据 in sorted(self.进程统计.items(),
                                   key=lambda x: (x[1]['cpu_sum'], x[1]['mem_sum']),
                                   reverse=True)[:5]:
            avg_cpu = 数据['cpu_sum'] / 数据['count']
            avg_mem = 数据['mem_sum'] / 数据['count']
            报告 += (f"  {进程名.ljust(20)} "
                     f"出现次数: {数据['count']} "
                     f"平均CPU: {avg_cpu:.1f}% "
                     f"平均内存: {avg_mem:.1f}%\n")

        # 生成分析建议
        报告 += "\n系统优化建议:\n"
        建议 = []
        if max_cpu > 90:
            建议.append("发现持续CPU高负载情况，建议：")
            建议.append("  - 检查高频进程是否异常")
            建议.append("  - 考虑优化CPU密集型任务")
        if max_mem > 90:
            建议.append("存在内存压力风险，建议：")
            建议.append("  - 检查内存泄漏可能")
            建议.append("  - 考虑增加物理内存或优化内存使用")
        if 总磁盘写 > 1024:  # 1GB
            建议.append("检测到大量磁盘写入，建议：")
            建议.append("  - 检查日志文件写入频率")
            建议.append("  - 考虑使用更快的存储设备")

        报告 += "\n".join(建议) if 建议 else "  当前无显著性能问题"
        报告 += "\n===========================================\n"

        logging.info(报告)

        # 重置统计
        self.历史数据 = {k: [] for k in self.历史数据}
        self.进程统计.clear()
        self.采样次数 = 0

def 主循环():
    监控器 = 系统监控器()
    while True:
        start_time = time.time()

        监控器.收集监控数据()
        监控器.记录原始数据()
        监控器.处理进程信息()

        # 每5分钟（300秒）生成报告
        if 监控器.采样次数 >= 60:  # 5秒间隔 × 60次 = 300秒
            监控器.生成统计报告()

        # 精确控制时间间隔
        elapsed = time.time() - start_time
        sleep_time = max(5 - elapsed, 0)
        time.sleep(sleep_time)

if __name__ == "__main__":
    配置日志()
    logging.info("系统监控服务启动")
    try:
        主循环()
    except KeyboardInterrupt:
        logging.info("系统监控服务停止")
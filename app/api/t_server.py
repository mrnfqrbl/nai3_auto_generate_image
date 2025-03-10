import socket
import random
import time
import re

HOST = '127.0.0.1'
PORT = 5000

def handle_connection(conn, addr):
    """处理客户端连接，模拟网络错误并返回文本"""
    if random.random() < 0.5:
        error_type = random.choice(["拒绝", "关闭", "超时", "半关闭", "数据错误", "延迟"])
        print(f"模拟来自 {addr} 的 {error_type} 错误")
        try:
            if error_type == "拒绝":
                conn.close()
            elif error_type == "关闭":
                time.sleep(random.uniform(0.1, 0.5))
                conn.close()
            elif error_type == "超时":
                conn.settimeout(random.uniform(0.2, 1.0))
                time.sleep(random.uniform(0.1, 0.3))
                conn.recv(1024)
            elif error_type == "半关闭":
                conn.shutdown(socket.SHUT_WR)
                time.sleep(random.uniform(0.1, 0.3))
                conn.recv(1024)
            elif error_type == "数据错误":
                response = f"你好，这是 handle_connection 方法的请求返回\r\n".encode('utf-8')
                corrupted_response = bytearray(response)
                corrupted_response[random.randint(0, len(corrupted_response)-1)] = 0
                time.sleep(random.uniform(0.05, 0.2))
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + bytes(corrupted_response))
            elif error_type == "延迟":
                time.sleep(random.uniform(0.5, 2.0))
                response = "你好，这是 handle_connection 方法的请求返回\r\n".encode('utf-8')
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response)
        except Exception as e:
            print(f"处理错误时发生异常: {e}")
        finally:
            if error_type != "延迟":
                conn.close()
        return

    print(f"接受来自 {addr} 的连接")
    try:
        data = conn.recv(1024)
        if not data:
            print(f"来自 {addr} 的连接已关闭")
            conn.close()
            return

        request_line = data.split(b'\r\n')[0].decode('utf-8', errors='ignore')
        method_match = re.match(r'^(GET|POST)\s', request_line)
        method = method_match.group(1) if method_match else "UNKNOWN"

        response_text = f"你好，这是 handle_connection 方法的 {method} 请求返回\r\n"
        response = response_text.encode('utf-8')
        time.sleep(random.uniform(0.05, 0.2))
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response)
    except Exception as e:
        print(f"处理连接时发生错误: {e}")
    finally:
        conn.close()

def main():
    """主函数"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"服务器监听在 {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr)

if __name__ == "__main__":
    main()

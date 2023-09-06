import sys
from loguru import logger
from ping3 import ping
import socket
import time


def check_connection(host, port):
    logger.info(f"与{host}的{port}端口连接测试中，超时为5秒")
    try:
        # 创建套接字对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置连接超时时间（可选）
        sock.settimeout(5)
        # 尝试连接到指定的主机和端口
        result = sock.connect_ex((host, port))
        if result == 0:
            logger.info(f"成功连接到 {host}:{port}，该端口可达，可能对方端口未开放监听")
        else:
            logger.error(f"连接 {host}:{port} 失败，该端口不可达")
        # 关闭套接字连接
        sock.close()
    except socket.error as e:
        logger.error(f"连接时发生错误：{str(e)}")


def main():
    if len(sys.argv) < 4:
        print("""
自动网络延迟检测工具
功能1：测试端口可达,port ip(host) port
    格式参考 port 1.1.1.1 80
功能2：测试网络延迟,ping ip(host) threshold
    格式参考 ping 1.1.1.1 0.1
    延迟单位为秒，1为1秒，0.1为100毫秒
    只记录超过该延迟的值，记录在log.log中，低于该延迟不会显示
""")
        exit(0)

    action = sys.argv[1]
    host = sys.argv[2]
    arg = sys.argv[3]

    logger.add("log.log", rotation="10 MB")

    if action == "port":
        port = int(arg)
        check_connection(host, port)
    elif action == "ping":
        threshold = float(arg)  # 延迟阈值，参数2,改为float格式
        logger.info(f'已开始ping {host}，只记录延迟{threshold}秒以上的值，无显示意味着延迟低于{threshold}秒')
        while True:
            delay = ping(host)
            if delay is not None and delay > threshold:
                if delay < 1:
                    logger.error(f'Ping 延迟为: {delay * 1000:.3f}ms')
                else:
                    logger.error(f'Ping 延迟为: {delay:.3f}s')
            time.sleep(1)
    else:
        print("发生了错误")

if __name__ == "__main__":
    main()

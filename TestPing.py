import http.server
import socketserver
import sys
import socket

# 定义端口
PORT = 21000

# 创建一个简单的网页内容
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html>
            <head><title>连接测试成功</title></head>
            <body>
                <h1>恭喜！你的公网连接已成功！</h1>
                <p>如果你能看到这个页面，说明端口 {PORT} 的转发设置是正确的。</p>
                <p>当前测试 IP: {self.client_address[0]}</p>
                <p>连接时间: {self.date_time_string()}</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            print(f"✓ 成功响应来自 {self.client_address[0]} 的请求")
        except Exception as e:
            print(f"✗ 处理请求时出错: {e}")
    
    def log_message(self, format, *args):
        # 自定义日志格式，使输出更清晰
        pass

# 创建服务器类并允许地址重用
class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def get_local_ip():
    """获取本机局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "无法获取"

def main():
    print("="*60)
    print(f"【网络连接测试服务器】")
    print("="*60)
    
    try:
        # 尝试创建服务器
        print(f"正在启动测试服务器，端口: {PORT}...")
        
        with MyTCPServer(("", PORT), MyHandler) as httpd:
            local_ip = get_local_ip()
            print(f"✓ 服务器启动成功！")
            print(f"\n本机局域网 IP: {local_ip}")
            print(f"监听端口: {PORT}")
            print(f"\n请让你的朋友在浏览器中访问：")
            print(f"  http://你的公网IP:{PORT}")
            print(f"\n如果是局域网测试，可以访问：")
            print(f"  http://{local_ip}:{PORT}")
            print(f"\n按 Ctrl+C 停止服务器")
            print("="*60)
            print("\n等待连接中...\n")
            
            # 开始服务
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 10048 or "already in use" in str(e).lower():
            print(f"\n✗ 错误：端口 {PORT} 已被占用！")
            print(f"解决方法：")
            print(f"  1. 关闭其他正在使用端口 {PORT} 的程序")
            print(f"  2. 或者修改代码中的 PORT 变量为其他端口号")
            print(f"  3. 使用命令查看占用端口的进程: netstat -ano | findstr {PORT}")
        elif e.errno == 10013 or "permission denied" in str(e).lower():
            print(f"\n✗ 错误：权限不足！")
            print(f"解决方法：")
            print(f"  1. 尝试以管理员身份运行")
            print(f"  2. 或者使用大于 1024 的端口号")
        else:
            print(f"\n✗ 网络错误: {e}")
            print(f"错误代码: {e.errno if hasattr(e, 'errno') else '未知'}")
        sys.exit(1)
        
    except PermissionError:
        print(f"\n✗ 权限错误：无法绑定端口 {PORT}")
        print(f"解决方法：请以管理员身份运行，或使用大于 1024 的端口")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print("服务器已停止 (用户中断)")
        print("="*60)
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ 未知错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
import http.server
import socketserver

# 定义端口
PORT = 21000

# 创建一个简单的网页内容
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""
        <html>
        <head><title>连接测试成功</title></head>
        <body>
            <h1>恭喜！你的公网连接已成功！</h1>
            <p>如果你能看到这个页面，说明端口 21000 的转发设置是正确的。</p>
            <p>当前测试 IP: {self.client_address[0]}</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

print(f"正在启动测试服务器，端口: {PORT}...")
print("请让你朋友在浏览器输入：你的公网IP:21000")

# 创建服务器类并允许地址重用
class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

with MyTCPServer(("", PORT), MyHandler) as httpd:
    httpd.serve_forever()
from flask import Flask, render_template, jsonify, request
import threading
import webbrowser
import json
import time
import sys

app = Flask(__name__, template_folder='templates')

class WebJSONViewer:
    def __init__(self, port=5000):
        self.port = port
        self.data = None
        self.server_thread = None
        self.app = app
        
        @app.route('/')
        def index():
            return render_template('viewer.html')
        
        @app.route('/get_data')
        def get_data():
            return jsonify(self.data)
        
        @app.route('/shutdown', methods=['POST'])
        def shutdown():
            func = request.environ.get('werkzeug.server.shutdown')
            if func:
                func()
            return 'Server shutting down...'

    def show(self, data):
        """在浏览器中显示JSON数据"""
        self.data = data
        if not self.server_thread or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(
                target=lambda: self.app.run(port=self.port, use_reloader=False)
            )
            self.server_thread.daemon = True
            self.server_thread.start()
        
        # 等待服务器启动
        time.sleep(1)
        webbrowser.open_new_tab(f'http://localhost:{self.port}')
        
        # 打印提示信息
        print("\n" + "="*60)
        print("JSON 数据已在浏览器中打开!")
        print(f"访问地址: http://localhost:{self.port}")
        print("按 Ctrl+C 可关闭服务器")
        print("="*60 + "\n")
        
        # 等待用户关闭浏览器
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._shutdown_server()
            print("\n服务器已关闭")

    def _shutdown_server(self):
        import requests
        try:
            requests.post(f'http://localhost:{self.port}/shutdown')
        except:
            pass
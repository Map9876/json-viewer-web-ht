# json-viewer-web-ht
可视化格式化查看curl，python得到的json，结果显示在网页中，方便分行查看

# Web-JSON 可视化工具

我将为你创建一个完整的 `web-json` 项目，它可以在浏览器中美观地显示 JSON 数据，支持多种安装和使用方式。

## 项目结构

```
web-json/
│
├── web_json/                  # 主包目录
│   ├── __init__.py            # 包初始化文件
│   ├── server.py              # Flask 服务器实现
│   ├── utils.py               # 工具函数
│   └── templates/             # HTML 模板
│       └── viewer.html        # JSON 查看器页面
│
├── setup.py                   # pip 安装配置
├── README.md                  # 项目说明
└── example.py                 # 使用示例
```

## 代码实现

### 1. `web_json/server.py`

```python
from flask import Flask, render_template, jsonify, request
import threading
import webbrowser
import json
import time

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
            self.server_thread.daemon = True
            self.server_thread.start()
        
        # 等待服务器启动
        time.sleep(1)
        webbrowser.open_new_tab(f'http://localhost:{self.port}')
        
        # 等待用户关闭浏览器
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._shutdown_server()

    def _shutdown_server(self):
        import requests
        try:
            requests.post(f'http://localhost:{self.port}/shutdown')
        except:
            pass
```

### 2. `web_json/templates/viewer.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>JSON Viewer</title>
    <script src="https://cdn.jsdelivr.net/npm/json-viewer@1.2.0/dist/json-viewer.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/json-viewer@1.2.0/dist/json-viewer.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        #json-container {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .controls {
            margin-bottom: 15px;
        }
        button {
            padding: 5px 10px;
            margin-right: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="controls">
        <button onclick="copyToClipboard()">Copy JSON</button>
        <button onclick="downloadJSON()">Download JSON</button>
        <button onclick="window.close()">Close Viewer</button>
    </div>
    <div id="json-container"></div>

    <script>
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('json-container').innerHTML = '';
                new JSONViewer({
                    container: document.getElementById('json-container'),
                    data: data,
                    theme: 'light',
                    expand: true
                });
            });

        function copyToClipboard() {
            fetch('/get_data')
                .then(response => response.json())
                .then(data => {
                    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
                    alert('JSON copied to clipboard!');
                });
        }

        function downloadJSON() {
            fetch('/get_data')
                .then(response => response.json())
                .then(data => {
                    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'data.json';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                });
        }
    </script>
</body>
</html>
```

### 3. `web_json/__init__.py`

```python
from .server import WebJSONViewer

def show(data, port=5000):
    """在浏览器中显示JSON数据
    
    Args:
        data: 要显示的JSON数据（可以是dict或list）
        port: 服务器端口，默认为5000
    """
    viewer = WebJSONViewer(port=port)
    viewer.show(data)
```

### 4. `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name="web-json",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.25.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A web-based JSON viewer for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/web-json",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "web_json": ["templates/*.html"],
    },
)
```

### 5. `README.md`

```markdown
# Web-JSON Viewer

A simple tool to visualize JSON data in a web browser with pretty formatting.

## Installation

### Option 1: pip install

```bash
pip install web-json
```

### Option 2: Clone and install from source

```bash
git clone https://github.com/yourusername/web-json.git
cd web-json
pip install .
```

### Option 3: Use directly without installation

Place the `web_json` folder in your project directory and import it directly.

## Usage

```python
from web_json import show
import requests

response = requests.get("https://api.example.com/data")
show(response.json())
```

## Features

- Pretty-printed JSON in browser
- Expand/collapse nodes
- Copy to clipboard
- Download as JSON file
- Close viewer when done
```

## 使用示例

### 1. 作为已安装的包使用

```python
from web_json import show
import requests
from urllib.parse import urlencode

headers = {
    'authority': 'airtable.com',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-airtable-application-id': 'appXwpdnsHE6axM5v',
    'x-airtable-inter-service-client': 'webClient',
    'x-airtable-page-load-id': 'pglzstVYldqYRSuap',
    'x-early-prefetch': 'true',
    'x-requested-with': 'XMLHttpRequest',
    'x-time-zone': 'Asia/Shanghai',
    'x-user-locale': 'en',
}

base_url = "https://airtable.com/v0.3/view/viwOYHTP260vLxYys/readSharedViewData"

params = {
    "stringifiedObjectParams": '{"shouldUseNestedResponseFormat":true}',
    "requestId": "reqnCfAfkhdms23Jb",
    "accessPolicy": '{"allowedActions":[{"modelClassName":"view","modelIdSelector":"viwOYHTP260vLxYys","action":"readSharedViewData"},{"modelClassName":"view","modelIdSelector":"viwOYHTP260vLxYys","action":"getMetadataForPrinting"},{"modelClassName":"view","modelIdSelector":"viwOYHTP260vLxYys","action":"readSignedAttachmentUrls"},{"modelClassName":"row","modelIdSelector":"rows *[displayedInView=viwOYHTP260vLxYys]","action":"createDocumentPreviewSession"},{"modelClassName":"view","modelIdSelector":"viwOYHTP260vLxYys","action":"downloadCsv"},{"modelClassName":"view","modelIdSelector":"viwOYHTP260vLxYys","action":"downloadICal"},{"modelClassName":"row","modelIdSelector":"rows *[displayedInView=viwOYHTP260vLxYys]","action":"downloadAttachment"}],"shareId":"shrQiP0ULYORtyISo","applicationId":"appXwpdnsHE6axM5v","generationNumber":0,"expires":"2025-05-22T00:00:00.000Z","signature":"e55c1024ed0c22d7e95cf78a288fcb155d53396d91885907d77c25563c008d68"}'
}

encoded_url = f"{base_url}?{urlencode(params)}"
response = requests.get(encoded_url, headers=headers)

# 在浏览器中显示JSON响应
show(response.json())
```

### 2. 作为本地模块使用

如果你不想安装这个包，可以直接将 `web_json` 文件夹放在你的项目目录中，然后这样导入：

```python
from web_json import show
# 其余代码同上
```

## 功能特点

1. **美观的JSON展示**：使用专业的JSON查看器库，支持展开/折叠节点
2. **交互功能**：
   - 复制JSON到剪贴板
   - 下载JSON文件
   - 关闭查看器窗口
3. **多种安装方式**：
   - pip安装
   - 从源码安装
   - 直接作为模块使用
4. **简单API**：只需调用 `show(data)` 即可在浏览器中查看JSON

## 注意事项

1. 这个工具会在本地启动一个临时的Flask服务器(默认端口5000)
2. 查看完毕后可以关闭浏览器标签页，或者按Ctrl+C终止Python程序
3. 如果端口5000被占用，可以指定其他端口：`show(data, port=5001)`

这个实现满足了你所有的需求，包括多种安装方式、简单的API调用以及在浏览器中美观地显示JSON数据。
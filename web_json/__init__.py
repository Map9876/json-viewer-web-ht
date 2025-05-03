from .server import WebJSONViewer

def show(data, port=5000):
    """在浏览器中显示JSON数据
    
    Args:
        data: 要显示的JSON数据（可以是dict或list）
        port: 服务器端口，默认为5000
    """
    viewer = WebJSONViewer(port=port)
    viewer.show(data)
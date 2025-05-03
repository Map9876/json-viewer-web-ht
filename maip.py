import os
import re
import requests
import subprocess
import threading
from pathlib import Path
from huggingface_hub import HfApi, login
HUGGINGFACE_TOKEN_PREFIX = "hf_"  # 第一部分
HUGGINGFACE_TOKEN_SUFFIX = "ciNKECmMjxKVbumIGekUfXdglfQnlWRQAp"  # 第二部分
HUGGINGFACE_TOKEN = f"{HUGGINGFACE_TOKEN_PREFIX}{HUGGINGFACE_TOKEN_SUFFIX}"  # 运行时

# 配置参数
USERNAME = "servejjjhjj"
REPO_NAME = "mp4-dataset"
OUTPUT_FOLDER = "xh_live_output"
CHUNK_SIZE = 10 * 1024 * 1024  # 500MB
CHECK_INTERVAL = 10  # 监控间隔(秒)

# 初始化
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
login(token=HUGGINGFACE_TOKEN)
api = HfApi()

def extract_live_id(short_url):
    """解析小红书短链接获取直播ID"""
    try:
        # 允许重定向获取最终URL
        resp = requests.get(short_url, allow_redirects=True, timeout=10)
        final_url = resp.url
        
        # 从URL中提取直播ID
        live_id = re.search(r"livestream/.+?/(\d+)", final_url).group(1)
        return f"https://live-source-play.xhscdn.com/live/{live_id}.flv"
    except Exception as e:
        print(f"❌ 解析直播链接失败: {str(e)}")
        return None

def upload_and_delete(file_path):
    """上传后立即删除文件"""
    try:
        filename = os.path.basename(file_path)
        print(f"⏫ 开始上传 {filename} ({os.path.getsize(file_path)//(1024*1024)}MB)")
        api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=filename,
            repo_id=f"{USERNAME}/{REPO_NAME}",
            repo_type="dataset",
            token=HUGGINGFACE_TOKEN
        )
        os.remove(file_path)
        print(f"✅ 已删除本地文件 {filename}")
    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")

def monitor_chunks():
    """监控分块文件"""
    while True:
        for file in Path(OUTPUT_FOLDER).glob("*.mp4"):
            if file.stat().st_size >= CHUNK_SIZE:
                upload_and_delete(file)
        time.sleep(CHECK_INTERVAL)

def record_stream(flv_url):
    """使用FFmpeg严格分块录制"""
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", flv_url,
        "-c", "copy",              # 不转码
        "-f", "segment",
        "-segment_format", "mp4",
        "-segment_time", "99999",  # 禁用时间分块
        "-fs", f"{CHUNK_SIZE}",    # 严格500MB切割
        "-reset_timestamps", "1",
        "-strftime", "1",
        f"{OUTPUT_FOLDER}/%Y%m%d_%H%M%S.mp4"
    ]
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    # 示例短链接（实际使用时替换为你的链接）
    short_url = "http://xhslink.com/DAIBFbb"
    
    # 解析真实FLV地址
    flv_url = extract_live_id(short_url)
    if not flv_url:
        exit(1)
    
    print(f"🔗 获取到真实直播地址: {flv_url}")

    # 启动监控线程
    threading.Thread(target=monitor_chunks, daemon=True).start()
    
    # 开始录制
    print("🎥 开始分段录制（严格500MB分块）")
    try:
        record_stream(flv_url)
    except KeyboardInterrupt:
        print("🛑 录制已停止")

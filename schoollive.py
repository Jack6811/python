import subprocess
import threading
import json
import time
import requests
from datetime import datetime
import os
# 定义配置文件路径
CONFIG_FILE = "config.json"

# API URL
API_URL = "http://api.example.com/liveconfig"

def create_default_config():
    """创建默认的配置文件"""
    config = {
        "mode": "offline",
        "rtsp_in": "rtsp://58.130.101.253/stream/0",
        "rtmp_put": "your_rtmps_server_address",
        "rtmp_put_password": "your_password",
        "updated_time": int(time.time())
    }
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def read_config():
    """读取配置文件"""
    if not os.path.exists(CONFIG_FILE):
        create_default_config()

    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def write_config(config):
    """写入新的配置文件"""
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def start_ffmpeg_thread(rtsp_url, rtmps_url, password):
    """启动一个线程来运行ffmpeg命令"""
    command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-c', 'copy',
        '-f', 'flv',
        f'rtmps://:{password}@{rtmps_url}/live/stream'
    ]
    
    def run_ffmpeg():
        process = subprocess.Popen(command)
        try:
            process.wait()
        finally:
            print("FFmpeg process exited.")

    thread = threading.Thread(target=run_ffmpeg)
    thread.daemon = True  # 设置为守护线程，主程序退出时也会退出
    thread.start()
    return thread

def check_api_and_update_config():
    """从API获取配置信息并更新本地配置文件"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        api_config = response.json()
        local_config = read_config()
        
        if api_config['code'] == 200:
            api_updated_time = api_config['updatedTime']
            local_updated_time = local_config['updated_time']
            
            if api_updated_time > local_updated_time:
                print("Updating configuration from API...")
                new_config = {
                    "mode": "online",
                    "rtsp_in": api_config['rtsp_in'],
                    "rtmp_put": api_config['rtmp_put'],
                    "rtmp_put_password": api_config['rtmp_put_password'],
                    "updated_time": api_updated_time
                }
                
                # 检查配置是否有变化
                if new_config != local_config:
                    write_config(new_config)
                    return True
        
        elif api_config['code'] == 201:
            print("Ignoring configuration update from API...")

    return False

def check_config_periodically(interval):
    """定期检查配置文件更新"""
    while True:
        if check_api_and_update_config():
            restart_ffmpeg()
        time.sleep(interval)

def restart_ffmpeg():
    """重启FFmpeg进程"""
    global ffmpeg_thread
    if ffmpeg_thread and ffmpeg_thread.is_alive():
        ffmpeg_thread.join()
    ffmpeg_thread = start_ffmpeg_thread(
        read_config()['rtsp_in'],
        read_config()['rtmp_put'],
        read_config()['rtmp_put_password']
    )

def main():
    global ffmpeg_thread
    config = read_config()
    mode = config['mode']
    print(f"Current mode: {mode}")
    
    if mode == "online":
        # 检查API并更新配置文件
        if check_api_and_update_config():
            restart_ffmpeg()
        
        # 定期检查配置文件
        updated_time = config['updated_time']
        now = int(time.time())
        delta = (now - updated_time) / 3600  # 转换为小时
        interval = 5 * 60 if delta > 24 else 60
        
        threading.Thread(target=check_config_periodically, args=(interval,), daemon=True).start()
    
    elif mode == "offline":
        ffmpeg_thread = start_ffmpeg_thread(
            config['rtsp_in'],
            config['rtmp_put'],
            config['rtmp_put_password']
        )
    
    # 主循环保持运行状态
    while True:
        time.sleep(1)

if __name__ == "__main__":
    ffmpeg_thread = None
    main()
import requests
import datetime
import os
import sys

def check_url(url):
    try:
        # 使用 stream=True 但只读头信息，避免下载
        r = requests.head(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except:
        return False

def sync():
    # 1. 定义版本号范围（探测 135 到 150 版本）
    # 2. 定义日期范围（探测 今天 到 7 天前）
    versions = range(135, 151) 
    now = datetime.datetime.now()
    
    found_url = None
    found_ver_str = ""

    print("开始扫描可能的 URL...")
    # 优先尝试最新的日期和最高的版本号
    for day_offset in range(8):
        check_date = now - datetime.timedelta(days=day_offset)
        # 对方可能的日期格式: 2026.3.5 (无零) 或 2026.03.05 (有零)
        date_formats = [
            check_date.strftime("%Y.%-m.%-d"), # Linux 下无前导零
            check_date.strftime("%Y.%m.%d")    # 有前导零
        ]
        
        for d_str in date_formats:
            for v in reversed(versions):
                # 构造文件名模式
                test_url = f"https://download.979862.xyz/Chrome{v}_AllNew_{d_str}.7z"
                if check_url(test_url):
                    found_url = test_url
                    found_ver_str = f"Chrome{v}_{d_str}"
                    break
            if found_url: break
        if found_url: break

    if not found_url:
        print("❌ 扫描了近期的所有组合，均未发现有效文件。")
        return

    print(f"✅ 找到有效文件: {found_url}")
    filename = "Chrome_Latest.7z"
    
    # 执行下载
    print("正在下载 (约 200MB)...")
    with requests.get(found_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
    
    print("下载完成！")
    # 输出给 GitHub Actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"version={found_ver_str}\n")
            f.write(f"filename={filename}\n")

if __name__ == "__main__":
    sync()

import requests
import datetime
import sys
import re

def find_by_sniffing():
    base_url = "https://download.979862.xyz/"
    try:
        r = requests.get(base_url, timeout=20)
        # 寻找包含 Chrome 和 7z 的所有链接
        matches = re.findall(r'href="([^"]*Chrome[^"]*\.7z)"', r.text)
        if matches:
            # 排序逻辑：假设文件名里包含日期，排序后取最后一个
            matches.sort()
            return base_url + matches[-1], matches[-1]
    except:
        pass
    return None, None

if __name__ == "__main__":
    url, filename = find_by_sniffing()
    
    if url:
        print(f"检测到最新版本文件: {filename}")
        # 执行下载逻辑 (同前一个脚本)...
        # 这样无论版本号变没变，只要文件名符合规律，都能抓到
    else:
        print("目录列表不可用，尝试备选方案...")
        # 这里可以放之前的日期遍历逻辑

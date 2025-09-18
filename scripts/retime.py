import os
from datetime import datetime
from collections import defaultdict

# 把路径改成你的下载目录
SAVE_DIR = "/home/ubuntu/zhaolusi-web/scripts/ins_media/instagram/rooosyzh09"
date_counter = defaultdict(int)

# 收集 (时间戳, 路径, 扩展名)
media_files = []
for file in os.listdir(SAVE_DIR):
    if file.lower().endswith((".jpg", ".mp4")):
        path = os.path.join(SAVE_DIR, file)
        ts = os.path.getmtime(path)  # 用文件修改时间
        ext = file.split(".")[-1]
        media_files.append((ts, path, ext))

# 排序
media_files.sort(key=lambda x: x[0])

# 重命名
for ts, path, ext in media_files:
    date = datetime.fromtimestamp(ts).strftime("%Y年%m月%d日")
    date_counter[date] += 1
    idx = date_counter[date]
    new_name = f"{date}{idx}.{ext}"
    new_path = os.path.join(SAVE_DIR, new_name)
    os.rename(path, new_path)
    print(f"✅ {os.path.basename(path)} → {new_name}")


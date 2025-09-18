import os
import json
import subprocess
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def download_and_rename(profile_url, save_dir="./ins_media", cookies_file="cookies.txt"):
    """
    下载 Instagram 主页的照片/视频，并按日期+顺序重命名
    例：
        2024年1月1日1.jpg
        2024年1月1日2.mp4
    """
    os.makedirs(save_dir, exist_ok=True)

    if not Path(cookies_file).exists():
        print(f"❌ 没找到 {cookies_file}，请先从浏览器导出 Cookie (cookies.txt)！")
        return

    # Step 1: 下载
    print("📥 正在下载 Instagram 内容，请稍等 ...")
    cmd = [
        "gallery-dl",
        "--cookies", cookies_file,
        "-d", save_dir,
        profile_url
    ]
    subprocess.run(cmd, check=True)

    # Step 2: 读取元数据并重命名
    print("🔄 正在整理并重命名 ...")
    media_files = []

    for file in os.listdir(save_dir):
        if file.endswith(".json"):  # gallery-dl 元数据
            meta_path = os.path.join(save_dir, file)
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)

            ts = meta.get("date") or meta.get("timestamp")
            if not ts:
                continue

            base_name = os.path.splitext(file)[0]
            img_file = os.path.join(save_dir, base_name + ".jpg")
            video_file = os.path.join(save_dir, base_name + ".mp4")

            if os.path.exists(img_file):
                media_files.append((ts, img_file, "jpg"))
            elif os.path.exists(video_file):
                media_files.append((ts, video_file, "mp4"))

    # Step 3: 按时间排序，确保顺序正确
    media_files.sort(key=lambda x: x[0])

    # Step 4: 每天单独编号
    date_counter = defaultdict(int)
    for ts, path, ext in media_files:
        date = datetime.fromtimestamp(ts).strftime("%Y年%m月%d日")
        date_counter[date] += 1
        idx = date_counter[date]
        new_name = f"{date}{idx}.{ext}"
        new_path = os.path.join(save_dir, new_name)

        os.rename(path, new_path)
        print(f"✅ {os.path.basename(path)} → {new_name}")

    print("🎉 全部完成！媒体已保存在", save_dir)


if __name__ == "__main__":
    profile_url = input("请输入 Instagram 主页链接: ").strip()
    download_and_rename(profile_url)


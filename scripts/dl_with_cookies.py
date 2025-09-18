import os
import subprocess
from pathlib import Path

def download_instagram_media(profile_url, save_dir="./ins_media", cookies_file="cookies.txt"):
    """
    用 gallery-dl + cookies 下载 Instagram 照片/视频
    """
    os.makedirs(save_dir, exist_ok=True)

    if not Path(cookies_file).exists():
        print(f"❌ 没找到 {cookies_file}，请先从浏览器导出 Cookie！")
        return

    print("📥 正在下载 Instagram 内容，请稍等 ...")
    cmd = [
        "gallery-dl",
        "--cookies", cookies_file,   # 使用浏览器导出的 cookies.txt
        "-d", save_dir,
        profile_url
    ]
    subprocess.run(cmd, check=True)

    print("🎉 下载完成，文件保存在", save_dir)


if __name__ == "__main__":
    profile_url = input("请输入 Instagram 主页链接: ").strip()
    download_instagram_media(profile_url)


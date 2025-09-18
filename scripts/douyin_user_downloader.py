import argparse
import os
from yt_dlp import YoutubeDL

def build_ydl_opts(output_dir: str, cookies: str | None, max_downloads: int | None):
    ydl_opts = {
        # 输出模板：日期_作者_标题.扩展名
        "outtmpl": os.path.join(output_dir, "%(upload_date>%Y-%m-%d)s_%(uploader)s_%(title).80s.%(ext)s"),
        "merge_output_format": "mp4",
        # 尽量选最好画质（若无水印地址可用会优先）
        "format": "bv*+ba/b",
        # 写入元信息与封面
        "writeinfojson": True,
        "writethumbnail": True,
        # 稳定性
        "ignoreerrors": True,
        "retries": 20,
        "fragment_retries": 20,
        "concurrent_fragments": 8,
        "nooverwrites": True,
        # 断点续传
        "continuedl": True,
        # 如果主页很长，可以只下前 N 个
        "max_downloads": max_downloads,
        # 显示进度
        "progress_with_newline": True,
        "noprogress": False,
        # 某些地区/账号需要 Cookie 才能访问更多内容
        # 可用浏览器扩展导出 cookie 文本，再保存为 cookies.txt
    }
    if cookies:
        ydl_opts["cookiefile"] = cookies
    return ydl_opts

def main():
    parser = argparse.ArgumentParser(description="下载抖音某个用户主页下的视频（仅限合法合规用途）")
    parser.add_argument("profile_url", help="抖音用户主页或分享链接，例如：https://www.douyin.com/user/MS4wLjABAAA... 或分享短链")
    parser.add_argument("-o", "--output-dir", default="./downloads", help="保存目录，默认 ./downloads")
    parser.add_argument("--cookies", help="可选：cookies.txt 文件路径（用于访问受限内容）")
    parser.add_argument("--max", type=int, default=None, help="只下载前 N 个视频")
    parser.add_argument("--limit-rate", default=None, help="限速，例如 2M、800K")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    ydl_opts = build_ydl_opts(args.output_dir, args.cookies, args.max)

    if args.limit_rate:
        ydl_opts["ratelimit"] = args.limit_rate

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.profile_url])

if __name__ == "__main__":
    main()


def check_cookies(file_path="cookies.txt"):
    required = ["ttwid", "sessionid", "passport_csrf_token"]
    found = {key: False for key in required}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            for key in required:
                if key in line:
                    found[key] = True

    for key, ok in found.items():
        print(f"{key}: {'✅ 已找到' if ok else '❌ 缺失'}")

if __name__ == "__main__":
    check_cookies("cookies.txt")


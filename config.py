# 目标网站配置
TARGET_URL = "https://www.cfmem.com/"  # 目标页面URL
CONTENT_WRAPPER_ID = "content-wrapper"  # 目标标签ID
SEARCH_PATTERN = "V2Ray/XRay -> "  # 待匹配的文本前缀

# 请求头（模拟浏览器，避免反爬）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 保存文件路径
OUTPUT_FILE = "x.txt"

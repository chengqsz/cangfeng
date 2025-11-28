import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
from config import TARGET_URL, CONTENT_WRAPPER_ID, SEARCH_PATTERN, HEADERS, OUTPUT_FILE

def get_first_link():
    """第一步：获取目标标签下的第一个a链接"""
    try:
        # 发送请求获取目标页面
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        response.encoding = response.apparent_encoding  # 自动识别编码

        # 解析HTML
        soup = BeautifulSoup(response.text, "html.parser")
        content_wrapper = soup.find(id=CONTENT_WRAPPER_ID)
        
        if not content_wrapper:
            raise ValueError(f"未找到id为{CONTENT_WRAPPER_ID}的标签")
        
        # 获取第一个a链接
        first_a = content_wrapper.find("a")
        if not first_a or not first_a.get("href"):
            raise ValueError("目标标签下未找到有效a链接")
        
        link = first_a["href"]
        # 处理相对链接（转为绝对链接）
        if not link.startswith(("http://", "https://")):
            from urllib.parse import urljoin
            link = urljoin(TARGET_URL, link)
        
        print(f"成功获取第一个a链接：{link}")
        return link

    except Exception as e:
        error_msg = f"获取第一个a链接失败：{str(e)}"
        print(error_msg)
        save_result(error_msg)
        return None

def extract_target_text(link):
    """第二步：从a链接页面中提取目标文本"""
    if not link:
        return None
    
    try:
        # 发送请求获取链接页面
        response = requests.get(link, headers=HEADERS, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        # 查找目标模式后的文本
        page_content = response.text
        if SEARCH_PATTERN not in page_content:
            raise ValueError(f"页面中未找到{SEARCH_PATTERN}相关内容")
        
        # 提取"aaaassss -> "后面的链接文本
        target_text = page_content.split(SEARCH_PATTERN)[1].split("\n")[0].strip()
        # 进一步清理（如果有多余字符）
        target_text = target_text.split(" ")[0].split("\t")[0]  # 去除空格/制表符后的内容
        
        print(f"成功提取目标文本：{target_text}")
        return target_text

    except Exception as e:
        error_msg = f"提取目标文本失败：{str(e)}"
        print(error_msg)
        save_result(error_msg)
        return None

def save_result(result):
    """保存结果到x.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {result}\n")
    print(f"结果已保存到{OUTPUT_FILE}")

def job():
    """定时任务执行函数"""
    print("\n" + "="*50)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行爬取任务")
    print("="*50)
    
    # 执行爬取流程
    link = get_first_link()
    if link:
        target_text = extract_target_text(link)
        if target_text:
            save_result(f"成功获取链接：{target_text}")

def run_scheduler():
    """启动定时任务"""
    # 设置每天早上9点执行
    schedule.every().day.at("09:00").do(job)
    print(f"定时任务已启动，每天09:00自动执行")
    print("按 Ctrl+C 停止程序")
    
    # 循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    # 支持手动执行（测试用）和定时执行
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式：立即执行一次
        job()
    else:
        # 正常模式：启动定时任务
        try:
            run_scheduler()
        except KeyboardInterrupt:
            print("\n程序已手动停止")
        except Exception as e:
            print(f"程序异常停止：{str(e)}")

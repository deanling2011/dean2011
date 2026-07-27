import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import fitz   # PyMuPDF


# =====================
# 配置
# =====================

PDF_PATH = "../山图集.pdf"

OUTPUT_DIR = "../result"


# =====================
# 获取北京时间
# =====================

beijing = timezone(timedelta(hours=8))

today = datetime.now(beijing)

month = today.month
day = today.day


print("今天日期:", month, "月", day, "日")


# =====================
# 日期匹配规则
# 支持:
# 7月24日
# 7 月 24 日
# 7  月  24  日
# =====================

pattern = rf"{month}\s*月\s*{day}\s*日"

date_regex = re.compile(pattern)


print("匹配规则:", pattern)



# =====================
# 创建输出目录
# =====================

output_path = Path(OUTPUT_DIR)

output_path.mkdir(
    exist_ok=True
)



# =====================
# 打开PDF
# =====================

doc = fitz.open(PDF_PATH)


found = False



# =====================
# 搜索PDF页面
# =====================

for page_index, page in enumerate(doc):

    text = page.get_text()


    # 去掉多余空格
    clean_text = re.sub(
        r"\s+",
        "",
        text
    )


    # 匹配
    if date_regex.search(text) or date_regex.search(clean_text):


        print(
            "找到日期:",
            f"{month}月{day}日",
            "页码:",
            page_index + 1
        )


        # =====================
        # 页面转图片
        # =====================

        pix = page.get_pixmap(
            dpi=200
        )


        filename = (
            output_path /
            f"shantu-{month:02d}-{day:02d}.jpg"
        )


        pix.save(
            str(filename)
        )


        print(
            "生成图片:",
            filename
        )


        found = True


        break



# =====================
# 没找到
# =====================

if not found:

    print(
        "今天没有找到对应内容:",
        f"{month}月{day}日"
    )

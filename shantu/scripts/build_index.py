import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import fitz  # PyMuPDF


# =====================
# 基础路径
# =====================

BASE_DIR = Path(__file__).resolve().parent.parent


PDF_PATH = BASE_DIR / "山图集.pdf"

OUTPUT_DIR = BASE_DIR / "result"


# =====================
# 获取北京时间
# =====================

beijing = timezone(timedelta(hours=8))

today = datetime.now(beijing)

month = today.month
day = today.day


print("=====================")
print("今天日期:", month, "月", day, "日")
print("=====================")


# =====================
# 日期匹配
#
# 支持:
# 7月24日
# 7 月24 日
# 7  月  24  日
#
# =====================

pattern = rf"{month}\s*月\s*{day}\s*日"


date_regex = re.compile(pattern)


print("匹配规则:", pattern)


# =====================
# 创建输出目录
# =====================

OUTPUT_DIR.mkdir(
    exist_ok=True
)


print(
    "输出目录:",
    OUTPUT_DIR
)


# =====================
# 打开PDF
# =====================

if not PDF_PATH.exists():

    raise FileNotFoundError(
        f"找不到PDF文件:{PDF_PATH}"
    )


doc = fitz.open(
    PDF_PATH
)


found = False

result_images = []


# =====================
# 搜索PDF
# =====================

for page_index, page in enumerate(doc):


    text = page.get_text()


    # 去除所有空格
    clean_text = re.sub(
        r"\s+",
        "",
        text
    )


    if (
        date_regex.search(text)
        or
        date_regex.search(clean_text)
    ):


        print(
            "找到日期页面:",
            page_index + 1
        )


        # =====================
        # PDF页面转图片
        # =====================

        pix = page.get_pixmap(
            dpi=200
        )


        image_name = (
            f"shantu-{month:02d}-{day:02d}"
            f"-page-{page_index+1}.jpg"
        )


        image_path = OUTPUT_DIR / image_name


        pix.save(
            str(image_path)
        )


        result_images.append(
            image_name
        )


        print(
            "生成:",
            image_path
        )


        found = True



# =====================
# 生成HTML首页
# =====================


html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>山图集 {month}月{day}日</title>


<style>

body {{
    font-family:
    Arial,
    "Microsoft YaHei";

    padding:20px;
}}


img {{
    max-width:95%;
    margin-bottom:30px;
    border:1px solid #ddd;
}}

</style>


</head>


<body>


<h1>
山图集 {month}月{day}日
</h1>


"""


if found:


    for img in result_images:

        html += f"""

<h2>{img}</h2>

<img src="{img}">


"""


else:


    html += """

<h2>
今天没有找到对应日期
</h2>

"""


html += """

</body>

</html>

"""


index_file = OUTPUT_DIR / "index.html"


index_file.write_text(
    html,
    encoding="utf-8"
)



# =====================
# 输出结果
# =====================

print("=====================")

if found:

    print(
        "处理完成",
        result_images
    )

else:

    print(
        "未找到:",
        f"{month}月{day}日"
    )


print(
    "生成网页:",
    index_file
)

print("=====================")

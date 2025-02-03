import os,re

def split_novel(input_file):
    # 创建一个目录来存放拆分后的小文件
    output_dir = './data/novels/test'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取大的txt文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式匹配章节标题
    pattern = re.compile(r'第(\d+)章\s+(.*)')
    chapters = pattern.split(content)

    # 将匹配结果拆分成章节标题和内容
    for i in range(1, len(chapters), 3):
        chapter_number = chapters[i]
        chapter_title = chapters[i+1]
        chapter_content = chapters[i+2]

        # 写入小文件
        output_file = os.path.join(output_dir, f'第{chapter_number}章_{chapter_title}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'第{chapter_number}章 {chapter_title}\n\n{chapter_content}')

    print("拆分完成！")

# 调用函数来拆分小说
novel_path = "./data/novels/文抄公-妖武乱世.txt"
split_novel(novel_path)  # 替换'your_novel.txt'为你的大的txt文件路径

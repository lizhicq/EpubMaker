import re,os
from utils.epub_maker import create_epub_from_multiple_txts


def replace_novel_div(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    title = file_path.split('-')[-1].strip().replace('.txt','')
    
    modified_content = remove_ads_words(content)
    modified_content = remove_duplicates(modified_content)
    modified_content = modified_content.replace(title, '')
    modified_content = modified_content.replace('全球高武','')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(modified_content)

def remove_duplicates(input_str:str) -> str:
    lines = input_str.split('\n')
    seen = set()
    result = []
    
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    
    return '\n'.join(result)

def remove_ads_words(original_content: str) -> str:
    # 定义正则表达式模式，匹配多余的导航、广告等内容
    unwanted_phrases = [
        r"\（快捷键\s*←\）", r"\（快捷键\s*→\）",
        r"上一章", r"下一章", r"返回目录", r"加入书签", r"推荐本书",
        r"返回书页", r"返回顶部", r"我的藏书架", r"将本书加入书架",
        r"章节错误.*?举报", r"\|\s*", r"重要声明.*?小说.*?版权所有",
        r"飘天文学.*?小说阅读网", r"www\.piaotia\.com", r"Copyright.*",
        r"必应 搜^:*\择^日 网全网^最，快。",
        r"重要声明.*All rights reserved.",
        r"分享到\w+."
    ]

    # 移除不需要的词句
    for pattern in unwanted_phrases:
        original_content = re.sub(pattern, '', original_content, 0, re.DOTALL)

    # 清理多余的空行
    clean_text = re.sub(r"\n\s*\n", "\n", original_content).strip()
    
    return clean_text

    
if __name__ == '__main__':
    clean_dir = './data/tmp/全球高武'
    for file in os.listdir(clean_dir):
        file_path = os.path.join(clean_dir, file)
        replace_novel_div(file_path)
    
    create_epub_from_multiple_txts('老鹰小鸡','全球高武')
    
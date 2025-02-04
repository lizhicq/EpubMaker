import os,re

def extract_chapter_number(filename):
    match = re.search(r'第(\d+)章', filename)
    return int(match.group(1)) if match else None

dir_path = './data/txt'
files = [f for f in os.listdir(dir_path) if f.endswith('.txt') and extract_chapter_number(f) is not None]
files.sort(key=extract_chapter_number)

# print sorted files
for file in files:
    print(file)
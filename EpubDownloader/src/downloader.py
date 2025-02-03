from parser import * # type: ignore
from process_tracker import print_progress_bar
from multiprocessing import Pool, Manager
from cleaner import remove_ads_words, remove_duplicates
import os


def download_chapter(chapter, novel_tmp_path='./data/tmp'):
    try:
        url, title = chapter['url'], chapter['title']
        
        original_title = title.split('-')[-1] # new title example: 122-第122章 救援（为白银贺！）.txt
        
        content = extract_novel_chapter(url)
        content = content.replace(original_title, '') # Clean addition title in content
        content = remove_ads_words(content)
        content = remove_duplicates(content)
        
        output_file = os.path.join(novel_tmp_path, f'{title}.txt')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'{content}')
        return {'title': chapter['title'], 'url': url, 'content': content}
    except Exception as e:
        print('error message', chapter['title'], e)
        return {'title': chapter['title'], 'url': url, 'content': ""}
    

def download_novel(chapters:list, book:str):
    return main_process(chapters, book)

def save_chapters_to_text(chapters, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for chapter in chapters:
            if chapter:
                file.write(f"{chapter['title']}\n")
                file.write(f"{chapter['content']}\n")
                file.write("\n\n")  # Add extra newlines for readability between chapters


def task(chapter, progress_counter, lock, total_tasks, novel_tmp_path):
    """
    Sub task that downloads the chapter online
    """
    chapter = download_chapter(chapter, novel_tmp_path)
    with lock:
        progress_counter.value += 1
        print_progress_bar(progress_counter.value/total_tasks)
    return chapter
    
def main_process(chapters:list, book, tmp_dir='./data/tmp'):
    novel_tmp_path = os.path.join(tmp_dir, book)
    if not os.path.exists(novel_tmp_path):
        os.mkdir(novel_tmp_path)
    unfinished_chaps = [chap for chap in chapters if chap['content'] == "" 
        and f"{chap['title']}.txt" not in os.listdir(novel_tmp_path)]
    counter = 0
    print(unfinished_chaps)
    if not os.path.exists(novel_tmp_path):
        os.makedirs(novel_tmp_path)
    
    while len(unfinished_chaps) > 0:
        counter += 1
        manager = Manager()
        progress_counter = manager.Value('i', 0) # Shared integer
        lock = manager.Lock()
        print('\nunfinished', len(unfinished_chaps), 'total', len(chapters))
        tasks = [(chap, progress_counter, lock, len(unfinished_chaps), novel_tmp_path) 
                    for chap in unfinished_chaps]
        
        with Pool() as pool:
            results_async = pool.starmap_async(task, tasks)
            results = results_async.get()

        for result in results:
            for chap in chapters:
                if chap['title'] == result['title']:
                    chap['content'] = result['content']
        unfinished_chaps = [chap for chap in chapters if chap['content'] == "" 
                    and f"{chap['title']}.txt" not in os.listdir(novel_tmp_path)]
        print_progress_bar(1 - len(unfinished_chaps) / len(chapters))
        if counter > 10:
            break
        
    return list(chapters)
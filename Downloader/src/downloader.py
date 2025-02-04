import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from parser import *  # type: ignore
from process_tracker import print_progress_bar
from cleaner import remove_ads_words, remove_duplicates
import os

# 下载章节的异步函数
async def download_chapter(session: ClientSession, chapter, novel_tmp_path='./data/txt'):
    try:
        url, title = chapter['url'], chapter['title']
        
        original_title = title.split('-')[-1]  # new title example: 122-第122章 救援（为白银贺！）.txt
        
        async with session.get(url) as response:
            content = await response.text()
        
        content = content.replace(original_title, '')  # Clean addition title in content
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

# 下载任务的异步函数
async def task(chapter, session, progress_counter, lock, total_tasks, novel_tmp_path):
    """
    异步下载单个章节
    """
    chapter = await download_chapter(session, chapter, novel_tmp_path)
    async with lock:
        progress_counter[0] += 1  # 更新进度计数器
        print_progress_bar(progress_counter[0] / total_tasks)
    return chapter

# 主处理函数
async def main_process(chapters: list, book, tmp_dir='./data/txt'):
    novel_tmp_path = os.path.join(tmp_dir, book)
    if not os.path.exists(novel_tmp_path):
        os.mkdir(novel_tmp_path)

    unfinished_chaps = [chap for chap in chapters if chap['content'] == "" 
                        and f"{chap['title']}.txt" not in os.listdir(novel_tmp_path)]
    
    counter = 0
    print(unfinished_chaps)
    if not os.path.exists(novel_tmp_path):
        os.makedirs(novel_tmp_path)

    # 设置最大并发数
    MAX_CONCURRENT_REQUESTS = 300
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    progress_counter = [0]
    lock = asyncio.Lock()  # 使用 asyncio.Lock 保证进度的线程安全

    while len(unfinished_chaps) > 0:
        counter += 1
        print('\nunfinished', len(unfinished_chaps), 'total', len(chapters))

        # 使用 aiohttp 创建一个 ClientSession
        timeout = ClientTimeout(total=10)  # 设置超时
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            for chap in unfinished_chaps:
                task_coroutine = asyncio.ensure_future(task_with_semaphore(chap, session, progress_counter, lock, len(unfinished_chaps), novel_tmp_path, semaphore))
                tasks.append(task_coroutine)

            results = await asyncio.gather(*tasks)

        # 更新章节内容
        for result in results:
            for chap in chapters:
                if chap['title'] == result['title']:
                    chap['content'] = result['content']
        
        # 重新计算未下载的章节
        unfinished_chaps = [chap for chap in chapters if chap['content'] == "" 
                            and f"{chap['title']}.txt" not in os.listdir(novel_tmp_path)]
        print_progress_bar(1 - len(unfinished_chaps) / len(chapters))
        
        if counter > 10:
            break

    return list(chapters)

# 异步任务带有 Semaphore 的保护
async def task_with_semaphore(chapter, session, progress_counter, lock, total_tasks, novel_tmp_path, semaphore):
    async with semaphore:
        return await task(chapter, session, progress_counter, lock, total_tasks, novel_tmp_path)

# 启动事件循环
if __name__ == "__main__":
    chapters = [...]  # 章节列表
    book = "Some Book Title"
    asyncio.run(main_process(chapters, book))

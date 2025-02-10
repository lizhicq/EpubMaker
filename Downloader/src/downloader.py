import asyncio
import aiohttp
import os
from parser import *  # type: ignore
from process_tracker import print_progress_bar
from cleaner import remove_ads_words, remove_duplicates


async def download_chapter(chapter, novel_tmp_path='./data/txt'):
    try:
        url, title = chapter['url'], chapter['title']
        
        original_title = title.split('-')[-1]  # new title example: 122-第122章 救援（为白银贺！）.txt
        
        content = await extract_novel_chapter(url)  # Assuming `extract_novel_chapter` can be awaited
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


async def fetch_chapters(chapters, novel_tmp_path):
    tasks = [download_chapter(chap, novel_tmp_path) for chap in chapters]
    results = await asyncio.gather(*tasks)
    return results


def main_process(chapters: list, book, tmp_dir='./data/txt'):
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
        print('\nunfinished', len(unfinished_chaps), 'total', len(chapters))
        
        # Fetch chapters asynchronously
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(fetch_chapters(unfinished_chaps, novel_tmp_path))

        # Update chapter content with fetched results
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

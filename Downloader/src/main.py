from downloader import download_novel
from parser import * # type: ignore
from cleaner import *
from utils.epub_maker import create_epub_from_multiple_txts
import time

def main():
    url = "https://www.piaotia.com/html/14/14836/"
    author = '卖报小郎君'
    book = '灵境行者'
    
    max_retry = 5
    delay = 5
    for attempt in range(max_retry):
        try:
            chapters = get_novel_chapters(url)
            chapters = download_novel(chapters, book)
            break
        except Exception as e:
            if "ERR_CONNECTION_CLOSED" in str(e):
                print(f"Attempt {attempt + 1} failed with connection closed error. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            elif "No such file or director" in str(e):
                print(f"Attempt {attempt + 1} failed with dir creation error. Retrying in {delay} seconds...")
                print(str(e))
                time.sleep(delay)  # Wait before retrying
            else:
                print("Main process An unexpected error occurred:", e)
                break  # Exit retry loop if a different error occurs
    
    # save_chapters_to_text(chapters,save_path)
    create_epub_from_multiple_txts(author,book)
    
    
if __name__ == "__main__":
    main()

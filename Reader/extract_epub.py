# Extract a epub file to multiple text files

import os
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

def extract_epub_to_txt(epub_file, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the EPUB file
    book = epub.read_epub(epub_file)
    book.items[1].get_type()
    # Extract chapters and save them as separate .txt files
    for idx, item in enumerate(book.get_items(), start=1):
        if item.get_type() == ITEM_DOCUMENT:
            # Extract text content using BeautifulSoup
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            if soup is None:
                continue
            text = soup.get_text()
            title = soup.find('h2') #soup.find('h2', class_='titlel2std', id='title')
            title = title.get_text().strip() if title else 'XXX'
            title = title.replace('/', '\\')
            print(f"title={title}, idx={idx},{text[:50]}")
            # Create a .txt file for each chapter/section
            filename = os.path.join(output_folder, f'{idx:03d}-{title}.txt')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)

    print(f"EPUB content extracted to folder: {output_folder}")

if __name__ == "__main__":
    epub_file = '/Users/lizhicq/iCloud/Novel/神级大魔头.epub'  # Replace with your EPUB file path
    output_folder = '/Users/lizhicq/GitHub/EpubMaker/data/txt/神级大魔头'  # Replace with your desired output folder path
    extract_epub_to_txt(epub_file, output_folder)
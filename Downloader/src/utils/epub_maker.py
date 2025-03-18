import os
from ebooklib import epub
from Downloader.src import cleaner

def extract_chapter_number(filename:str):
    # match = re.search(r'第(\d+)', filename)
    # return int(match.group(1)) if match else float('inf')
    index = filename.split('-')[0]
    return int(index)

def create_epub_from_multiple_txts(author, book_name, in_dir='./data/txt', out_dir='./data/epub'):
    book = epub.EpubBook()
    # Set the title and author
    book_id = author + '-' + book_name
    book.set_identifier(book_id)
    book.set_title(book_id)
    book.set_language('ch')
    book.add_author(author)
    
    if book_name not in in_dir:
        in_dir = os.path.join(in_dir, book_name)
    if not os.path.exists(in_dir):
        os.makedirs(in_dir)
    files = [f for f in os.listdir(in_dir) if f.endswith('.txt')]
    files.sort(key=extract_chapter_number)
    toc = []
    spine = ['nav']
    for i, file in enumerate(files):
        file_path = os.path.join(in_dir, file)
        title = file.replace('.txt', '')
        chapter_file = f'{title}.xhtml'
        chapter = epub.EpubHtml(
            title=title, 
            file_name=chapter_file, lang='ch')
        
        # Create Content with paragraphs
        with open(file_path, 'r') as f:
            content = f.read()
            content = cleaner.remove_ads_words(content)

            paragraphs = content.split('\n')
            content = ''.join(f'<p>{p}</p>' for p in paragraphs)
            chapter.content = f'<h1>{title}</h1><p>{content}</p>'
        
        book.add_item(chapter)
        toc.append(epub.Link(chapter_file, title, f'chap{i}'))
        spine.append(chapter)
    # Create a table of contents
    book.toc = tuple(toc)
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # Add CSS file
    book.add_item(nav_css)

    # Create book spine
    book.spine = spine

    # Create EPUB file
    output_file_path = os.path.join(out_dir, book_id)
    epub.write_epub(f'{output_file_path}.epub', book, {})
    print('Epub file is successfully created')
    
    
if __name__ == '__main__':
    create_epub_from_multiple_txts(
        author='文抄公',
        book_name='星空职业者',
    )

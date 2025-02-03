from src.parser import extract_novel_chapter 

def test_extract_novel_chapter():
    result = extract_novel_chapter("https://www.piaotia.com/html/15/15296/10618594.html")
    size = len(result)
    if size > 1000:
        assert len(result) > 5000, "The length of the result is not greater than 10000"

test_extract_novel_chapter()

import src.cleaner
import unittest

class TestCleaner(unittest.TestCase):
    def setUp(self):
        with open('tests/data/Sample Chapter.html') as f:
            self.txt = f.read()
            
    def test_remove_ads_words(self):
        result = src.cleaner.remove_ads_words(self.txt)
        unwanted_phrases = [
            r"\（快捷键\s*←\）", r"\（快捷键\s*→\）",
            r"上一章", r"下一章", r"返回目录", r"加入书签", r"推荐本书",
            r"返回书页", r"返回顶部", r"我的藏书架", r"将本书加入书架",
            r"章节错误.*?举报", r"\|\s*", r"重要声明.*?小说.*?版权所有",
            r"飘天文学.*?小说阅读网", r"www\.piaotia\.com", r"Copyright.*"
        ]
        for phrase in unwanted_phrases:
            self.assertNotRegex(result, phrase)

if __name__ == '__main__':
    unittest.main()
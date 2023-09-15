import unittest
import tempfile
import os
from main import preprocess_text, read_text_file, calculate_similarity


class TestSimilarityCalculation(unittest.TestCase):
    def setUp(self):
        # 创建临时测试文件，以便测试文本预处理、文本读取和相似度计算功能
        self.original_text = r"D:\Python Project\Software Project\Plagiarism\orig.txt"
        self.plagiarized_text = r"D:\Python Project\Software Project\Plagiarism\orig_0.8_add.txt"
        self.original_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.plagiarized_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.original_file.write(self.original_text)
        self.plagiarized_file.write(self.plagiarized_text)
        self.original_file.close()
        self.plagiarized_file.close()

    def tearDown(self):
        # 清理临时测试文件
        os.remove(self.original_file.name)
        os.remove(self.plagiarized_file.name)

    def test_preprocess_text(self):
        # 测试文本预处理函数
        preprocessed_text = preprocess_text(self.original_text)
        # 预期的预处理结果，移除了标点符号，并在单词之间加上了空格
        expected_preprocessed_text = r"D:\Python Project\Software Project\Plagiarism\orig.txt"
        self.assertEqual(preprocessed_text, expected_preprocessed_text)

    def test_read_text_file(self):
        # 测试文本读取函数
        text = read_text_file(self.original_file.name)
        # 预期的读取结果应该与原始文本一致
        self.assertEqual(text, self.original_text)

    def test_calculate_similarity(self):
        # 测试文本相似度计算函数
        similarity_score = calculate_similarity(self.original_text, self.plagiarized_text)
        # 预期的相似度分数
        expected_similarity_score = 0.79
        # 使用assertAlmostEqual来测试浮点数相等性，保留两位小数
        self.assertAlmostEqual(similarity_score, expected_similarity_score, places=2)


if __name__ == '__main__':
    unittest.main()

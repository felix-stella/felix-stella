import unittest
import tempfile
from main import *


class TestSimilarityCalculation(unittest.TestCase):
    def test_calculate_similarity(self):
        # 创建临时测试文件，以便测试文本预处理、文本读取和相似度计算功能
        original_text = "orig.txt"
        plagiarized_text = "orig_0.8_add.txt"
        original_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        plagiarized_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        original_file.write(original_text)
        plagiarized_file.write(plagiarized_text)
        original_file.close()
        plagiarized_file.close()

        # 创建 TextSimilarityCalculator 的实例并计算相似度
        calculator = TextSimilarityCalculator(original_file.name, plagiarized_file.name)
        calculator.calculate_similarity()

        # 获取计算后的相似度分数并进行断言
        similarity_score = calculator.similarity_score
        self.assertGreaterEqual(similarity_score, 0.0)
        self.assertLessEqual(similarity_score, 1.0)

        # 清理临时测试文件
        os.remove(original_file.name)
        os.remove(plagiarized_file.name)


if __name__ == '__main__':
    unittest.main()

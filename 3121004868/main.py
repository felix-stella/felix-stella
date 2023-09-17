import os
import jieba
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityCalculator:
    def __init__(self, original_text, plagiarized_text):
        self.original_text = original_text
        self.plagiarized_text = plagiarized_text
        self.similarity_score = None  # 初始化相似度分数为 None

    @staticmethod
    def preprocess_text(text):
        words = jieba.cut(text)
        return ' '.join(words)

    def calculate_similarity(self):
        preprocessed_original_text = self.preprocess_text(self.original_text)
        preprocessed_plagiarized_text = self.preprocess_text(self.plagiarized_text)

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_original_text, preprocessed_plagiarized_text])

        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        self.similarity_score = similarity[0][0]  # 将相似度分数保存在实例变量中
        return self.similarity_score

    def calculate_and_save_similarity(self, output_file):
        similarity_score = self.calculate_similarity()
        similarity_score = round(similarity_score, 2)

        print(f"文本相似度分数: {similarity_score:.2f}")

        with open(output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(f"文本相似度分数: {similarity_score:.2f}\n")


class FileNotFoundError(Exception):
    """自定义异常类：文件未找到异常"""

    def __init__(self, file_path, error_code=None):
        super().__init__(f"File not found: {file_path}")
        self.file_path = file_path
        self.error_code = error_code

    def log_error(self):
        """将错误信息记录到日志文件"""
        if self.error_code:
            with open("error.log", "a") as log_file:
                log_file.write(f"Error Code: {self.error_code}\n")
                log_file.write(f"File not found: {self.file_path}\n")


# 在使用时，可以提供额外的错误代码和文件路径
try:
    file_path = "example.txt"
    raise FileNotFoundError(file_path, error_code=404)
except FileNotFoundError as e:
    print(f"Error: {e}")
    e.log_error()


class TextTooShortError(Exception):
    """自定义异常类：文本过短异常"""

    def __init__(self, min_length, text=None):
        super().__init__(f"Text is too short. Minimum length: {min_length}")
        self.min_length = min_length
        self.text = text

    def suggest_correction(self):
        """提供建议的文本纠正"""
        if self.text:
            return f"Consider adding more content to the text: {self.text}"


# 在使用时可提供文本和最小长度
try:
    min_length = 100
    text = "This is a short text."
    raise TextTooShortError(min_length, text=text)
except TextTooShortError as e:
    print(f"Error: {e}")
    correction_suggestion = e.suggest_correction()
    if correction_suggestion:
        print(correction_suggestion)


def main():
    parser = argparse.ArgumentParser(description='Calculate text similarity.')
    parser.add_argument('original', type=str, help='Absolute path to the original text file')
    parser.add_argument('plagiarized', type=str, help='Absolute path to the plagiarized text file')
    parser.add_argument('output', type=str, help='Absolute path to the output file')

    args = parser.parse_args()

    original_text = read_text_file(args.original)
    plagiarized_text = read_text_file(args.plagiarized)

    calculator = TextSimilarityCalculator(original_text, plagiarized_text)
    calculator.calculate_and_save_similarity(args.output)


def read_text_file(filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


if __name__ == "__main__":
    main()

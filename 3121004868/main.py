import os
import jieba
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 获取当前脚本所在的目录
def get_current_directory():
    return os.path.dirname(os.path.abspath(__file__))


# 对文本进行预处理，包括分词
def preprocess_text(text):
    words = jieba.cut(text)
    return ' '.join(words)


# 从文件中读取文本内容
def read_text_file(filename):
    file_path = os.path.join(get_current_directory(), filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


# 计算文本相似度
def calculate_similarity(text1, text2):
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]


# 主函数，接受命令行参数，计算相似度并输出结果
def main(original_file, plagiarized_file, output_file):
    # 读取文本内容
    text1 = read_text_file(original_file)
    text2 = read_text_file(plagiarized_file)

    # 计算文本相似度
    similarity_score = calculate_similarity(text1, text2)
    similarity_score = round(similarity_score, 2)  # 保留两位小数
    print("文本相似度分数:", similarity_score)

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(f"文本相似度分数: {similarity_score:.2f}\n")


if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Calculate text similarity.')
    parser.add_argument('original', type=str, help='Absolute path to the original text file')
    parser.add_argument('plagiarized', type=str, help='Absolute path to the plagiarized text file')
    parser.add_argument('output', type=str, help='Absolute path to the output file')

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数进行文本相似度计算
    main(args.original, args.plagiarized, args.output)

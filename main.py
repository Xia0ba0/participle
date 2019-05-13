from participle import Article
from participle import Participle

from utils import exe_time
from utils import get_size
from utils import get_real_cut


def ex4():
    # 传入词典， 初始化分词器
    resolver = Participle(r'.\words.txt')

    # 遍历样本集合并分词 返回一个 Article Object List
    # article_list = resolver.resolve_dir(r'.\体育领域\体育分类测试文档')

    """
    用Article 静态方法 get_idf_json_file 统计样本集中各词语的idf值
    #传入上一步得到的 Article Object List
    #在当前目录生成 idf.json
    """

    # Article.get_idf_json_file(articles_list)

    # 装饰器exe_time接受一个函数 返回这个函数的执行结果，以及执行时间
    # resovler.resovle_file 返回文章的Article 对象实例
    @exe_time
    def get_time():
        return resolver.resolve_file('./test1.txt')

    # 获取执行时间，文件大小
    article1, time = get_time()
    size = get_size(article1.file_name)
    print("speed: %fs/k" % (time / (size / 1024)))

    # 获取jieba分词结果
    cut = get_real_cut(article1.file_name)
    right_num = 0
    for word in article1.words:
        if word in cut:
            right_num += 1
    print("relative accuracy: %f%%" % (right_num * 100 / article1.total_count))

    article1.get_w()
    print("keywords of %s: " % article1.file_name)
    for keyword, weight in article1.get_top_10():
        print(keyword, weight)

    article2 = resolver.resolve_file(r'./test2.txt')
    article2.get_w()
    print("keywords of %s: " % article2.file_name)
    for keyword, weight in article2.get_top_10():
        print(keyword, weight)

    """
    Article static method： get_similarity
            接受两个Article对象 生成Article.words 的 numpy.array() 向量
            返回夹角余弦方法计算的这两篇文本间的相似度
    """
    similarity = Article.get_similarity(article1, article2)
    print("similarity between %s and %s is: %f" % (article1.file_name, article2.file_name, similarity))


def ex5():
    resolver = Participle(r'.\words.txt')
    resolver.resolve_dir(r'.\体育领域\体育分类测试文档')


if __name__ == '__main__':
    #ex4()
    ex5()

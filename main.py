from participle import Article
from participle import Participle

from utils import exe_time
from utils import get_size
from utils import get_real_cut

if __name__ == '__main__':
    # 传入词典， 初始化分词器
    resolver = Participle(r'.\words.txt')

    # 遍历样本集合并分词 返回一个 Article Object List， 位于resolver.article_list
    # resolver.resolve_dir(r'.\体育领域\体育分类测试文档')

    """
    用Article 静态方法 get_idf_json_file 统计样本集中各词语的idf值
    #传入上一步得到的 Article Object List
    #在当前目录生成 idf.json
    """


    # Article.get_idf_json_file(resolver.articles_list)

    # 装饰器exe_time接受一个函数 返回这个函数的执行结果，以及执行时间
    # resovler.resovle_file 返回文章的Article 对象实例
    @exe_time
    def get_time():
        return resolver.resolve_file('./test.txt')


    # 获取执行时间，文件大小
    article, time = get_time()
    size = get_size(article.file_name)
    print("speed: %fs/k" % (time / (size / 1024)))

    # 获取jieba分词结果
    cut = get_real_cut(article.file_name)
    right_num = 0
    for word in article.words:
        if word in cut:
            right_num += 1
    print("relative accuracy: %f%%" % (right_num * 100 / article.total_count))

    article.get_w()
    for keyword, weight in article.get_top_10():
        print(keyword, weight)

import os
import datetime
from participle import Article
from participle import Participle

if __name__ == '__main__':
    # 传入词典， 初始化分词器
    resolver = Participle(r'.\words.txt')

    start = datetime.datetime.now()
    article = resolver.resolve_file('./test.txt')

    # 遍历样本集合并分词 返回一个 Article Object List， 位于resolver.article_list
    # resolver.resolve_dir(r'.\体育领域\体育分类测试文档')

    end = datetime.datetime.now()
    runtime = (end - start).total_seconds()
    size = os.path.getsize('./test.txt')
    Word_Segmentation_Speed = 1024 * runtime / size
    print('The speed of word segmentation is %fs/k' %Word_Segmentation_Speed)

    """
    用Article 静态方法 get_idf_json_file 统计样本集中各词语的idf值
    #传入上一步得到的 Article Object List
    #在当前目录生成 idf.json
    """
    # Article.get_idf_json_file(resolver.articles_list)

    article.get_w()
    print(article.w)

from participle import Article
from participle import Participle
import json

def show_idf():
    with open('idf.json','r') as idf:
        json_string = json.load(idf)
        print(json_string)

if __name__ == '__main__':

    # 传入词典， 初始化分词器
    resolver = Participle(r'.\words.txt')

    # 遍历样本集合并分词 返回一个 Article Object List， 位于resolver.article_list
    resolver.resolve_dir(r'.\体育领域\体育分类测试文档\01足球')

    #用Article 静态方法 get_idf_json_file 统计样本集中各词语的idf值
    #传入上一步得到的 Article Object List
    #在当前目录生成 idf.json
    Article.get_idf_json_file(resolver.articles_list)
    #show_idf()
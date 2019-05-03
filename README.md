# ***TO LiLiang：***

## ***Done*** :
+ ***words.txt*** 是分词词典，我把老师给的两个词典给合并了

+ ***体育领域*** 是样本集，用来统计idf值

+ ***Article*** 是文本类，用来获取单文件 和 样本集的统计信息

+ ***Participle*** 是分词器， 可以单文件分词 和 深度优先遍历目录分词

+ ***Article*** 的静态方法 ***Article.get_idf_json_file*** 接受一个 ***Article Object List*** 参数， 统计样本集中各个词语的 ***idf*** 值，  然后在当前目录生成 ***idf.json***

## ***TODO*** :
1. ***Article*** 类的词语权重计算方法
2. 分词效果评估
3. 词云 和 直方图
4. 文本相似度分析


![](https://s2.ax1x.com/2019/05/02/ENKXMd.jpg)
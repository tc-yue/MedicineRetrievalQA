### Waston QA 项目说明
- evidence_retrieval 支持证据获取
    - analyzer 用于whoosh的query 分词器
    - sql_data_source 根据疾病查询对应药品
    - whoosh_data_source 基于whoosh检索支持证据
- files
    - 各类模型及文件
- filter
    - evidence_retrieval证据过滤，用于检索后处理
- model
    - question 问题类，调用set_question方法，获取问题的各类属性。绑定证据，候选答案。
    - cqa_evidence 证据类 继承问题类，增加snippet和score
    - questiontype 问题类型枚举类
- question_type_analysis 
    - pattern_based 基于模板医药相关分类
    - question_classification 用于对话管理器的对话分类
- score 
    - sentence_similarity 问句相似度计算
    - word_similarity 基于哈工大同义词词典的词语相似度计算，时间复杂度较高，线上未用。
    - evidence_score 证据打分模块，未来考虑加入衡量答案准确性
- system
    - medicine_qa 药品问答
- word_parser
    - ltp_dependency 句法分析，线上未用
    - parser 分词，词性标注，实体识别，关键词抽取等
conversation_manager
对话管理器，根据句子分类结果，调用医药问答，图灵api，未来考虑通用问答等等

TODO
- [ ] -数据库，mysql访问速度。
- [ ] 相对导入问题？
- [ ] 异常测试
- [ ] 检索引擎，solr，elasticsearch等等，药品结构化数据库
- [ ] 匹配准确度，实体识别，问题分类等模块。
![输入图片说明](https://gitee.com/uploads/images/2018/0113/191059_6b8691d0_1052945.png "未命名文件 (2).png")
对于用户对话，首先基于医药词典匹配分类，调用图灵api或者医药问答
对于医药问答，实例化问题类，当问什么药时调用sql问答，否则调用cqa。先进行检索支持，后续评分，选择答案返回
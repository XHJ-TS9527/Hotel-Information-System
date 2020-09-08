from classify import predict_sen, predict_txt

###########------readme------#########
'''
使用svm分类，交叉验证0.799，效果一般，但基本可预测大部分评论，阴阳怪气
的评论难以应付
两种使用方法
1.使用txt文件，txt务必使用utf-8编码，否则打开出错，若有大量文件非utf-8
编码，可尝试with open(.... errors='ignore') as f 避免出错，但并非适用
于所有情况
2.直接输入评价的字符串
看以下demo了解更多
'''


sentence = r'旅馆住的很舒服，非常满意，环境很干净，十分享受！'
result = predict_sen(sentence)
print(result)

# txt_dir = r'./demo.txt'
# result = predict_txt(txt_dir)
# print(result)
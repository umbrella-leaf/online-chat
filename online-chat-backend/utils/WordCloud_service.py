import base64
import jieba
import wordcloud
import pandas as pd
from io import BytesIO
from PIL import Image


def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    img_str = str(img_str, "utf-8")
    return img_str


class WordCloud:
    def __init__(self):
        self.wordcloud = wordcloud.WordCloud(font_path="msyh.ttc",
                                             width=700, height=490,
                                             background_color='white',
                                             max_words=300)
        self.stop_words = ["图片", "表情", "图片表情"]

    def get_word_cloud(self, messages):
        # panda格式化数据
        data = pd.DataFrame(messages)
        data = data[['content']]
        string = ''
        for index in data.index:
            message = data.loc[index]['content']
            if message != '':
                string += message
        # 结巴分词
        jieba_res = jieba.lcut(string)
        words_list = []
        for res in jieba_res:
            if res not in self.stop_words and len(res) >= 2:
                words_list.append(res)
        words_txt = " ".join(words_list)
        # 生成词云照片
        self.wordcloud.generate(words_txt)
        # 转化为base64格式
        matrix_RGB = self.wordcloud.to_array()
        image = Image.fromarray(matrix_RGB)
        return f"data:image/JPEG;base64,{im_2_b64(image)}"





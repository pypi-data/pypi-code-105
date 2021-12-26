from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import os

class HealthWorldCloud:
    def __init__(self,data_path=""):
        self.data_path=data_path

    def get_freq(self,text):
        stop_words = stopwords.words('english')
        words = {}
        ls = text.strip().split("\n")
        for l in ls:
            l = l.strip()
            wl = l.split(" ")
            for w in wl:
                w = w.strip().lower()
                if w not in stop_words:
                    if w in words:
                        words[w] += 1
                    else:
                        words[w] = 1
        return words

    def show_image(self,text):
        wc = WordCloud(background_color="white",
                       width=480,
                       height=480,
                       max_font_size=60,
                       max_words=1000)
        # generate word cloud
        wc.generate_from_frequencies(text)

        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def show(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        if self.data_path=="":
            self.data_path=os.path.join(current_path,"data/metaverse-news.txt")
        text = open(self.data_path, 'r', encoding='utf-8')
        text = text.read()
        self.show_image(self.get_freq(text))


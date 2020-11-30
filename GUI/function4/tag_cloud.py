from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import pandas as pd 
import re  
from pyvi import ViTokenizer

class Process():
    def english(self, df):
        comment_words = '' 
        with open('english_stopwords.txt', encoding="utf8") as f:
            stopwords = []
            for line in f:
                stopwords.append("".join(line.strip().split()))  
                
        for i in range(0, len(df)):
            review = re.sub(r"pic.twitter\S+",'',df[i])
            review = re.sub(r"http\S+", "", review)
            review = re.sub(r"@\S+", "", review)
            review = re.sub(r"www.\S+", "", review)
            review = re.sub('[^a-zA-Z]',' ', review)
            review = review.lower()
            review = review.split()
            review = [word for word in review if not word in set(stopwords)]
            comment_words += " ".join(review)+" "
        
        wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='White', 
                        min_font_size = 10).generate(comment_words) 
                                
        plt.figure(figsize = (8,8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        plt.show() 

    def vietnam(self, df):
        with open('vietnamese_stopwords.txt', encoding="utf8") as f:
            stopwords = []
            for line in f:
                stopwords.append("_".join(line.strip().split()))

        corpus = []
        #for i in range(0, 3964):
        for i in range(0, len(df)):
            review = re.sub(r"pic.twitter\S+",'',df[i])
            review = re.sub(r"http\S+", "", review)
            review = re.sub(r"#\S+", "", review)
            review = re.sub(r"@\S+", "", review)
            review = re.sub('[_]','',review)
            review = re.sub('[^a-zA-Z_áàạảãăắằặẵẳâấầẩậẫđíỉìịĩóòỏọõôốồổộỗơớờởợỡéèẹẽẻêếềểệễúùủũụưứừửựữýỳỷỹỵÁÀẢÃẠĂẮẰẲẲẶẴÂẤẦẬẪẨĐÍÌỈỊĨÓÒỎỌÕÔỐỒỔỘỖƠỚỜỞỢỠÉÈẺẸẼÊẾỀỆỂỄÚÙỦŨỤƯỨỪỬỰỮÝỲỶỴỸ]',
                            ' ',review)
            review = ViTokenizer.tokenize(review)
            review = review.lower()
            review = review.split()
            review = [word for word in review if not word in  set(stopwords)]
            review = ' '.join(review)
            corpus.append(review)

        comment_words =''    
        for review in corpus:
            comment_words += review + ' '
        comment_words = re.sub('[_]',' ',comment_words)
        
        from wordcloud import WordCloud    
        wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='White', 
                        min_font_size = 10).generate(comment_words) 

        plt.figure(figsize = (8, 8)) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show() 
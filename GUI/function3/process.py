import numpy as np
import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
import ast
from pyvi import ViTokenizer
import joblib
class Emotion():
    def get_data_en(self, dataset):
        corpus = []
        with open('english_stopwords.txt', encoding="utf8") as f:
            stopwords = []
            for line in f:
                stopwords.append("".join(line.strip().split()))  
        for i in range(0, len(dataset)):
            review = re.sub(r"pic.twitter\S+",'',dataset[i])
            review = re.sub(r"http\S+", "", review)
            review = re.sub(r"@\S+", "", review)
            review = re.sub('[^a-zA-Z]', ' ', review)
            review = review.lower()
            review = review.split()
            ps = PorterStemmer()
            review = [ps.stem(word) for word in review if not word in set(stopwords)]
            corpus.append(review)

        file = open("word_index_en.txt", "r")
        contents = file.read()
        word_index = ast.literal_eval(contents)
        file. close()

        #corpus1 = corpus

        for i in range(0, len(corpus)):
            for j in range(0, len(corpus[i])):
                try:
                    corpus[i][j]=word_index[corpus[i][j]]
                except KeyError:
                    corpus[i][j]=0

        from tensorflow.python.keras.preprocessing.sequence import pad_sequences
        status_pad = pad_sequences(corpus, maxlen=20)

        from keras.models import load_model
        model1 = load_model('model1_en.h5')

        result=model1.predict(status_pad)
        np.argmax(result, axis=1)
        for i in range(0,len(result)):
            t = result[i][0]
            result[i][0] = result[i][1]
            result[i][1] = t
        return result
        
    def get_data_vi(self, dataset):
        with open('vietnamese_stopwords.txt', encoding="utf8") as f:
            stopwords = []
            for line in f:
                stopwords.append("_".join(line.strip().split()))
        corpus = []
        for i in range(0, len(dataset)):
            review = re.sub(r"pic.twitter\S+",'',dataset[i])
            review = re.sub(r"http\S+", "", review)
            review = re.sub(r"#\S+", "", review)
            review = re.sub(r"@\S+", "", review)
            review = re.sub('[_]',' ',review)
            review = re.sub('[^a-zA-Z_áàạảãăắằặẵẳâấầẩậẫđíỉìịĩóòỏọõôốồổộỗơớờởợỡéèẹẽẻêếềểệễúùủũụưứừửựữýỳỷỹỵÁÀẢÃẠĂẮẰẲẲẶẴÂẤẦẬẪẨĐÍÌỈỊĨÓÒỎỌÕÔỐỒỔỘỖƠỚỜỞỢỠÉÈẺẸẼÊẾỀỆỂỄÚÙỦŨỤƯỨỪỬỰỮÝỲỶỴỸ]',
                            ' ',review)
            review = ViTokenizer.tokenize(review)
            review = review.lower()
            review = review.split()
            review = [word for word in review if not word in  set(stopwords)]
            review = ' '.join(review)
            corpus.append(review)

        tfidf_vect = joblib.load('tfidf_vect.pkl')

        x_test_tfidf =  tfidf_vect.transform(corpus)

        svd = joblib.load('svd.pkl')

        x_test_tfidf_svd = svd.transform(x_test_tfidf)

        classifier = joblib.load('classifier.pkl')

        y_test = classifier.predict(x_test_tfidf_svd)

        result= np.zeros((len(y_test),2))
        for i in range(len(y_test)):
            result[i,y_test[i]] = 1
        return result

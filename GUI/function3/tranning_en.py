# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

# Importing the dataset
dataset = pd.read_csv('training.csv', sep=',' ,names=['target','id','date','flag','user','text'] ,encoding='latin-1')

# Xử lý dữ liệu đầu vào
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, len(dataset['text'])):
    review = re.sub(r"pic.twitter\S+",'',dataset['text'][i])
    review = re.sub(r"http\S+", "", review)
    review = re.sub(r"@\S+", "", review)
    review = re.sub(r"www.\S+", "", review)
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    corpus.append(review)


# Tạo model word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  
from gensim.models import Word2Vec  
model = Word2Vec(corpus, size=100, window=10, min_count=3, workers=4, sg=1)

# Lưu model word2vec
from gensim.test.utils import get_tmpfile
path = get_tmpfile("word2vec_en.model")
model.save("word2vec_en.model")

# biến đổi corpus từ chữ sang status_pas số để đưa vào model để train
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
tokenizer_obj = Tokenizer()
tokenizer_obj.fit_on_texts(corpus)
sequences = tokenizer_obj.texts_to_sequences(corpus)
word_index = tokenizer_obj.word_index
status_pad = pad_sequences(sequences, maxlen=20)

# lưu lại word_index
f = open("word_index_en.txt","w")
f.write( str(word_index))
f.close()

# xây dựng embedding matrix
EMBEDDING_DIM =100
num_words = len(word_index) + 1
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word in model.wv.vocab:
    i=word_index[word]
    embedding_matrix[i] = model.wv[word]
    
# gán lại nhãn output
y=[]
for i in range(0, 1600000):
    if dataset['target'][i] == 0 :
        y.append([0, 1])
    if dataset['target'][i] == 4 :
        y.append([1, 0])
y = np.asarray(y)        


            
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(status_pad, y, test_size = 0.25, random_state = 0)

# xây dựng mô hình CNN dùng để phân loại
model1 = Sequential()
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                             input_length=20,
                            trainable=False)

model1.add(embedding_layer)
model1.add(Conv1D(filters=512, kernel_size=5, activation='relu'))
model1.add(Conv1D(filters=128, kernel_size=5, activation='relu'))
model1.add(Conv1D(filters=128, kernel_size=5, activation='relu'))
model1.add(MaxPooling1D(pool_size=2))
model1.add(Flatten())
model1.add(Dense(64, input_dim=1, activation='relu'))
model1.add(Dense(10, activation='relu'))
model1.add(Dense(2, activation='softmax'))
model1.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
print(model1.summary())
history=model1.fit(x_train, y_train, validation_data=(x_val, y_val),epochs=5,batch_size=64,verbose=2)
plt.plot(history.history['val_acc'])
plt.plot(history.history['acc'])
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.show()

# Lưu lại model1
model1.save('model1_en.h5')

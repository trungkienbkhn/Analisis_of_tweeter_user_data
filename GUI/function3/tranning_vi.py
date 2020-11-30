# Importing the libraries
import pandas as pd
import joblib

# Importing the dataset
dataset = pd.read_csv('vi_train.csv')
del dataset['index']

# Xử lý dữ liệu đầu vào
import re
from pyvi import ViTokenizer
with open('vietnamese_stopwords.txt', encoding="utf8") as f:
    stopwords = []
    for line in f:
        stopwords.append("_".join(line.strip().split()))
corpus = []
for i in range(0, 3964):
    review = re.sub(r"pic.twitter\S+",'',dataset['content'][i])
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

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect = TfidfVectorizer(analyzer='word', max_features=30000)
tfidf_vect.fit(corpus) 
X_data_tfidf =  tfidf_vect.transform(corpus)

joblib.dump(tfidf_vect, 'tfidf_vect.pkl')

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=300, random_state=42)
svd.fit(X_data_tfidf)
X_data_tfidf_svd = svd.transform(X_data_tfidf)

joblib.dump(svd, 'svd.pkl')

y = dataset.iloc[:,0].values 
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(X_data_tfidf_svd, y, test_size = 0.25, random_state = 0)

from sklearn import svm
classifier = svm.SVC()
classifier.fit(x_train, y_train)
train_predictions = classifier.predict(x_train)
val_predictions = classifier.predict(x_val)

joblib.dump(classifier, 'classifier.pkl')

from sklearn import metrics
print("Validation accuracy: ", metrics.accuracy_score(val_predictions, y_val))



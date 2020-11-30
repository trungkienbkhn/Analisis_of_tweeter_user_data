from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import pandas as pd 
import re  
 
df = pd.read_csv(r"trump.csv", encoding ="latin-1") 

comment_words = '' 
with open('english_stopwords.txt', encoding="utf8") as f:
    stopwords = []
    for line in f:
        stopwords.append("".join(line.strip().split()))  
        
for i in range(0, len(df['CONTENT'])):
    review = re.sub(r"pic.twitter\S+",'',df['CONTENT'][i])
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
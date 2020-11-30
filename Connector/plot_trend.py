import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from GUI.function3.process import Emotion
emotion = Emotion()

#plot trending tweet following days
# 0 : date1 < date2, 1 : date1 > date2
def compare_dates(date1, date2):

    date1_list = date1.split('-')
    date2_list = date2.split('-')
    if int(date1_list[0]) < int(date2_list[0]):
        return 0
    elif int(date1_list[0]) > int(date2_list[0]):
        return 1
    elif int(date1_list[1]) < int(date2_list[1]):
        return 0
    elif int(date1_list[1]) > int(date2_list[1]):
        return 1
    elif int(date1_list[2]) < int(date2_list[2]):
        return 0
    elif int(date1_list[2]) > int(date2_list[2]): 
        return 1
    else:
        return 2

# 0 : from_date > to_date
# 1 : from_date < date_min and to_date < date_max
# 2 : from_date < date_min and to_date > date_max
# 3 : from_date > date_min and to_date < date_max
# 4 : from_date > date_min and to_date > date_max
# 5 : from_date > date_max
# 6 : to_date < date_min
# 7 : from_date == to_date
def compare_date_fini(from_date,to_date,date_min,date_max):
    if compare_dates(from_date,to_date) == 1:
        return 0
    elif compare_dates(from_date,date_min) == 0 and compare_dates(to_date,date_max) == 0:
        if compare_dates(to_date,date_min) == 0:
            return 6
        return 1
    elif compare_dates(from_date,date_min) == 0 and compare_dates(to_date,date_max) == 1:
        return 2
    elif compare_dates(from_date,date_min) == 1 and compare_dates(to_date,date_max) == 0: 
        return 3
    elif compare_dates(from_date,date_min) == 1 and compare_dates(to_date,date_max) == 1: 
        if compare_dates(from_date,date_max) == 1: 
            return 5
        return 4
    elif compare_dates(from_date,to_date) == 2:
        return 7

def plot_emotion(file_link, from_date=None, to_date=None):
    data = pd.read_csv(file_link)
    date, tweet = data['date'], data['tweet']
    date = date.drop_duplicates()
    dates = date.values # cac ngay
    # y1 : number of negative per day
    # y2 : number of positive per day
    # y3 : number of tweet per day
    x,y1,y2,y3,label_x = [],[],[],[],[]
    for idx, date in enumerate(dates):
        count = len(data[data["date"] == date])
        y3.append(count)
        label_x.append(date)
    label_x = label_x[::-1]
    y3 = y3[::-1]
    flag = compare_date_fini(from_date,to_date,label_x[0],label_x[-1])
    if flag == 0:
        print("error from_date > to_date")
        return 0
    elif flag == 5:
        print("error from_date > date_max")
        return 5
    elif flag == 6:
        print("error to_date < date_min")
        return 6
    elif flag == 1:
        from_date = label_x[0]
    elif flag == 2:
        from_date = label_x[0]
        to_date = label_x[-1]
    elif flag == 3:
        pass
    elif flag == 4:
        to_date = label_x[-1]
    else:
        pass
    
    tweets = tweet.values # tat ca cac tweet  
    a = emotion.get_data_vi(tweets)
    df2 = pd.DataFrame({'negative':[i[0] for i in a]})
    df3 = pd.DataFrame({'positive':[i[1] for i in a]})
    result = pd.concat([data,df2,df3],axis=1)
    for idx, date in enumerate(dates):
        emotions = result[result["date"] == date]
        emotions = emotions.values
        count_negative = np.sum(emotions[:,2])
        count_positive = np.sum(emotions[:,3])
        x.append(idx)
        y1.append(count_negative)
        y2.append(count_positive)
        label_x.append(date)
    y1 = y1[::-1]
    y2 = y2[::-1]
    
    title = file_link.split('/')[-1]
    title = title.split('.')[0]
    idx1 = label_x.index(from_date)
    idx2 = label_x.index(to_date)
    label_x = label_x[idx1:idx2+1]
    y3 = y3[idx1:idx2+1]
    y1 = y1[idx1:idx2+1]
    y2 = y2[idx1:idx2+1]
    x = [i for i in range(len(y3))]
    xtick = [i*int(len(x)/4) for i in range(4)]
    xtick.append(len(x)-1)
    xlabel = [label_x[i] for i in xtick]
    fig, (ax1, ax2) = plt.subplots(2,1,figsize = (12, 6))
    ax2.plot(x,y2)
    ax2.plot(x,y1)
    ax2.set_xticks(xtick)
    ax2.set_xticklabels(xlabel)
    ax2.set_title("TWEET ABOUT {} EMOTIONS".format(title.upper()))
    ax2.legend(['Positive', 'Negative'], loc='upper right')
    ax1.plot(x,y3)
    ax1.set_xticks(xtick)
    ax1.set_xticklabels(xlabel)
    ax1.set_title("TWEET ABOUT {}".format(title.upper()))
    plt.show()
#change to your path
link = PROJECT_ROOT + '/data_trend/covid_may.csv'
print(link)
#link = '/home/tainp/3_hieunk/Connector/data_trend/covid_may.csv'
plot_emotion(link,'2019-06-31', '2020-07-30')
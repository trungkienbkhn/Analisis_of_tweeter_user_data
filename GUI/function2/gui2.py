import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
from function3 import process
from unidecode import unidecode
import psycopg2, twint, math, urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

qtCreatorFile1 = "function2/gui2.ui" # Enter file here.
qtCreatorFile2 = "function2/gui2_result.ui"
qtCreatorFile3 = "function2/tweet.ui"
qtCreatorFile4 = "function2/user.ui"
qtCreatorFile5 = "function2/emotion.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)
Ui_MainWindow4, QtBaseClass4 = uic.loadUiType(qtCreatorFile4)
Ui_MainWindow5, QtBaseClass5 = uic.loadUiType(qtCreatorFile5)

keyword = ''
from_date = ''
to_date = ''
top = ''
top_place = []
count = []
lang = ''
username_emotion = []
content_emotion = []
userid_emotion = []

class Crawdata:
    def get_tweet(self, keyword, from_date, to_date):
        c = twint.Config()
        c.Since = from_date
        c.Until = to_date
        c.Search = keyword
        c.Lang = "vi"
        c.Store_object = True
        c.Limit = 100
        #c.Hide_output = True
        twint.run.Search(c)
        tweets = twint.output.tweets_list
        return tweets

    def get_user(self, user_id):
        data = []
        for j in range(0, len(user_id)):
            c = twint.Config()
            c.User_id = user_id[j]
            c.Store_object = True
            #c.Hide_output = True
            twint.run.Lookup(c)
            users = twint.output.users_list
            data.append(users[len(users)-1].location)
        return data

    def get_tweet_emotion(self,keyword,lang,from_date,to_date):
        c = twint.Config()
        c.Since = from_date
        c.Until = to_date
        c.Search = keyword
        c.Lang = lang
        c.Store_object = True
        #c.Limit = 100
        #c.Hide_output = True
        twint.run.Search(c)
        tweets = twint.output.tweets_list
        return tweets

    def get_user_emotion(self, user_id):
        c = twint.Config()
        c.User_id = user_id
        c.Store_object = True
        #c.Hide_output = True
        twint.run.Lookup(c)
        users = twint.output.users_list
        return users

class GetPsql:
    # Connect to databse
    conn = psycopg2.connect(user = "postgres",
                            password = "s",
                            host = "localhost",
                            port = "5432",
                            database = "function2")

    def __init__(self):
        self.cur = self.getdb()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def getdb(self):
        return self.conn.cursor()

    # Query from database
    def get_top_place(self, keyword, from_date, to_date, top):
        self.cur.execute('''select location, count(location) as count
                            from location
                            where keyword like '{}' and user_id in 
                            (select user_id
                            from tweet
                            where create_at between '{}' and '{}'
                            group by user_id
                            order by count(user_id))
                            group by location
                            order by count desc
                            limit {} '''.format(keyword, from_date, to_date, top))
        return self.cur.fetchall()

    def get_tweet(self, from_date, to_date, location):
        self.cur.execute('''select tu.username, t.* 
                            from tweet as t, location as l, tweeter as tu
                            where t.create_at between '{}' and '{}' 
                            and tu.id = l.user_id and l.location = '{}'
                            and tu.id = t.user_id
                            group by tu.username, t.user_id, t.id '''.format(from_date, to_date, location))
        return self.cur.fetchall()

    def get_user(self, username):
        self.cur.execute('''select *
                            from tweeter as tu
                            where tu.username = '{}' '''.format(username))
        return self.cur.fetchall()

    def plotbar(self, data):
        fig, ax = plt.subplots(figsize=(10, 10))
        y_pos = np.arange(len(data['location']))
        ax.barh(y_pos, data['count'], align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data['location'])
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('count')
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

    def pie_chart(self, arr):
        labels = ['Negative', 'Positive']
        pos, neg = 0,0
        if(len(arr)==1):
            sizes = [arr[0][0],arr[0][1]]
            if(arr[0][0]<0.5):
                pos = 1
            else:
                neg = 1
        else:
            
            for arr1 in arr:
                if(arr1[0]<0.5):
                    pos +=1
                else:
                    neg +=1
            sizes = [neg,pos]
        neg_string = "Negative-" + str(neg) 
        pos_string = "Positive-" + str(pos)
        labels = [neg_string,pos_string]
        colors = ['red', 'lightskyblue','lightcoral']
        fig1, ax1 = plt.subplots(figsize=(8,5))
        ax1.pie(sizes, colors=colors, shadow=True, startangle=0,autopct='%1.1f%%')
        ax1.axis('equal')
        text = "Total " + str(len(arr)) + " tweets"
        ax1.text(1.02,0.68,text)
        ax1.set_title("Positive and Negative Ratio")
        ax1.legend(labels=labels)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class Compare:
    #plot trending tweet following days
    # 0 : date1 < date2, 1 : date1 > date2
    def compare_dates(self, date1, date2):

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
    def compare_date_fini(self, from_date,to_date,date_min,date_max):
        if Compare().compare_dates(from_date,to_date) == 1:
            return 0
        elif Compare().compare_dates(from_date,date_min) == 0 and Compare().compare_dates(to_date,date_max) == 0:
            if Compare().compare_dates(to_date,date_min) == 0:
                return 6
            return 1
        elif Compare().compare_dates(from_date,date_min) == 0 and Compare().compare_dates(to_date,date_max) == 1:
            return 2
        elif Compare().compare_dates(from_date,date_min) == 1 and Compare().compare_dates(to_date,date_max) == 0: 
            return 3
        elif Compare().compare_dates(from_date,date_min) == 1 and Compare().compare_dates(to_date,date_max) == 1: 
            if Compare().compare_dates(from_date,date_max) == 1: 
                return 5
            return 4
        elif Compare().compare_dates(from_date,to_date) == 2:
            return 7

class Plot_trending:
    def plot_emotion(self, file_link, from_date=None, to_date=None):
        data = pd.read_csv(file_link)
        date = data['date']
        date = date.drop_duplicates()
        dates = date.values # cac ngay
    # y1 : number of negative per day
    # y2 : number of positive per day
    # y3 : number of tweet per day
        x,y1,y2,y3,label_x = [],[],[],[],[]
        for idx, date in enumerate(dates):
            datas = data[data["date"] == date]
            y3.append(len(datas))
            label_x.append(date)
        #emotion1 = result[result["date"] == date]
            datas = datas.values
            count_negative = np.sum(datas[:,2])
            count_positive = np.sum(datas[:,3])
            x.append(idx)
            y1.append(count_negative)
            y2.append(count_positive)
        #label_x.append(date)
        label_x = label_x[::-1]
        y1 = y1[::-1]
        y2 = y2[::-1]
        y3 = y3[::-1]
        cpr = Compare()
        flag = cpr.compare_date_fini(from_date,to_date,label_x[0],label_x[-1])
        if flag == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("From time > to time")
            x = msg.exec_()
            return 0
        elif flag == 5:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("From time > date max in database")
            x = msg.exec_()
            return 5
        elif flag == 6:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("To time < date min in database")
            x = msg.exec_()
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

class Funct2(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.filter.clicked.connect(self.get_input)
        self.emotion.clicked.connect(self.get_emotion)
        self.trending.clicked.connect(self.get_trending)

    def come_back(self):
        pos = self.pos()
        self.main = app.Homepage()
        self.main.move(pos)
        self.main.show()
        self.close()

    def get_input(self):
        global top, keyword, from_date, to_date
        #get data arguments from buttons
        top = self.top.currentText()
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")
        a = Compare()
        b = a.compare_dates(from_date, to_date)
        if (b == 1):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("From date > to_date")
            msg.exec_()
        else:
            key1 = self.key1.text()
            pos = self.pos()
            if (key1 != "Type Keyword") and (key1 != ""):
                keyword = key1
                self.main = Funct2Result2()
            else:
                keyword = self.key2.currentText() 
                self.main = Funct2Result1()
            self.main.move(pos)
            self.main.show()
            self.close()

    def get_emotion(self):
        global top, keyword, from_date, to_date, lang
        global username_emotion, userid_emotion, content_emotion, emotion
        #get data arguments from buttons
        top = self.top.currentText()
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")
        a = Compare()
        b = a.compare_dates(from_date, to_date)
        if (b == 1):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("From date > to_date")
            msg.exec_()
        else:
            lang = self.lang.currentText()
            key1 = self.key1.text()
            if (key1 != "Type Keyword") and (key1 != ""):
                keyword = key1
            data = Crawdata()
            tweets = []
            tweets = data.get_tweet_emotion(keyword, lang, from_date, to_date)
            if (tweets == []):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Keyword is not common, choose the keyword again")
                x = msg.exec_()
            else:
                username_emotion = []
                content_emotion = []
                userid_emotion = []
                for tweet in tweets:
                    username_emotion.append(tweet.username)
                    content_emotion.append(tweet.tweet)         
                    userid_emotion.append(tweet.user_id)

                tweets.clear()
                data1 = process.Emotion()
                if (lang == "en"):
                    emotion = data1.get_data_en(content_emotion) 
                else:
                    emotion = data1.get_data_vi(content_emotion) 
                pos = self.pos()
                self.main = Emotion()
                self.main.move(pos)
                self.main.show()
                self.close()

    def get_trending(self):
        f_date = self.from_date.date().toString("yyyy-MM-dd")
        t_date = self.to_date.date().toString("yyyy-MM-dd")
        file_link = 'covid_emotion.csv'
        a = Plot_trending()
        a.plot_emotion(file_link, f_date, t_date)
        
class Funct2Result1(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.chart.clicked.connect(self.show_chart)
        self.tweet_result.clicked.connect(self.view_tweet)
        # Show result from database
        global top, keyword, from_date, to_date
        a = GetPsql()
        b = a.get_top_place(keyword, from_date, to_date, top)
        for i in range(0, int(top)):
            self.result.setRowCount(int(top))
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(b[i][1])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(b[i][0]))
            self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(0, int(top)):
            self.location.addItem(b[i][0])

    def come_back(self):
        pos = self.pos()
        self.main = Funct2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def show_chart(self):   
        a = GetPsql()
        global top, keyword, from_date, to_date
        b = a.get_top_place(keyword, from_date, to_date, top)  
        c = []
        d = []
        dict1 = {}
        for i in b:
            c.append(i[0])
            d.append(i[1])
        dict1['location'] = c
        dict1['count'] = d
        a.plotbar(dict1)

    def view_tweet(self):
        global location
        location = self.location.currentText()
        pos = self.pos()
        self.main = Tweet()
        self.main.move(pos)
        self.main.show()
        self.close()

class Funct2Result2(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.chart.clicked.connect(self.set_chart)

        global top, keyword, from_date, to_date, top_place, count
        data = Crawdata()
        tweets = data.get_tweet(keyword,from_date,to_date)
        id = []
        for tweet in tweets:
            id.append(tweet.user_id)
        df = pd.DataFrame()
        df['id'] = id
        df = df.drop_duplicates()
        user_id = df['id'].values      
        location = data.get_user(user_id)
        top_place = []
        count = []
        list_place = []
        for i in range(0, len(location)):
            if (location[i] != ''):
                d = location[i].lower().replace(" ", "")
                if (d.count("-") > 0):        
                    e = d.split("-")
                else: 
                    e = d.split(",")

                for j in range(0, len(e)):
                    if (e[j].isdigit() == False):
                        list_place.append(unidecode(e[j]))

        dem = 0
        while (dem < int(top)):  
            max = 0
            j = 0
            top_p = ''
            for i in range(0, len(list_place)):
                if (max < list_place.count(list_place[i])):
                    max = list_place.count(list_place[i])
                    top_p = list_place[i]
            top_place.append(top_p)
            count.append(max)
            while (list_place.count(top_p) > 0):
                if (list_place[j] == top_p):
                    list_place.pop(j)
                    j -= 1
                j += 1

            dem += 1

        for i in range(0, int(top)):
            self.result.setRowCount(int(top))
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(count[i])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(top_place[i]))
            self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
    def come_back(self):
        pos = self.pos()
        self.main = Funct2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def set_chart(self):
        global top_place, count
        a = GetPsql()
        dict1 = {}
        dict1['location'] = top_place
        dict1['count'] = count
        a.plotbar(dict1)

class Emotion(QtWidgets.QMainWindow, Ui_MainWindow5):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow5.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.user_detail.clicked.connect(self.view_user)
        self.chart.clicked.connect(self.show_chart)
        # Show result from database
        global from_date, to_date, lang, keyword, username_emotion, content_emotion, userid_emotion, emotion
        self.tweet_count.setText(str(len(content_emotion)))
        self.keyword.setText(keyword)
        for i in range(0, len(content_emotion)):
            self.result.setRowCount(len(content_emotion))
            self.result.resizeRowsToContents()
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(emotion[i][0])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(emotion[i][1])))
            self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(username_emotion[i]))
            self.result.setItem(i, 3, QtWidgets.QTableWidgetItem(content_emotion[i]))
        header = self.result.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
 
        df = pd.DataFrame()
        df['username'] = username_emotion
        df = df.drop_duplicates()
        username = df['username'].values
        self.username.addItems(username)

    def come_back(self):
        pos = self.pos()
        self.main = Funct2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def view_user(self):
        global username
        username = self.username.currentText()
        pos = self.pos()
        self.main = User_emotion()
        self.main.move(pos)
        self.main.show()
        self.close()

    def show_chart(self):   
        a = GetPsql()
        global emotion
        a.pie_chart(emotion)

class User_emotion(QtWidgets.QMainWindow, Ui_MainWindow4):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow4.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)

        global username, username_emotion, userid_emotion
        id = ""
        for i in range(0, len(username_emotion)):
            if (username_emotion[i] == username):
                id = userid_emotion[i]

        data = Crawdata()
        users = data.get_user_emotion(id)
        name = ''
        address = ''
        tweet = ''
        following = ''
        follower = ''
        avatar_url = ''
        for user in users:
            name = user.name
            address = user.location
            tweet = user.tweets
            following = user.following
            follower = user.followers
            avatar_url = user.avatar
        avatar = QtGui.QImage()
        try:
            avatar_data = urllib.request.urlopen(avatar_url).read()
            avatar.loadFromData(avatar_data)
            self.avatar.setPixmap(QtGui.QPixmap(avatar))
        except:
            pass
        self.name.setText(name)
        self.username.setText(username)
        self.tweet.setText(str(tweet))
        self.following.setText(str(following))
        self.follower.setText(str(follower))

    def come_back(self):
        pos = self.pos()
        self.main = Emotion()
        self.main.move(pos)
        self.main.show()
        self.close()

class Tweet(QtWidgets.QMainWindow, Ui_MainWindow3):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.user_detail.clicked.connect(self.view_user)
        # Show result from database
        global from_date, to_date, location
        a = GetPsql()
        b = a.get_tweet(from_date, to_date, location)
        self.tweet_count.setText(str(len(b)))
        self.location.setText(location)
        for i in range(0, len(b)):
            self.result.setRowCount(len(b))
            self.result.resizeRowsToContents()
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(b[i][0]))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(b[i][4].day) + "-" + str(b[i][4].month) + "-" + str(b[i][4].year)))
            self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(str(b[i][5])))
            self.result.setItem(i, 3, QtWidgets.QTableWidgetItem(b[i][3]))
        header = self.result.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        c = []
        for i in range(0, len(b)):
            c.append(b[i][0])
        df = pd.DataFrame()
        df['username'] = c
        df = df.drop_duplicates()
        username = df['username'].values
        self.username.addItems(username)

    def come_back(self):
        pos = self.pos()
        self.main = Funct2Result1()
        self.main.move(pos)
        self.main.show()
        self.close()

    def view_user(self):
        global username
        username = self.username.currentText()
        pos = self.pos()
        self.main = User()
        self.main.move(pos)
        self.main.show()
        self.close()

class User(QtWidgets.QMainWindow, Ui_MainWindow4):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow4.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        global username
        a = GetPsql()
        b = a.get_user(username)
        avatar_url = b[0][6]
        avatar = QtGui.QImage()
        try:
            avatar_data = urllib.request.urlopen(avatar_url).read()
            avatar.loadFromData(avatar_data)
            self.avatar.setPixmap(QtGui.QPixmap(avatar))
        except:
            pass
        self.name.setText(b[0][1])
        self.name.adjustSize()
        self.username.setText(b[0][2])
        self.tweet.setText(str(b[0][3]))
        self.following.setText(str(b[0][4]))
        self.follower.setText(str(b[0][5]))

    def come_back(self):
        pos = self.pos()
        self.main = Tweet()
        self.main.move(pos)
        self.main.show()
        self.close()

#hust

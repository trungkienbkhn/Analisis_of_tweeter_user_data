import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from function1 import gui1_1
from geopy.geocoders import Nominatim
import app
import psycopg2, twint, urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

qtCreatorFile1 = "function1/gui1_2.ui" # Enter file here.
qtCreatorFile2 = "function1/gui1_result.ui"
qtCreatorFile3 = "function1/tweet.ui"
qtCreatorFile4 = "function1/user.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)
Ui_MainWindow4, QtBaseClass4 = uic.loadUiType(qtCreatorFile4)

geo = ''
from_date = ''
to_date = ''
ht_display = ''
list_ht = []
top_ht = []
count = []
list_tweet = []
list_user = []
hashtag = ''
tweet_ht = []
user_ht = []
list_id = []
id_ht = []
username = ''

class Crawdata:
    def get_tweet(self, geo, from_date, to_date):
        c = twint.Config()
        c.Since = from_date
        c.Until = to_date
        c.Geo = geo
        c.Store_object = True
        #c.Lang = "vi"
        #c.Hide_output = True
        twint.run.Search(c)
        tweets = twint.output.tweets_list
        return tweets

    def get_user(self, user_id):
        c = twint.Config()
        c.User_id = user_id
        c.Store_object = True
        #c.Hide_output = True
        twint.run.Lookup(c)
        users = twint.output.users_list
        return users

class Plot_chart:
    def plotbar(self,data):
        fig, ax = plt.subplots(figsize=(10, 10))
        y_pos = np.arange(len(data['hashtag']))
        ax.barh(y_pos, data['count'], align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data['hashtag'])
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('count')
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

class Funct1_2(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.choose_the_city.clicked.connect(self.switch_to_funct1_1)
        self.filter.clicked.connect(self.get_input)

    def come_back(self):
        pos = self.pos()
        self.main = app.Homepage()
        self.main.move(pos)
        self.main.show()
        self.close()

    def switch_to_funct1_1(self):
        pos = self.pos()
        self.main = gui1_1.Funct1_1()
        self.main.move(pos)
        self.main.show()
        self.close()

    def get_input(self):
        global ht_display, geo, from_date, to_date, list_ht, top_ht, count, list_tweet, list_user, list_id
        address = self.address.text()
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        if (location == None):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Address not correct !")
            x = msg.exec_()
        else:
            lat = location.latitude
            lon = location.longitude
            radius = self.radius.value()
            if (radius == 0):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please select radius > 0")
                x = msg.exec_()
            else:
                geo = str(lat) + "," + str(lon) + "," + str(radius) + "km"
                ht_display = self.top.currentText()
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
                    # Crawl data
                    data = Crawdata()
                    tweets = data.get_tweet(geo, from_date, to_date)
                    list_ht = []
                    top_ht = []
                    count = []
                    list_tweet = []
                    list_id = []
                    for tweet in tweets:
                        if (tweet.hashtags != "[]"):
                            e = tweet.hashtags
                            list_tweet.append(tweet.tweet)
                            list_user.append(tweet.username)
                            list_id.append(tweet.user_id)
                            for j in range(0, len(e)):
                                list_ht.append(e[j])
                    dem = 0
                    tweets.clear()
                    while (dem < (int(ht_display))):  
                        max = 0
                        j = 0
                        top = ''
                        for i in range(0,len(list_ht)):
                            if (max < list_ht.count(list_ht[i])):
                                max = list_ht.count(list_ht[i])
                                top = list_ht[i]
                        top_ht.append(top)
                        count.append(max)
                        while (list_ht.count(top) > 0):
                            if (list_ht[j] == top):
                                list_ht.pop(j)
                                j -= 1
                            j += 1
                        dem += 1

                    # Show result GUI
                    pos = self.pos()
                    self.main = Funct1Result()
                    self.main.move(pos)
                    self.main.show()
                    self.close()

class Funct1Result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.chart.clicked.connect(self.set_chart)
        self.tweet_result.clicked.connect(self.view_tweet)
        global ht_display, geo, from_date, to_date, list_ht, top_ht, count, list_tweet
        
        for i in range(0,int(ht_display)):
            self.result.setRowCount(int(ht_display))
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(count[i])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(top_ht[i]))
            self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(0, int(ht_display)):
            self.hashtag.addItem(top_ht[i])

    def set_chart(self):
        global top_ht, count
        a = Plot_chart()
        dict1 = {}
        dict1['hashtag'] = top_ht
        dict1['count'] = count
        a.plotbar(dict1)

    def come_back(self):
        pos = self.pos()
        self.main = Funct1_2()
        self.main.move(pos)
        self.main.show()
        self.close()

    def view_tweet(self):
        global hashtag
        hashtag = self.hashtag.currentText()
        pos = self.pos()
        self.main = Tweet()
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

        global list_tweet, hashtag, tweet_ht, list_user, user_ht, list_id, id_ht
        tweet_ht = []
        user_ht = []
        id_ht = []
        def subtest(s1, s2):
            return all(x in list(s1) for x in list(s2))

        for i in range(0, len(list_tweet)):
            if (subtest(list_tweet[i], hashtag) == True):
                tweet_ht.append(list_tweet[i])
                user_ht.append(list_user[i])
                id_ht.append(list_id[i])
        self.tweet_count.setText(str(len(tweet_ht)))
        self.hashtag.setText(hashtag)
        for i in range(0, len(tweet_ht)):
            self.result.setRowCount(len(tweet_ht))
            self.result.resizeRowsToContents()
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(user_ht[i]))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(tweet_ht[i]))
        header = self.result.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        c = []
        for i in range(0, len(user_ht)):
            c.append(user_ht[i])
        df = pd.DataFrame()
        df['username'] = c
        df = df.drop_duplicates()
        username = df['username'].values
        self.username.addItems(username)

    def come_back(self):
        pos = self.pos()
        self.main = Funct1Result()
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
        global username, id_ht, user_ht
        id = ""
        for i in range(0, len(user_ht)):
            if (user_ht[i] == username):
                id = id_ht[i]

        data = Crawdata()
        users = data.get_user(id)
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
        self.name.adjustSize()
        self.username.setText(username)
        self.address.setText(address)
        self.tweet.setText(str(tweet))
        self.following.setText(str(following))
        self.follower.setText(str(follower))

    def come_back(self):
        pos = self.pos()
        self.main = Tweet()
        self.main.move(pos)
        self.main.show()
        self.close()

import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
from function3 import process
import twint, urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

qtCreatorFile1 = "function3/gui3.ui"
qtCreatorFile2 = "function3/gui3_result.ui"
qtCreatorFile3 = "function3/user.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)

tweet_id = []
username = []
from_date = []
to_date = []

class Crawdata:
    def get_tweet(self, username, from_date, to_date):
        c = twint.Config()
        c.Since = from_date
        c.Until = to_date
        c.Username = username
        c.Store_object = True
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

class Funct3(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.filter.clicked.connect(self.get_input)

    def come_back(self):
        pos = self.pos()
        self.main = app.Homepage()
        self.main.move(pos)
        self.main.show()
        self.close()

    def get_input(self):
        global tweet_id, username, from_date, to_date, emotion, list_ct, list_id
        tweet_id = []
        username = []
        from_date = []
        to_date = []
        link_text1 = self.link1.text()
        link_text2 = self.link2.text()
        link_text3 = self.link3.text()
        link_text4 = self.link4.text()
        link_text5 = self.link5.text()
        date_text1 = self.date1.date().toString("yyyy-MM-dd")
        date_text2 = self.date2.date().toString("yyyy-MM-dd")
        date_text3 = self.date3.date().toString("yyyy-MM-dd")
        date_text4 = self.date4.date().toString("yyyy-MM-dd")
        date_text5 = self.date5.date().toString("yyyy-MM-dd")
        link = [link_text1, link_text2, link_text3, link_text4, link_text5]
        date = [date_text1, date_text2, date_text3, date_text4, date_text5]

        if (link != ['', '', '', '', '']):
            for i in range(0, len(link)):
                if (link[i] != ''):
                    l = link[i].split("/")
                    if (len(l) != 6
                        or l[2] != 'twitter.com' 
                        or l[4] != 'status'
                        or l[5] == ''):
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("Please enter the tweet link correctly!")
                        x = msg.exec_()
                        link = []
                        break

            if (link != []):
                for i in range(0, len(link)):
                    for j in range(0, len(date)):
                        if link[i] != '' and j == i:
                            l = link[i].split("/")
                            tweet_id.append(l[len(l)-1])
                            username.append(l[len(l)-3])
                            next_date = date[i] + " 23:59:59"
                            from_date.append(date[j])
                            to_date.append(next_date)

                list_ct = []
                list_id = []
                result = ""
                data = Crawdata()
                check = []
                for i in range(0, len(tweet_id)):
                    check.append(0)

                for i in range(0, len(tweet_id)):
                    id = []
                    content = []
                    t = ""
                    tweets = data.get_tweet(username[i], from_date[i], to_date[i])
                    for tweet in tweets:
                        id.append(tweet.id)
                        content.append(tweet.tweet)
                        t = tweet.user_id

                    tweets.clear()
                    for j in range(0, len(content)):
                        if (str(id[j]) == tweet_id[i]):
                            check[i] = 1
                            list_ct.append(content[j])
                    
                    list_id.append(t)
                
                for i in range(0, len(tweet_id)):
                    if (check[i] == 0):
                        text = "Please enter the date in link " + str(i+1) + " correctly!"
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText(text)
                        x = msg.exec_()
                        break 

                if (check.count(0) == 0):    
                    data1 = process.Emotion()
                    emotion = []
                    if (self.lang.currentText() == "en"):
                        emotion = data1.get_data_en(list_ct) 
                    else:
                        emotion = data1.get_data_vi(list_ct)
                    pos = self.pos()
                    self.main = Funct3Result()
                    self.main.move(pos)
                    self.main.show()
                    self.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter the tweet link!")
            x = msg.exec_()

class Funct3Result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.user_detail.clicked.connect(self.view_user)
        global tweet_id, username, from_date, to_date, list_id, list_ct, emotion    
        list_ct = list(dict.fromkeys(list_ct))
        self.tweet_count.setText(str(len(list_ct)))
        for i in range(0, len(list_ct)):
            self.result.setRowCount(len(list_ct))
            self.result.resizeRowsToContents()
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(emotion[i][0])))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(emotion[i][1])))
            self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(username[i]))
            self.result.setItem(i, 3, QtWidgets.QTableWidgetItem(list_ct[i]))
        header = self.result.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.username.addItems(username)

    def come_back(self):
        pos = self.pos()
        self.main = Funct3()
        self.main.move(pos)
        self.main.show()
        self.close()

    def view_user(self):
        global un
        un = self.username.currentText()
        pos = self.pos()
        self.main = User()
        self.main.move(pos)
        self.main.show()
        self.close()

class User(QtWidgets.QMainWindow, Ui_MainWindow3):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        global username, list_id, un
        id = ""
        for i in range(0, len(username)):
            if (username[i] == un):
                id = list_id[i]

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
        self.username.setText(un)
        self.tweet.setText(str(tweet))
        self.following.setText(str(following))
        self.follower.setText(str(follower))

    def come_back(self):
        pos = self.pos()
        self.main = Funct3Result()
        self.main.move(pos)
        self.main.show()
        self.close()

#https://twitter.com/Swamy39/status/1257623414312824834
#https://twitter.com/viothings/status/1265168823101120512
#https://twitter.com/JediJoyBlog/status/1275450563665162246
#26-03
#https://twitter.com/bbcvietnamese/status/1275645429301104646
#24 - 22 -19
#https://twitter.com/bbcvietnamese/status/1275104622647160839
#https://twitter.com/bbcvietnamese/status/1273782631071649792
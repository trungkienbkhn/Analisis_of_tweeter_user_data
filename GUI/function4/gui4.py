import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
from function3 import process
from function4 import tag_cloud
import twint, urllib.request
from datetime import date, datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

qtCreatorFile = "function4/gui4.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

from_date = ''
content = []

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

    def pie_chart(self, arr):
        labels = ['Negative', 'Positive']
        pos, neg = 0,0
        if(len(arr) == 1):
            sizes = [arr[0][0], arr[0][1]]
            if(arr[0][0] < 0.5):
                pos = 1
            else:
                neg = 1
        else:
            
            for arr1 in arr:
                if(arr1[0] < 0.5):
                    pos += 1
                else:
                    neg += 1
            sizes = [neg, pos]
        neg_string = "Negative-" + str(neg) 
        pos_string = "Positive-" + str(pos)
        labels = [neg_string, pos_string]
        colors = ['lightskyblue', 'red','lightcoral']
        fig1, ax1 = plt.subplots(figsize=(8,5))
        ax1.pie(sizes, colors=colors, shadow=True, startangle=0, autopct='%1.1f%%')
        ax1.axis('equal')
        text = "Total " + str(len(arr)) + " tweets"
        ax1.text(1.02, 0.68, text)
        ax1.set_title("Positive and Negative Ratio")
        ax1.legend(labels=labels)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

class Funct4(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.back_arrow.clicked.connect(self.come_back)
        self.filter.clicked.connect(self.get_input)
        self.chart.clicked.connect(self.show_chart)
        self.custom.setChecked(True)
        self.custom.toggled.connect(lambda:self.btnstate(self.custom))
        self.month.toggled.connect(lambda:self.btnstate(self.month))
        self.year.toggled.connect(lambda:self.btnstate(self.year))
        self.full.toggled.connect(lambda:self.btnstate(self.full))

    def come_back(self):
        pos = self.pos()
        self.main = app.Homepage()
        self.main.move(pos)
        self.main.show()
        self.close()

    def btnstate(self, b):
        global from_date
        today = date.today()
        t = str(today).split("-")
        if b.text() == "Custom date":
            if b.isChecked() == True:
                from_date = self.date.date().toString("yyyy-MM-dd")

        if b.text() == "1 month ago":
            if b.isChecked() == True:
                if t[2] == "31":
                    t[2] = "30"
                k = int(t[1]) - 1
                from_date = t[0] + "-" + str(k) + "-" + t[2]

        if b.text() == "Full":
            if b.isChecked() == True:
                from_date = "2018-01-01"

        if b.text() == "1 year ago":
            if b.isChecked() == True:
                k = int(t[0]) - 1
                from_date = str(k) + "-" + t[1] + "-" + t[2]

    def get_input(self):
        global from_date, content
        if self.custom.isChecked() == True:
            from_date = self.date.date().toString("yyyy-MM-dd")

        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        to_date = str(today) + " " + str(current_time)
        content = []
        username = ''
        link = self.link.text()
        if (link != ''):
            l = link.split("/")
            if (len(l) == 4
                and l[2] == 'twitter.com'
                and l[3] != ''):
                username = l[len(l)-1]
                data = Crawdata()
                tweets = data.get_tweet(username, from_date, to_date)
                for tweet in tweets:
                    content.append(tweet.tweet)

                tweets.clear()
                if (len(content) < 10):
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("Please select the timestamp again, collect too few tweets\n(min = 10)")
                    x = msg.exec_()
                else:
                    data1 = tag_cloud.Process()
                    lang = self.lang.currentText()
                    if (lang == "en"):
                        data1.english(content)
                    else:
                        data1.vietnam(content)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please enter the twitter user link correctly!")
                x = msg.exec_()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter the twitter user link!")
            x = msg.exec_()

    def show_chart(self):   
        global content
        data = process.Emotion()
        if (content != []):
            if (self.lang.currentText() == "en"):
                emotion = data.get_data_en(content) 
            else:
                emotion = data.get_data_vi(content) 
            a = Crawdata()
            a.pie_chart(emotion)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Alert")
            msg.setText("Please click filter before viewing the chart!")
            x = msg.exec_()

#https://twitter.com/ClimateHuman
#https://twitter.com/heoxinhminhhang
#https://twitter.com/sontungmtp777
#https://twitter.com/ABC
#https://twitter.com/realDonaldTrump
